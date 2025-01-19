import requests
from datetime import datetime
import json

# API_KEY = "QWT6MNRtbK1hDEySneLHGuHMr44M4vP91q1EXh7a"
API_KEY = "u3Z8kJFHYL4FberYCkeRf6MzcLCFUaFu9L88HAV7"
API_URL = "https://api.censori.dev.ontelio.ai"
FILENAME = "hubspot_example_1.json"
LANGUAGE = "en"
ENTITIES = []
CALLBACK = "https://webhook-test.com/e6a068b405863d7023fce5fe85ca4296"

start_time = datetime.now()
COUNT = 0

# Send media to begin redaction process


def send_media(count=None):
    """Sends media to Ontelio's Redaction Engine. Input parameters in the form of json body.
    See code comments for explanation of each json key.

    Raises:
        e: Generic exception during key retrieval or media upload process.
    """

    # open json file
    try:
        with open(f"./files/redact/{FILENAME}", "rb") as file:  # Path to file
            _transcript = json.load(file)
    except Exception as e:
        raise e

    # _transcript = '{'

    upload_key_endpoint = f"{API_URL}/redact"
    # Call to get upload key
    upload_key_json_body = {
        "entities": ENTITIES,
        "callbackUrl": CALLBACK,
        "transcript": _transcript,
        "language": LANGUAGE,
    }
    # Header object
    headers = {"x-api-key": API_KEY}

    try:
        upload_key_response = requests.post(
            upload_key_endpoint, json=upload_key_json_body, headers=headers
        )
        if upload_key_response.status_code != "":
            if upload_key_response.status_code == 403:
                print("Need API key - Forbidden.")
                return 403
            if upload_key_response.status_code == 500:
                upload_key_json = json.loads(upload_key_response.text)
                print(upload_key_json["error"])
                return 500
            if upload_key_response.status_code == 200:
                upload_key_json = json.loads(upload_key_response.text)
                if "results" in upload_key_json:
                    if "channels" in upload_key_json["results"]:
                        print(
                            upload_key_json["results"]["channels"][0]["alternatives"][
                                0
                            ]["transcript"]
                        )
                    else:
                        print(
                            upload_key_json["results"]["transcripts"][0]["transcript"]
                        )
                else:
                    print(upload_key_json)
                return 200
            if upload_key_response.status_code == 409:
                upload_key_json = json.loads(upload_key_response.text)
                print(upload_key_json["error"])
                return 409
        else:
            print("dont know.")
    except Exception as e:
        print(e)
        raise e

    # # Call to upload media
    # if "jobId" in upload_key_json and "uploadUrl" in upload_key_json:
    #     job_id = upload_key_json["jobId"]
    #     upload_url = upload_key_json["uploadUrl"]

    #     try:
    #         with open(f"./files/{FILENAME}", 'rb') as file:  # Path to file
    #             requests.put(upload_url, data=file)
    #     except Exception as e:
    #         raise e

    #     ##poll_status(job_id=job_id)


# def poll_status(job_id = None):
#     """ Polls job status until the redaction process is completed.
#     Args:
#         job_id (int): The job ID of the job you are getting the status of.
#     Raises:
#         e: Error while getting redaction status
#     """
#     status_endpoint = f"{API_URL}/job/{job_id}"
#     start = time.time()
#     headers = {
#         "x-api-key": API_KEY
#     }

#     try:
#         print('Checking the status of the job.')
#         response = requests.get(status_endpoint, headers=headers)
#         response_json = response.json()
#         if response_json and response_json["status"] == "ERROR":
#             print("Error in redaction process")
#             return
#         if response_json and response_json["status"] != "COMPLETED":
#             print(f'The current status of the job is {response_json["status"]}')
#             time.sleep(1.0 - ((time.time() - start) % 1.0))
#             poll_status(job_id=job_id)
#         else:
#             _time_delta = datetime.now() - start_time
#             current_time = _time_delta.strftime("%H:%M:%S")
#             #print(response_json["transcript"])
#             print(f'current count is {COUNT}, current time since is {current_time}')
#     except Exception as e:
#         raise e

# def forever():
#     while(1):
#         time.sleep(5)
#         send_media()

if __name__ == "__main__":
    _i = 1
    while _i > 0:
        send_media()
        _i = _i - 1
    # COUNT = 0
    # while(1):
    #     status = send_media()
    #     if (status == 200):
    #         COUNT = COUNT + 1
    #         _time_delta = datetime.now() - start_time
    #         print(f'current count is {COUNT}, current time since is {_time_delta}')
