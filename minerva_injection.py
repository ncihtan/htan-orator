import urllib.request
import json
import orator
import re
import boto3
import sys

cloudfront_prefix = "https://d3p249wtgzkn5u.cloudfront.net/"

exhibit_url = sys.argv[1]

synid = re.match(r".+(syn\d+).+", exhibit_url).group(1)

with urllib.request.urlopen(exhibit_url) as url:
    exhibit = json.load(url)

description = exhibit["Stories"][0]["Description"]

print(description)

oration = orator.orate_miti(synid)

oration_ready = oration

new_exhibit = exhibit
new_exhibit["Header"] = oration_ready

print(new_exhibit)

import boto3

session = boto3.session.Session(profile_name="htan-dev")
s3 = session.resource("s3")

key = exhibit_url.replace(cloudfront_prefix, "")
bucket = "htan-assets"

s3object = s3.Object(bucket, key)

print(key)

s3object.put(
    Body=(bytes(json.dumps(new_exhibit).encode("UTF-8"))),
    Metadata={"Cache-Control": "max-age=60"},
)
