import json
from pathlib import Path

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts import BILL_EXTRACTION_PROMPT
from schemas import BillExtraction


client = genai.Client(api_key=GEMINI_API_KEY)


def extract_bill_data(pdf_path: str) -> BillExtraction:

    pdf_file = Path(pdf_path)

    if not pdf_file.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_file}"
        )

    print(f"Reading PDF: {pdf_file}")
    print("Uploading PDF to Gemini...")

    uploaded_file = client.files.upload(
        file=str(pdf_file)
    )

    print("PDF uploaded successfully.")
    print("Sending bill to Gemini...")
    print(f"Model: {GEMINI_MODEL}")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            uploaded_file,
            BILL_EXTRACTION_PROMPT
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=BillExtraction,
            temperature=0
        )
    )

    print("Gemini response received.")

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    data = json.loads(response.text)

    return BillExtraction.model_validate(data)