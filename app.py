import os
import json
import time
import uuid

import boto3

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from botocore.exceptions import ClientError

from config import Config


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.config.from_object(Config)


# =========================================================
# AWS S3
# =========================================================

s3 = boto3.client(
    "s3",
    region_name=app.config["AWS_REGION"]
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def allowed_file(filename):
    """
    Check whether uploaded file is an allowed file type.
    """

    if not filename:
        return False

    if "." not in filename:
        return False

    extension = filename.rsplit(
        ".",
        1
    )[1].lower()

    return extension in app.config[
        "ALLOWED_EXTENSIONS"
    ]


# =========================================================
# GENERATE OUTPUT JSON KEY
# =========================================================

def get_output_key(input_key):

    filename = input_key.split("/")[-1]

    base_filename = os.path.splitext(
        filename
    )[0]

    return (
        f"{app.config['S3_OUTPUT_FOLDER']}"
        f"{base_filename}.json"
    )


# =========================================================
# GET JSON RESULT FROM S3
# =========================================================

def get_json_from_s3(output_key):

    try:

        response = s3.get_object(
            Bucket=app.config["S3_BUCKET"],
            Key=output_key
        )

        content = response[
            "Body"
        ].read().decode("utf-8")

        return json.loads(content)

    except ClientError as error:

        error_code = error.response[
            "Error"
        ].get("Code")

        if error_code in [
            "NoSuchKey",
            "404",
            "NoSuchBucket"
        ]:

            return None

        raise


# =========================================================
# WAIT FOR LAMBDA RESULT
# =========================================================

def wait_for_result(output_key):

    timeout = app.config[
        "PROCESSING_TIMEOUT"
    ]

    interval = app.config[
        "POLLING_INTERVAL"
    ]

    start_time = time.time()

    while (
        time.time() - start_time
        < timeout
    ):

        print(
            f"Checking S3 for result: {output_key}"
        )

        data = get_json_from_s3(
            output_key
        )

        if data is not None:

            print(
                "Processing result found."
            )

            return data

        time.sleep(interval)

    print(
        "Processing timed out."
    )

    return None


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# UPLOAD BILL
# =========================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_bill():

    try:

        # -------------------------------------------------
        # CHECK FILE
        # -------------------------------------------------

        if "bill" not in request.files:

            flash(
                "Please select an electricity bill PDF."
            )

            return redirect(
                url_for("index")
            )

        file = request.files["bill"]

        if not file.filename:

            flash(
                "No file selected."
            )

            return redirect(
                url_for("index")
            )


        # -------------------------------------------------
        # VALIDATE PDF
        # -------------------------------------------------

        if not allowed_file(
            file.filename
        ):

            flash(
                "Only PDF electricity bills are allowed."
            )

            return redirect(
                url_for("index")
            )


        # -------------------------------------------------
        # ORIGINAL FILE NAME
        # -------------------------------------------------

        original_filename = file.filename


        # -------------------------------------------------
        # GENERATE UNIQUE FILE NAME
        # -------------------------------------------------

        extension = os.path.splitext(
            original_filename
        )[1].lower()

        unique_id = uuid.uuid4().hex[:12]

        safe_filename = (
            f"bill_{unique_id}"
            f"{extension}"
        )


        # -------------------------------------------------
        # S3 INPUT KEY
        # -------------------------------------------------

        s3_key = (
            f"{app.config['S3_INPUT_FOLDER']}"
            f"{safe_filename}"
        )


        print("=" * 60)

        print(
            "Uploading electricity bill..."
        )

        print(
            f"Original filename: "
            f"{original_filename}"
        )

        print(
            f"S3 Bucket: "
            f"{app.config['S3_BUCKET']}"
        )

        print(
            f"S3 Key: {s3_key}"
        )

        print("=" * 60)


        # -------------------------------------------------
        # UPLOAD PDF TO S3
        # -------------------------------------------------

        s3.upload_fileobj(
            file,
            app.config["S3_BUCKET"],
            s3_key,
            ExtraArgs={
                "ContentType": "application/pdf"
            }
        )


        print(
            "PDF uploaded successfully."
        )


        # -------------------------------------------------
        # GENERATE EXPECTED OUTPUT KEY
        # -------------------------------------------------

        output_key = get_output_key(
            s3_key
        )


        print(
            f"Expected Lambda output: "
            f"{output_key}"
        )


        # -------------------------------------------------
        # PROCESSING PAGE
        # -------------------------------------------------

        return render_template(
            "processing.html",
            filename=original_filename,
            s3_key=s3_key,
            output_key=output_key
        )


    except Exception as error:

        print("=" * 60)
        print("UPLOAD ERROR")
        print("=" * 60)

        print(
            type(error).__name__
        )

        print(
            str(error)
        )


        flash(
            f"Upload failed: {str(error)}"
        )

        return redirect(
            url_for("index")
        )


# =========================================================
# PROCESS BILL
# =========================================================

@app.route(
    "/process",
    methods=["GET"]
)
def process_bill():

    output_key = request.args.get(
        "output_key"
    )

    s3_key = request.args.get(
        "s3_key"
    )


    # -----------------------------------------------------
    # VALIDATE PARAMETERS
    # -----------------------------------------------------

    if not output_key:

        flash(
            "Missing processing information."
        )

        return redirect(
            url_for("index")
        )


    if not s3_key:

        flash(
            "Missing S3 file information."
        )

        return redirect(
            url_for("index")
        )


    print("=" * 60)

    print(
        "WAITING FOR LAMBDA PROCESSING"
    )

    print(
        f"Input key: {s3_key}"
    )

    print(
        f"Output key: {output_key}"
    )

    print("=" * 60)


    # -----------------------------------------------------
    # WAIT FOR OUTPUT JSON
    # -----------------------------------------------------

    data = wait_for_result(
        output_key
    )


    # -----------------------------------------------------
    # TIMEOUT
    # -----------------------------------------------------

    if data is None:

        return render_template(
            "processing.html",
            filename=s3_key,
            s3_key=s3_key,
            output_key=output_key,
            timeout=True
        )


    # -----------------------------------------------------
    # RESULT PAGE
    # -----------------------------------------------------

    print("=" * 60)

    print(
        "BILL PROCESSING COMPLETED"
    )

    print("=" * 60)


    return render_template(
        "result.html",
        data=data,
        source_key=s3_key,
        output_key=output_key
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "service": "Energy Auditor"
    }


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )