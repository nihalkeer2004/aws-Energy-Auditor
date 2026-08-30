⚡ Energy Auditor

Energy Auditor is an AI-powered electricity bill analysis application built with Flask, AWS S3, AWS Lambda, and Google Gemini.

Overview

The project allows a user to upload an electricity bill in PDF format through a simple web interface. The uploaded bill is stored in Amazon S3 and prepared for serverless processing. Google Gemini is used to extract structured information from the bill, while Pydantic models provide a consistent data schema.

This is Step 1 of an energy auditing workflow, focused on reliable bill-data extraction and readable reporting.

Features

📄 PDF electricity bill upload

☁️ Amazon S3 storage

🤖 Google Gemini PDF analysis

📊 Structured bill-data extraction

📟 Meter-wise consumption information

🕐 Hourly consumption support

💰 Billing charges and totals

📈 Peak-load and base-load information

⚡ Power-factor information

💡 Energy-saving recommendation display

🔄 S3 polling for asynchronous processing

❤️ Health-check endpoint

🧪 Local PDF extraction testing

📱 Responsive web interface

Project Structure

energy_auditor_step1/
├── app.py
├── config.py
├── gemini_service.py
├── lambda_function.py
├── local_test.py
├── prompts.py
├── schemas.py
├── requirements.txt
├── .env.example
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   ├── index.html
│   ├── processing.html
│   └── result.html
├── test_data/
├── output/
└── lambda_layer/

Technology Stack

Python

Flask

Amazon S3

AWS Lambda

Boto3

Google Gemini API

Pydantic

HTML5

CSS3

JavaScript

How It Works

The user opens the Energy Auditor web application.

The user selects an electricity bill in PDF format.

Flask validates the uploaded file.

The PDF is uploaded to the configured S3 bucket.

An expected JSON output location is generated.

The processing page waits for the generated result.

Gemini analyzes the electricity bill.

Pydantic validates the extracted bill data.

The processed JSON can be stored in S3.

Flask reads the result and displays the Energy Audit Report.

Extracted Information

The schema supports invoice details, customer information, service details, total consumption, electricity charges, demand surcharges, distribution fees, environmental charges, taxes, total amount due, peak-load information, base-load information, highest energy consumer, power factor, meter readings, and hourly consumption.

Local Setup

Create a virtual environment and install the dependencies.

python -m venv venv

Windows:

venv\Scripts\activate

Linux/macOS:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Install the Gemini SDK and Pydantic if required:

pip install google-genai pydantic

Environment Variables

Create a .env file from .env.example.

GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model
AWS_REGION=ap-south-1
S3_BUCKET=your_s3_bucket
S3_INPUT_FOLDER=bills/
S3_OUTPUT_FOLDER=output/
LAMBDA_FUNCTION_NAME=EnergyAuditorBillProcessor
SECRET_KEY=change_this_secret
PROCESSING_TIMEOUT=180
POLLING_INTERVAL=3

Never commit API keys, AWS credentials, private keys, or other secrets to GitHub.

Run the Application

python app.py

Open:

http://localhost:5000

Health check:

http://localhost:5000/health

Local Extraction Test

Test Gemini extraction against a local PDF:

python local_test.py test_data/sample_bill.pdf

The extracted JSON is saved to:

output/extracted_bill.json

AWS Architecture

The intended cloud workflow uses Amazon S3 for input and output storage, with AWS Lambda handling asynchronous bill processing. Flask uploads the PDF and polls S3 for the expected JSON result.

The included Lambda file is currently a placeholder for the next implementation stage, so additional Lambda code and AWS configuration are required for a complete serverless deployment.

Security

Use least-privilege IAM permissions. Keep Gemini and AWS credentials outside the repository. If a private key or credential has ever been committed publicly, revoke or rotate it immediately and remove it from Git history.

Current Status

This repository represents Step 1 of the Energy Auditor project. Flask, S3 upload handling, Gemini extraction, Pydantic schemas, processing UI, result UI, and local testing are included. Further Lambda integration and production hardening can be added in later steps.

License

Add an appropriate license before distributing the project publicly.
