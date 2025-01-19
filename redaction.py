import requests
import json

API_KEY = "<INSERT API KEY>"
API_URL = "https://api.censori.ontelio.ai"
FILENAME = "preamble.json"
LANGUAGE = "en"
ENTITIES = []
# ENTITIES = ["PERSON", "LOCATION"]
CALLBACK = "<INSERT CALLBACK URL>"


def send_media() -> str:
    """
    Sends media to Ontelio's Redaction Engine. Input parameters in the form of json body.

    Raises:
        Exception: Missing a Job ID
        Exception: Missing an API key
        Exception: Generic exception during key retrieval or media upload process
        Exception: Status Code unknown
        e: Exception during key retrieval or media upload process

    Returns:
        str: Job ID of the redaction job
    """

    try:
        with open(f"./files/{FILENAME}", "rb") as file:  # Path to file
            _transcript = json.load(file)

        upload_key_endpoint:str = f"{API_URL}/redact"

        # Call to get upload key
        upload_key_json_body = {
            "entities": ENTITIES,
            "callbackUrl": CALLBACK,
            "transcript": _transcript,
            "language": LANGUAGE,
        }
        # Header object
        headers = {"x-api-key": API_KEY}

        upload_key_response = requests.post(
            upload_key_endpoint, json=upload_key_json_body, headers=headers
        )
        if upload_key_response.status_code != "":
            if upload_key_response.status_code == 200:
                upload_key_json = json.loads(upload_key_response.text)
                if "jobId" in upload_key_json:
                    return upload_key_json.get('jobId', "Unknown")
                else:
                    raise Exception("Missing job ID")
            elif upload_key_response.status_code == 403:
                raise Exception("Need API key - Forbidden")
            else:
                text:str = upload_key_response.text
                raise Exception(text)
        else:
            raise Exception("Status Code unknown")
    except Exception as e:
        raise e


if __name__ == "__main__":
    try:
        print("sent. waiting for response...")
        job_id: str = send_media()
        print(f"job id: {job_id}")
        print("done")
    except Exception as e:
        print(e)
        print("failed")
