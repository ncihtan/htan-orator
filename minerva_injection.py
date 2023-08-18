import urllib.request
import json
import orator
import re
import boto3
import sys
import requests
from bs4 import BeautifulSoup

session = boto3.session.Session(profile_name="tower")
s3 = session.resource("s3")


exhibit_key = sys.argv[1] + "exhibit.json"
index_key = sys.argv[1] + "index.html"
bucket = "htan-project-tower-bucket"

exhibit_s3object = s3.Object(bucket, exhibit_key)
exhibit = exhibit_s3object.get()["Body"].read()
exhibit = json.loads(exhibit.decode("UTF-8"))


index_s3object = s3.Object(bucket, index_key)
index = index_s3object.get()["Body"].read().decode("UTF-8")

# print(index)

synid = re.match(r".+(syn\d+).+", exhibit_key).group(1)

oration = orator.orate_miti(synid)

print(oration)

oration_ready = (
    oration.replace("\n", "\\n")
    .replace("False", "false")
    .replace("'", '"')
    .replace("_", "\_")
)

new_exhibit = exhibit
new_exhibit["Header"] = oration_ready

new_index = re.sub(r"exhibit: \{.+\}", "exhibit: " + str(new_exhibit), index)

# exhibit_s3object = s3.Object(bucket, sys.argv[1] + "exhibit2.json")
# index_s3object = s3.Object(bucket, sys.argv[1] + "index2.html")

exhibit_s3object.put(Body=(bytes(json.dumps(new_exhibit).encode("UTF-8"))))

index_s3object.put(Body=(bytes(new_index.encode("UTF-8"))))
