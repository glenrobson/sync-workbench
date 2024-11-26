# Sync Workbench images with s3

This project downloads a list of images held in a [IIIF Workbench](https://workbench.gdmrdigital.com/), converts them to Pyramid tiff and uploads them to S3 for access by [serverless iiif](https://samvera.github.io/serverless-iiif/). 

```
usage: main.py [-h] [--image-path IMAGE_PATH] [--webpage-path WEBPAGE_PATH] [--repo-list REPO_LIST] [--webpage-url WEBPAGE_URL] image_bucket webpage_bucket cloudfront

Upload Github workbench images to s3

positional arguments:
  image_bucket          Bucket for storing ptif files
  webpage_bucket        Bucket for storing html pages
  cloudfront            Distribution ID for Cloudfront instance

options:
  -h, --help            show this help message and exit
  --image-path IMAGE_PATH
                        location for storing the images
  --webpage-path WEBPAGE_PATH
                        location for storing the images
  --repo-list REPO_LIST
                        Text file containing user/repo for each workbench project
  --webpage-url WEBPAGE_URL
                        Base URL to webpage files
```

The Repo list is a text file that looks like the following:

```
github_user/githup_repo
iiif-test/test2
iiif-test/Places
```