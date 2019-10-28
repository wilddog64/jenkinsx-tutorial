import requests
import sys
import time

projectId = "ADD YOUR PROJECT ID"
jobId = "ADD YOUR JOB ID"
apiKey = "ADD YOUR API KEY"
agentId = "ADD YOUR AGENT ID"
apiUrl = "https://api.testproject.io/"
url = apiUrl + 'v2/projects/' + projectId + '/jobs/' + jobId + '/run'

headers = {
    "accept": "application/json",
    "Authorization": apiKey,
    "Content-Type": "application/json"
}
body = {
    "agentId": agentId,
    "browsers": [
        "Chrome"
    ],
    "queue": True
}

executionId = requests.post(url, json=body, headers=headers).json()["id"]

url = apiUrl + 'v2/projects/' + projectId + '/jobs/' + jobId + '/executions/'+ executionId + '/state'

headers = {
    "accept": "application/json",
    "Authorization": apiKey,
}

executionState = requests.get(url, headers=headers).json()["state"]

count = 0
while count < 10:
    executionState = requests.get(url, headers=headers).json()["state"]
    print(executionState)
    if executionState == 'Passed':
        exit(1)
    time.sleep(2)
    count += 1
exit(0)