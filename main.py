import requests
import time

api_key = "hv07nvAeWJ3qvv9C6HPkI6l6NEIqb1T9aWk1uBYZ"


# send media to begin redaction process
def send_media():
    upload_key_endpoint = "https://yp1ypp2boj.execute-api.us-east-2.amazonaws.com/prod/redact/media"
    # call to get upload key
    upload_key_json_body = {
        "filename": "preamble.wav",
        "callbackUrl": "http://test.io/",
        "language": "en-US",
        "transcriptType": "VOCI"
    }
    headers = {
        "x-api-key": api_key
    }

    upload_key_response = requests.post(upload_key_endpoint, json=upload_key_json_body, headers=headers)
    upload_key_json = upload_key_response.json()

    # call to upload media
    if "jobId" in upload_key_json and "uploadUrl" in upload_key_json:
        job_id = upload_key_json["jobId"]
        upload_url = upload_key_json["uploadUrl"]

        with open("./files/preamble.wav", 'rb') as file:
            upload_file_response = requests.put(upload_url, data=file)
            # TODO: Add error handling

        # deal with return
        poll_status(job_id)


# Polls status until the redaction process is completed
def poll_status(job_id):
    status_endpoint = f"https://yp1ypp2boj.execute-api.us-east-2.amazonaws.com/prod/job/{job_id}"
    start = time.time()
    headers = {
        "x-api-key": api_key
    }
    response = requests.get(status_endpoint, headers=headers)
    response_json = response.json()
    if response_json and response_json["status"] != "COMPLETED":

        time.sleep(1.0 - ((time.time() - start) % 1.0))
        poll_status(job_id)
    else:
        print(response_json["transcript"])


if __name__ == '__main__':
    send_media()

