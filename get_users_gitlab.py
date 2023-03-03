import boto3
import json
import requests
import botocore
from botocore.exceptions import ClientError
from datetime import date, time 
import csv 


# Using datetime module setting UK Date  
now = date.today()
uk_date = now.strftime("%d-%m-%Y")

# Using AWS SDK Boto3 to create a session for SSO, however you can use IAM if you prefer: 
# Boto3 Components:
sess = boto3.Session(profile_name="YOUR SSO PROFILE", region_name="eu-west-1 OR PREFFERED REGION")
s3_client = sess.client("s3")


# The Bucket Name you want to upload to in S3: 
bucket_name = "gitlab-users"

# If you have an access token it's best to grab this from somewhere secure, this could even be secrets manager, Here I'm using SSM.
# Boto3 SSM to grab access_token from AWS SSM
ssm = sess.client("ssm")
access_token_req = ssm.get_parameter(
    Name="/service/gitlab/MYACCESSTOKEN", WithDecryption=True
)
access_token = access_token_req["Parameter"]["Value"]

# Base URI of Gitlab API from our private Gitlab Instance
baseuri = "BASEURL OF YOUR PRIVATE GITLAB INSTANCE"

# Function to grab users and put objects in S3 bucket, this will also paginate each page with max results 100, this includes without project bots, so only active users.
# Feel free to ammend the URL to fit your needs, you can even add more if you an Admin: 

def get_gitlab_users(access_token=access_token, baseuri=baseuri):
    next_page = 1
    result = []
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(access_token),
    }
    # while loop to add the JSON data to users variable and paginate, this will also grab "id", "username", "state"
    while True:
        url = f"{baseuri}/users/?per_page=100&active=true&without_project_bots=true&page={next_page}"
        req = requests.get(url, headers=headers)
        users = req.json()
        if users:
            result.extend(users)
            next_page += 1
        else:
            break
    result = [{k: user[k] for k in ["id", "username", "name", "state"]} for user in result]

   # Write to a CSV file, also adds the UK Date at the end of the CSV so you can keep records of users and track growth etc: 
    with open(f"GitLab_Users-{uk_date}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "username", "name", "state"])
        for user in result:
            writer.writerow([user[k] for k in ["id", "username", "name", "state"]])

    # Upload the CSV file to S3
    with open(f"GitLab_Users-{uk_date}.csv", "rb") as f:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"GitLab_Users-{uk_date}.csv",
            Body=f.read()
        )

# Mainly to test locally first if you wish:
if __name__ == "__main__":
    get_gitlab_users(access_token=access_token, baseuri=baseuri)
