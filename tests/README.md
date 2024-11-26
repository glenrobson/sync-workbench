# sync-workbench

Allows the download of Workbench images, converting to pTiff and upload to s3 for use with serverless-iiif


## Testing

Unit tests are in the `tests` folder and can be run with:
```
python -m unittest discover -s tests
```

Run single test:
```
python -m unittest tests.test_image_download.TestImages.test_image_download
```
