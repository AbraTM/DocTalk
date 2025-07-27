import os
import json
import requests
import time
import google.generativeai as genai
from PIL import Image
from utils.pdf2Img import pdf_to_images
from awsConfig import s3, sqs, S3_BUCKET_NAME, SQS_QUEUE_URL
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

def pollSQS():
    response = sqs.receive_message(
        QueueUrl = SQS_QUEUE_URL,
        MaxNumberOfMessages = 1,
        WaitTimeSeconds = 10
    )

    messages = response.get("Messages", [])
    if not messages:
        return None, None
    
    message = messages[0]
    receipt_handle = message["ReceiptHandle"]
    body = json.loads(message["Body"])

    print(body)
    return body, receipt_handle


TEMP_FOLDER = "temp"
os.makedirs("temp", exist_ok=True)
from urllib.parse import urlparse

def get_s3_key(s3_url):
    parsed_url = urlparse(s3_url)
    return parsed_url.path.lstrip('/')  # Removes leading slash


def downloadFromS3(message):
    file_name = message["file_name"]
    s3_url = message["s3_url"]

    print("In Download")
    local_file_path = os.path.join(TEMP_FOLDER, file_name)
    s3_key = get_s3_key(s3_url)
    s3.download_file(S3_BUCKET_NAME, s3_key, local_file_path)

    print(local_file_path)
    return local_file_path


def processFiles(file_path):
    file_name = os.path.basename(file_path).split(".")[0]
    file_ext = os.path.splitext(file_path)[1].lower()
    images_paths = []

    if file_ext == ".pdf":
        images_paths = pdf_to_images(file_path, file_name)
    elif file_ext in [".png", ".jpg", ".jpeg"]:
        images_paths = [file_path]
    else:
        raise ValueError("Unsupported File Format.")
    
    return images_paths


def summariseReport(image_paths):
    # Gemini Config
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Load Images from paths
    images = []
    for path in image_paths:
        with Image.open(path) as img:
            images.append(img.copy())

    # Prompt to make Gemini Summarise the report
    prompt = """
        You are a medically-aware assistant. A patient has uploaded one or more diagnostic test reports.
        Your job is to analyze the content and generate a structured medical summary that can be shown to non-experts.

        Respond ONLY with a valid JSON object, no extra comments. Use this structure:

        {
        "level_of_concern": "Normal" | "Low" | "Moderate" | "High" | "Critical",
        "main_finding": "<most important finding>",
        "summary_text": "<plain-language explanation of results>",
        "additional_notes": "<optional doctor-style advice, if applicable>"
        }

        Guidelines:
        - Be calm, fact-based, and empathetic.
        - If findings are unclear, say so and recommend professional consultation.
        - Avoid medical jargon unless it is explained clearly.
        - Make sure the summary is detailed, clearing up every relevant thing and making sure the patient is aware of them

        Begin analysis below.
    """

    response = model.generate_content(
        [prompt] + images,
        stream=False
    )
    output_text = response.text.strip()

    try:
        # Parse JSON from response
        json_start = output_text.find("{")
        json_end = output_text.rfind("}") + 1
        json_string = output_text[json_start:json_end]

        # Convert data to Python Dict
        json_data = json.loads(json_string)
        return json_data
    except Exception as e:
        print("JSON Parse Error:" + str(e))
        return{
            "level_of_concern": "Unknown",
            "main_finding": "Could not parse summary",
            "summary_text": "There was a problem generating the summary. Please consult your doctor.",
            "additional_notes": str(e)
        }
    

def main():
    print("EC2 Worker Started..")
    while True:
        try:
            # Getting the report message from SQS Queue
            message_body, message_receipt_handle = pollSQS()
            if not message_body:
                continue
            
            # From the info polled from SQS Queue downloading the report to be summarised
            local_file_path = downloadFromS3(message_body)

            # Process File if it's a PDF into images so it can be passed to gemini-pro-vision
            image_paths = processFiles(local_file_path)

            # Summarize
            summary_filename = f"summaries/{message_body['file_id']}_summary.json"
            summary = summariseReport(image_paths)
            summary_file = BytesIO(json.dumps(summary).encode("utf-8"))

            # Store Summary in S3
            s3.upload_fileobj(
                summary_file, 
                S3_BUCKET_NAME, 
                summary_filename,
                ExtraArgs={"ContentType": "application/json"}
            )
            summary_s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{summary_filename}"

            # Storing Summary in Postgres
            response = requests.post(
                os.getenv("BACKEND_API_URL"),
                json={
                    "file_id": message_body["file_id"],
                    "summary_s3_url": summary_s3_url
                }
            )
            if not response.ok:
                raise Exception(f"Failed to POST summary to backend: {response.status_code} - {response.text}")

            # Clean up
            # Deleting the SQS Queue message
            sqs.delete_message(SQS_QUEUE_URL, message_receipt_handle)
            # Deleting the file from local storage
            print(local_file_path)
            if os.path.exists(local_file_path):
                os.remove(local_file_path)
            # Deleting images or any generated images from local storage
            for path in image_paths:
                if os.path.exists(path):
                    os.remove(path)

        except Exception as e:
            print(f"Error Occured: {str(e)}")
            time.sleep(5)


if __name__ == "__main__":
    main()
