import os
import json
import google.generativeai as genai
from PIL import Image

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