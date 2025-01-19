import requests

API_KEY = "<INSERT API KEY>"
API_URL = "https://api.censori.ontelio.ai"
MEDIA_FILE = "preamble.wav" # Name of file to be redacted
LANGUAGE = "en" # if no language is specified, the default is auto
DIARIZE = True # if diarize is set to True, the engine will attempt to separate speakers
CALLBACK = "<INSERT CALLBACK URL>"

# Send media to begin redaction process

def send_media() -> str:
    """
    Sends media to the transcription service and returns the job ID.

    Returns:
        str: The job ID of the transcription job.
    """
    upload_key_endpoint = f"{API_URL}/transcribe"
    # Call to get upload key
    upload_key_json_body = {
        "filename": MEDIA_FILE,  # Name of file to be redacted
        "language": LANGUAGE,
        "callbackUrl": CALLBACK,
        "diarize": DIARIZE,
    }
    # Header object
    headers = {"x-api-key": API_KEY}

    try:
        upload_key_response = requests.post(
            upload_key_endpoint, json=upload_key_json_body, headers=headers
        )
        upload_key_json = upload_key_response.json()
        if "message" in upload_key_json:
            if upload_key_json["message"] == "Forbidden":
                raise Exception("Need API key - Forbidden")

        # Call to upload media
        if "jobId" in upload_key_json and "uploadUrl" in upload_key_json:
            job_id = upload_key_json["jobId"]
            upload_url = upload_key_json["uploadUrl"]

            # Path to file
            with open(f"./files/{MEDIA_FILE}", "rb") as file:
                requests.put(upload_url, data=file)
            
            return job_id
        else:
            raise Exception("Missing job ID or upload URL")
    except Exception as e:
        print(e)
        raise e

if __name__ == "__main__":
    print("sent. waiting for response...")
    job_id:str = send_media()
    print(f"job id: {job_id}")
