import asyncio
import os
from uuid import uuid4

import boto3
from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name="eu-north-1",
    endpoint_url="https://s3.eu-north-1.amazonaws.com",
)
BUCKET = "nt-sn03-bucket"


@app.post("/api/upload")
async def upload_file(image: UploadFile):
    key = f"test/{uuid4()}.pdf"

    image.file.seek(0)

    loop = asyncio.get_running_loop()

    await loop.run_in_executor(
        None,
        lambda: s3.upload_fileobj(
            image.file,
            BUCKET,
            key,
            ExtraArgs={
                "ContentType": image.content_type,
                "ContentDisposition": "inline",
            },
        ),
    )

    url = s3.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=3600
    )

    return {"key": key, "url": url}
