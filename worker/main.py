import os
import json
import requests
import time
from utils.pollSQS import pollSQS
from utils.downloadFromS3 import downloadFromS3
from utils.processFiles import processFiles
from utils.summariseReport import summariseReport
from awsConfig import s3, S3_BUCKET_NAME, sqs, SQS_QUEUE_URL
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()
TEMP_FOLDER = "temp"
    
def main():
    print("EC2 Worker Started..")
    while True:
        try:
            # Getting the report message from SQS Queue
            print("Polling the SQS Queue..")
            message_body, message_receipt_handle = pollSQS()
            if not message_body:
                print("No message received. Waiting for some time...\n\n")
                continue
            
            print(f"Message received for file: {message_body['file_name']}")
            should_delete = False

            try:
                # From the info polled from SQS Queue downloading the report to be summarised
                print(f"Downloading file form S3...")
                local_file_path = downloadFromS3(message_body)
                print(f"File Downloaded to: {local_file_path}")

                # Process File if it's a PDF into images so it can be passed to gemini-pro-vision
                print(f"Pre-Processing Files..")
                image_paths = processFiles(local_file_path)

                # Summarize
                print("Sending images to Gemini LLM for summarization...")
                summary_filename = f"summaries/{message_body['file_id']}_summary.json"
                summary = summariseReport(image_paths)
                summary_file = BytesIO(json.dumps(summary).encode("utf-8"))
                print("Summary generated.")

                # Store Summary in S3
                print("Uploading the summary to S3...")
                s3.upload_fileobj(
                    summary_file, 
                    S3_BUCKET_NAME, 
                    summary_filename,
                    ExtraArgs={"ContentType": "application/json"}
                )
                summary_s3_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{summary_filename}"
                print("Summary uploaded to S3 successfully at : {summary_s3_url}")

                # Storing Summary in Postgres
                print("Saving summary metadata to backend...")
                response = requests.post(
                    os.getenv("BACKEND_API_URL"),
                    json={
                        "file_id": message_body["file_id"],
                        "summary_s3_url": summary_s3_url
                    }
                )
                if not response.ok:
                    raise Exception(f"Failed to POST summary to backend: {response.status_code} - {response.text}")
                print("Summary metadata successfully stored in backend...")
                should_delete = True

            finally:
                # Clean up
                print("Cleaning up local temp files...")
                # Deleting the file from local storage
                print(local_file_path)
                if os.path.exists(local_file_path):
                    os.remove(local_file_path)
                # Deleting images or any generated images from local storage
                for path in image_paths:
                    if os.path.exists(path):
                        os.remove(path)
                if should_delete:
                    # Deleting the SQS Queue message
                    print("Deleting current message form SQS queue...")
                    sqs.delete_message(
                        QueueUrl = SQS_QUEUE_URL,
                        ReceiptHandle = message_receipt_handle
                    )
                else:
                    print("Message was not deleted due to error in processing.")

            print("Process Complete for current message.\n\n")
        except Exception as e:
            print(f"Error Occured: {str(e)}")
            time.sleep(5)


if __name__ == "__main__":
    main()
