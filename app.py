import boto3
import os
from crypt import methods
from dotenv import load_dotenv
from flask import Flask
from flask import redirect, render_template, request
from unicodedata import name

app = Flask(__name__)
s3_bucket = 'hotdog-app-bucket'
upload_folder = 'uploads'
access_key_id = os.getenv('aws_access_key_id')
secret_access_key = os.getenv('aws_secret_access_key')

def configure():
    load_dotenv()
    
@app.route('/',methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def classify():
    image = request.files['imagefile']
    image.save(os.path.join(upload_folder, image.filename))
    upload_file(f"uploads/{image.filename}", s3_bucket)
    return render_template('home.html')

def upload_file(file_name, bucket):
    """
    Function to upload submitted image to S3 bucket
    """
    object_name = file_name
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    response = s3_client.upload_file(file_name, bucket, object_name)
    return True

def list_files(bucket):
    """
    Function to list files in a given S3 bucket
    """
    s3_client = boto3.client('s3', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    contents = []
    for item in s3_client.list_objects(Bucket=bucket)['Contents']:
        contents.append(item)
    return contents

if __name__ == '__main__':
    configure()
    app.run(port=5000)
