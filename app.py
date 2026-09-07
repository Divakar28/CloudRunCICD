import logging
import os

from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/", methods=["POST"])
def gcs_event():

    event = request.get_json(silent=True)

    if not event:
        logging.error("No event received")
        return "Invalid event", 400

    bucket_name = event.get("bucket")
    file_name = event.get("name", "")

    logging.info("Bucket: %s", bucket_name)
    logging.info("File: %s", file_name)

    # --------------------------------------------------
    # Validate bucket
    # --------------------------------------------------

    if bucket_name != "div_test_cicd":
        logging.info("Ignoring different bucket: %s", bucket_name)
        return "Ignored - different bucket", 200

    # --------------------------------------------------
    # Validate folder
    # --------------------------------------------------

    if not file_name.startswith("raw_data/"):
        logging.info(
            "Ignoring file outside raw_data folder: %s",
            file_name
        )
        return "Ignored - not raw_data folder", 200

    # --------------------------------------------------
    # Validate CSV
    # --------------------------------------------------

    if not file_name.lower().endswith(".csv"):
        logging.info(
            "Ignoring non-CSV file: %s",
            file_name
        )
        return "Ignored - not CSV", 200

    # --------------------------------------------------
    # CSV detected
    # --------------------------------------------------

    logging.info(
        "CSV FILE DETECTED: gs://%s/%s",
        bucket_name,
        file_name
    )

    # --------------------------------------------------
    # Add your CSV processing logic here
    # --------------------------------------------------

    return "CSV file processed successfully", 200


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )