import requests
import time


def send_media():
    upload_key_endpoint = "https://yp1ypp2boj.execute-api.us-east-2.amazonaws.com/prod/redact/media"
    api_key = "hv07nvAeWJ3qvv9C6HPkI6l6NEIqb1T9aWk1uBYZ"
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

    # deal with return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    send_media()

