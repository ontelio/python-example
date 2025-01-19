import requests
import json

# API_KEY = "QWT6MNRtbK1hDEySneLHGuHMr44M4vP91q1EXh7a"
API_KEY = "u3Z8kJFHYL4FberYCkeRf6MzcLCFUaFu9L88HAV7"
API_URL = "https://api.censori.ontelio.ai"
FILENAME = "preamble.json"
LANGUAGE = "en"
ENTITIES = []
# ENTITIES = ["PERSON", "LOCATION"]
CALLBACK = "https://webhook-test.com/e6a068b405863d7023fce5fe85ca4296"


def send_media() -> str:
    # open json file
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
                upload_key_json = json.loads(upload_key_response.text)
                raise Exception(upload_key_json["error"])
        else:
            raise Exception("Status Code unknown")
    except Exception as e:
        print(e)
        raise e


if __name__ == "__main__":
    print("sent. waiting for response...")
    job_id: str = send_media()
    print(f"job id: {job_id}")
    print("done")
