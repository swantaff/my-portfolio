import boto3
import botocore.client 
import configparser
import StringIO
import zipfile
import mimetypes

s3 =boto3.resource('s3', config=configparser(signature_version='s3v4')

portfolio_bucket = s3.Bucket(portfolio.markjones.info)
build_bucket= s3.Bucket(portfoliobuild.markjones.info)

portfolio_zip = StringIO.StringIO()

build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')