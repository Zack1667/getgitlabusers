# Get GitLab Users from API using Python


## Instructions on how to use

Some of the code below has been changed for brevity and also to allow you to modify if you wish to re-use:

```python
# If you have an iDP and wish to use SSO you can do so the Amazon SDK boto3, I usually create a session and then call the client and store that in a variable so it's easier, please ammend to your specified region: 

sess = boto3.Session(profile_name="YOUR SSO PROFILE", region_name="eu-west-1 OR PREFFERED REGION")
s3_client = sess.client("s3")
```

```python
# As I'm using SSM, again I can call my session and the client below or you can use secrets manager to use your access key:

ssm = sess.client("ssm")
access_token_req = ssm.get_parameter(
    Name="/pathhere/YOURACCESSTOKEN", WithDecryption=True
)
access_token = access_token_req["Parameter"]["Value"]
```

```python
# Change your bucket name accordingly
bucket_name = "your-bucket-name"
```
```python 
# Base URI of Gitlab API from our private Gitlab Instance
baseuri = "https://gitlaburlhere/api/v4" # You can find your api endpoint in gitlab.
```
```python 
# Below lines of code will need to be ammended based on the results you want:

url = f"{baseuri}/users/?per_page=100&active=true&without_project_bots=true&page={next_page}"


result = [{k: user[k] for k in ["id", "username", "name", "state"]} for user in result]

# The same in the CSV file too if you wish to ammend to rows and their names

```
```python
# If you are using boto3 to authenticate just ensure you log in first:

aws sso login --profile # after you will need to specify profile name 
```

```python
# Once you have logged in, you can simply run the .py file
```
