import requests
from iiif_prezi3 import Manifest
import json
import os

def name_from_image(url):
    """
        Extract image name from Github URL
    """
    splitUrl = url.split("/")
    return splitUrl[5]

def images(repo):
    """
        Retrieve Manifest.json and get links to full image
    """
    (user,repo) = repo.split("/")
    # URL of the JSON data
    url = f"https://{user}.github.io/{repo}/images/manifest.json"

    urls = []
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        # Raise an exception for HTTP errors
        response.raise_for_status()
        # Parse the JSON content
        data = response.json()  # Automatically parses JSON into a Python dictionary or list
        manifest = Manifest(**data)

        for canvas in manifest.items:
            for annotationPage in canvas.items:
                for annotation in annotationPage.items:
                    service = annotation.body.service[0]
                    id = service.id
                    if service.type == "ImageService2":
                        size = "full"
                    else:
                        size = "max"
                    urls.append(f"{id}/full/{size}/0/default.jpg")        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return urls    

def download(url, targetDir):
    filename = f"{name_from_image(url)}.jpg"
    try:
        # Send a GET request to fetch the image
        response = requests.get(url)
        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Write the image data to a file
        with open(os.path.join(targetDir, filename), "wb") as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return filename    