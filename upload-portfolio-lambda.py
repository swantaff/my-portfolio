import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    
    sns = boto3.client('sns')
    
    try:
        s3 = boto3.resource('s3')
        
        portfolio_bucket = s3.Bucket('portfolio.markjones.info')
        build_bucket = s3.Bucket('portfoliobuild.markjones.info')
        
        portfolio_zip = StringIO.StringIO()
        
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
        
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
    except Exception, e:
        response = sns.publish(
            TopicArn = 'arn:aws:sns:eu-west-2:793110508758:deployPortfolioTopic',
            Message='Portfolio Deployment Failed!'
            )
        raise e