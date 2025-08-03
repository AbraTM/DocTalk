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

        Respond ONLY with a valid JSON object, no extra comments or markdown. Use this structure:

        {
            "level_of_concern": "Normal" | "Low" | "Moderate" | "High" | "Critical",
            "main_finding": "<most important finding>",
            "quick_summary": "<2-4 sentence layman explanation of the result>",
            "detailed_summary": "<longer, 10-15 sentence explanation going into relevant metrics, implications, and clarifying medical terms>",
            "additional_notes": "<optional doctor-style advice, lifestyle suggestions, or follow-up recommendations>",
            "tags": ["<keyword1>", "<keyword2>", ...],
            "recommended_action": "Monitor" | "Routine Checkup" | "Consult Doctor" | "Urgent Attention"
        }

        Guidelines:
        - Be calm, fact-based, and empathetic.
        - Explain all relevant terms (e.g., QT interval, WBC) in non-technical language.
        - If findings are unclear or borderline, indicate so with a confidence level and advise consultation.
        - Use bullet-point style only in `additional_notes`, if it improves readability.
        - Never include markdown, explanations, or code blocks — only raw JSON.

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
            "main_finding": "Could not parse report.",
            "quick_text": "There was a problem generating the summary. Please consult your doctor.",
            "error": str(e)
        }