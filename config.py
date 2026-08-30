import os
from dotenv import load_dotenv

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3-flash-preview"
)

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Please add it to the .env file."
    )


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

class Config:

    # -----------------------------------------------------
    # Flask
    # -----------------------------------------------------

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "energy-auditor-secret-key"
    )


    # -----------------------------------------------------
    # AWS
    # -----------------------------------------------------

    AWS_REGION = os.environ.get(
        "AWS_REGION",
        "ap-south-1"
    )


    # -----------------------------------------------------
    # S3 BUCKET
    # -----------------------------------------------------

    S3_BUCKET = os.environ.get(
        "S3_BUCKET",
        "nihal-energy-auditor-2026"
    )


    # -----------------------------------------------------
    # S3 INPUT FOLDER
    # Uploaded PDF bills
    # -----------------------------------------------------

    S3_INPUT_FOLDER = os.environ.get(
        "S3_INPUT_FOLDER",
        "bills/"
    )


    # -----------------------------------------------------
    # S3 OUTPUT FOLDER
    # Lambda-generated JSON
    # -----------------------------------------------------

    S3_OUTPUT_FOLDER = os.environ.get(
        "S3_OUTPUT_FOLDER",
        "output/"
    )


    # -----------------------------------------------------
    # Lambda
    # -----------------------------------------------------

    LAMBDA_FUNCTION_NAME = os.environ.get(
        "LAMBDA_FUNCTION_NAME",
        "EnergyAuditorBillProcessor"
    )


    # -----------------------------------------------------
    # Allowed upload extensions
    # -----------------------------------------------------

    ALLOWED_EXTENSIONS = {
        "pdf"
    }


    # -----------------------------------------------------
    # Processing settings
    # -----------------------------------------------------

    PROCESSING_TIMEOUT = int(
        os.environ.get(
            "PROCESSING_TIMEOUT",
            "180"
        )
    )


    POLLING_INTERVAL = int(
        os.environ.get(
            "POLLING_INTERVAL",
            "3"
        )
    )