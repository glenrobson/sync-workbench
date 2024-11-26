import unittest
import os
import tempfile
from sync_workbench import workbench

class TestImages(unittest.TestCase):

    #def setUp(self):

    def test_image_download(self):
        repo = "iiif-test/test2"

        images = workbench.images(repo)
        self.assertEqual(len(images),13, f"Expected 13 images from {repo}")
        self.assertTrue("https://iiif-test.github.io/test2/images/IMG_8722/full/max/0/default.jpg" in images, f"Failed to find expected image in {images}" )
        self.assertTrue("https://iiif-test.github.io/test2/images/IMG_8664/full/full/0/default.jpg" in images, f"Failed to find expected image in {images}" )

    def test_name_from_url(self):
        name = workbench.name_from_image("https://iiif-test.github.io/test2/images/IMG_8722/full/max/0/default.jpg")    
        self.assertEqual("IMG_8722", name, "Expected the image to be called IMG_8722")

        name = workbench.name_from_image("https://iiif-test.github.io/test2/images/IMG_8664/full/full/0/default.jpg")    
        self.assertEqual("IMG_8664", name, "Expected the image to be called IMG_8664")

    def test_download(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            imagesDir = os.path.join(tmpdir, "iiit-test/test2")
            os.makedirs(imagesDir)

            workbench.download("https://iiif-test.github.io/test2/images/IMG_8722/full/max/0/default.jpg", imagesDir)
            self.assertTrue(os.path.exists(os.path.join(imagesDir,"IMG_8722.jpg")),"Image file is missing")
            workbench.download("https://iiif-test.github.io/test2/images/IMG_8664/full/full/0/default.jpg", imagesDir)
            self.assertTrue(os.path.exists(os.path.join(imagesDir,"IMG_8664.jpg")),"Image file is missing")

           # Uncomment to have a look at the files before they are deleted 
           # print (imagesDir)
           # input("Press Enter to continue...")