from sync_workbench import workbench, convertor, storage
import tempfile
import os
from jinja2 import Environment, FileSystemLoader
import argparse

TEST=False

def run(image_bucket, webpage_bucket, image_path, webpage_path, repo_list, webpage_url, cloudfront):
    projects = []
    # upload json
    target = f"{webpage_path}/js"
    for filename in os.listdir("js"):
        source = os.path.join("js",filename)
        dest = os.path.join(target, filename)
        if not storage.exists(webpage_bucket, dest):
            mime=None
            if filename.endswith(".js"):
                mime = "application/javascript"
            if filename.endswith(".css"):
                mime = "text/css"

            if not TEST:
                print (f"Uploading {dest}")
                storage.upload_file(source, webpage_bucket, dest, mime_type=mime, public=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        with open(repo_list, "r") as file:
            for line in file:
                repoUser = line.strip()
                print (f"Looking for {repoUser}")
                imagesDir = os.path.join(tmpdir, repoUser)
                os.makedirs(imagesDir)

                images = workbench.images(repoUser)
                print (f"Found {len(images)} images")

                infoJsons = {}
                for image in images:
                    id = workbench.name_from_image(image)
                    dest = f"{image_path}/{repoUser}/{id}.tif"
                    # check if image already exists
                    if storage.exists(image_bucket, dest):
                        infoJsonURL = storage.infoJsonURL(dest)
                        infoJsons[id] = infoJsonURL
                        print (f"Image {image} exists at {infoJsonURL}")
                    else:    
                        # Download image to local temporary dir 
                        print (f"Downloading {image}")
                        filename = os.path.join(imagesDir, workbench.download(image, imagesDir))

                        output_filename = filename.replace(".jpg", ".tif")
                        # convert to pTif
                        print (f"Converting to ptiff")
                        convertor.convert_to_pyramidal_tiff(filename, output_filename)

                        # upload to s3
                        if not TEST:
                            print (f"Uploading tif to {dest}")
                            storage.upload_file(output_filename, image_bucket, dest)
                        else:
                            print (f"If this wasn't a test I would be uploading this image to {dest}")    

                        infoJsonURL = storage.infoJsonURL(dest)

                        infoJsons[id] = infoJsonURL

                # create HTML page with links
                (user, repo) = repoUser.split("/")

                # Load the template from the 'templates' directory
                env = Environment(loader=FileSystemLoader('templates'))
                template = env.get_template('index.html')

                print (f"Creating webpage")
                html = template.render(user=user, repo=repo, infoJsons=infoJsons)

                # upload to s3
                location = os.path.join(webpage_path, repoUser, "index.html")
                if not TEST:
                    print (f"Uploading webpage to {location}")
                    storage.upload_string_to_s3(webpage_bucket, location, html)
                else:
                    print (html)    
                projects.append(f"{webpage_url}/{location}")

                image_template = env.get_template('image.html')
                for image_id in infoJsons:
                    html = image_template.render(name=image_id, infoJson=infoJsons[image_id])
                    location = os.path.join(webpage_path, repoUser, f"{image_id}.html")
                    if not TEST:
                        print (f"Uploading {location}")
                        storage.upload_string_to_s3(webpage_bucket, location, html)


    storage.create_invalidation(cloudfront,[f"/{webpage_path}/*"])
    print ("Uploaded the following projects:")        
    for project in projects:
        print (f" * {project}")

if __name__ == "__main__":
    # Initialize the ArgumentParser
    parser = argparse.ArgumentParser(description="Upload Github workbench images to s3")

    # Add arguments
    parser.add_argument("image_bucket", type=str, help="Bucket for storing ptif files")
    parser.add_argument("webpage_bucket", type=str, help="Bucket for storing html pages")
    parser.add_argument("cloudfront", type=str, help="Distribution ID for Cloudfront instance")
    parser.add_argument("--image-path", type=str,required=False, help="location for storing the images", default="training")
    parser.add_argument("--webpage-path", type=str, required=False, help="location for storing the images", default="training")
    parser.add_argument("--repo-list", type=str, required=False, help="Text file containing user/repo for each workbench project", default="data/repos.txt")
    parser.add_argument("--webpage-url", type=str, required=False, help="Base URL to webpage files", default="https://iiif.gdmrdigital.com")
    

    # Parse the command-line arguments
    args = parser.parse_args()
    run(args.image_bucket, args.webpage_bucket, args.image_path, args.webpage_path, args.repo_list, args.webpage_url, args.cloudfront)
