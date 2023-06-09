import requests
import time

API_KEY = "API_KEY"
API_URL = "https://yp1ypp2boj.execute-api.us-east-2.amazonaws.com/prod"

# Send media to begin redaction process
def send_media():
    """ Sends media to Ontelio's Redaction Engine. Input parameters in the form of json body.
    See code comments for explanation of each json key.

    Raises:
        e: Generic exception during key retrieval or media upload process.
    """

    upload_key_endpoint = f"{API_URL}/redact/media"
    # Call to get upload key
    upload_key_json_body = {
        "filename": "preamble.wav",  # Name of file to be redacted
        "callbackUrl": "http://test.io/",  # Callback URL to receive redacted transcript
        "language": "en-US",  # Language that is being redacted in the transcript
        "transcriptType": "VOCI",  # Type of transcript
        "enableTranscriptRedaction": True,  # Toggle transcript redaction
        "enableMediaRedaction": True,  # Toggle media file redaction
        "entities": ["PERSON", "LOCATION"]  # Types of entities to be redacted
    }
    # Header object
    headers = {
        "x-api-key": API_KEY
    }

    try:
        upload_key_response = requests.post(upload_key_endpoint, json=upload_key_json_body, headers=headers)
        upload_key_json = upload_key_response.json()
        if 'message' in upload_key_json:
            if upload_key_json['message'] == "Forbidden":
                raise Exception('Need API key - Forbidden')
    except Exception as e:
        raise e

    # Call to upload media
    if "jobId" in upload_key_json and "uploadUrl" in upload_key_json:
        job_id = upload_key_json["jobId"]
        upload_url = upload_key_json["uploadUrl"]

        try:
            with open("./files/preamble.wav", 'rb') as file:  # Path to file
                requests.put(upload_url, data=file)
        except Exception as e:
            raise e

        poll_status(job_id=job_id)


def poll_status(job_id = None):
    """ Polls job status until the redaction process is completed.
    Args:
        job_id (int): The job ID of the job you are getting the status of.
    Raises:
        e: Error while getting redaction status
    """
    status_endpoint = f"{API_URL}/job/{job_id}"
    start = time.time()
    headers = {
        "x-api-key": API_KEY
    }

    try:
        print('Checking the status of the job.')
        response = requests.get(status_endpoint, headers=headers)
        response_json = response.json()
        if response_json and response_json["status"] == "ERROR":
            print("Error in redaction process")
            return
        if response_json and response_json["status"] != "COMPLETED":
            print(f'The current status of the job is {response_json["status"]}')
            time.sleep(1.0 - ((time.time() - start) % 1.0))
            poll_status(job_id=job_id)
        else:
            print(response_json["transcript"])
    except Exception as e:
        raise e


if __name__ == '__main__':
    send_media()

