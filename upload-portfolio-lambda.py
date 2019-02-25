import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    
    sns = boto3.client('sns')
    
    location = {
        "bucketName": 'portfoliobuild.markjones.info',
        "objectKey": 'portfoliobuild.zip'
    }

    print(event)
    
    try:
        job = event.get("CodePipeline.job")

        print(job)

        if job:
            for artifact in job["data"] [inputArtifacts]:
                if artifact["name"] == "BuildArtifact":
                    location = artifact["location"]["s3Location"]
        
        print("Building portfolio from") + str(location)

        s3 = boto3.resource('s3')
        
        portfolio_bucket = s3.Bucket('portfolio.markjones.info')
        
        build_bucket = s3.Bucket(location["bucketName"])
        
        portfolio_zip = StringIO.StringIO()
        
        build_bucket.download_fileobj(location["objectKey"], portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm,
                    ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        
        
        print ("Job Done")
        response = sns.publish(
            TopicArn = 'arn:aws:sns:eu-west-2:793110508758:deployPortfolioTopic',
            Message='Portfolio successfully Deployed!'
            )
        if job:
            pipeline = boto3.client('codepipeline')
            pipeline.put_job_success_result(jobId=job["id"])
    except Exception, e:
        response = sns.publish(
            TopicArn = 'arn:aws:sns:eu-west-2:793110508758:deployPortfolioTopic',
            Message='Portfolio Deployment Failed!'
            )
        if job:
            pipeline = boto3.client('codepipeline')
            pipeline.put_job_failure_result(jobId=job["id"])
        raise e