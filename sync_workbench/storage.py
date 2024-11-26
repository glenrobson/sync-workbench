import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

def upload_file(file_name, bucket_name, object_name=None, mime_type="image/tiff", public=False):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket_name: Bucket to upload to
    :param object_name: S3 object name. If not specified, file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket_name, object_name, ExtraArgs={'ContentType': mime_type})
        print(f"File {file_name} uploaded to bucket {bucket_name} as {object_name}")

        if public:
            s3_client.put_object_acl(
                Bucket=bucket_name,
                Key=object_name,
                ACL='public-read'
            )
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
        return False
    except NoCredentialsError:
        print("Credentials not available.")
        return False
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return False

def upload_string_to_s3(bucket_name, object_name, content, mime_type="text/html"):
    """
    Upload a string as an object to an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param object_name: Key name for the object in the bucket
    :param content: The string content to upload
    :return: None
    """
    s3_client = boto3.client('s3')

    try:
        # Upload the string content
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=content, ContentType=mime_type)
        s3_client.put_object_acl(
            Bucket=bucket_name,
            Key=object_name,
            ACL='public-read'
        )
    except Exception as e:
        print(f"Error uploading string to S3: {e}")


def exists(bucket, filename):
    """
    Check if a file exists in an S3 bucket.

    :param bucket: Name of the S3 bucket
    :param filename: Key of the file to check
    :return: True if the file exists, False otherwise
    """
    s3_client = boto3.client('s3')
    try:
        s3_client.head_object(Bucket=bucket, Key=filename)
        return True
    except ClientError as e:
        # If the error is a 404, the file does not exist
        if e.response['Error']['Code'] == "404":
            return False
        else:
            # Something else went wrong, raise the exception
            raise

def infoJsonURL(filename):
    filename = filename.replace(".tif", "").replace("/", "%2F")
    return f"https://iiif.gdmrdigital.com/image/iiif/2/{filename}/info.json"


def create_invalidation(distribution_id, paths):
    """
    Create a CloudFront invalidation for specific paths.

    :param distribution_id: The ID of the CloudFront distribution
    :param paths: List of paths to invalidate (e.g., ['/index.html', '/images/*'])
    :return: None
    """
    client = boto3.client('cloudfront')

    try:
        response = client.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': len(paths),
                    'Items': paths
                },
                'CallerReference': str(hash(frozenset(paths)))  # Unique reference
            }
        )
        invalidation_id = response['Invalidation']['Id']
        print(f"Invalidation created with ID: {response['Invalidation']['Id']}")
        # Wait for the invalidation to complete
        waiter = client.get_waiter('invalidation_completed')
        print("Waiting for invalidation to complete...")
        waiter.wait(
            DistributionId=distribution_id,
            Id=invalidation_id
        )
        print("Invalidation completed.")
    except ClientError as e:
        print(f"Error creating invalidation: {e}")