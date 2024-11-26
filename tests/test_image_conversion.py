from sync_workbench import convertor,workbench
import tempfile
import os
import unittest

class TestConversion(unittest.TestCase):

    #def setUp(self):

    def test_conversion(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            imagesDir = os.path.join(tmpdir, "iiit-test/test2")
            os.makedirs(imagesDir)

            image_url = "https://iiif-test.github.io/test2/images/IMG_8722/full/max/0/default.jpg"
            filename = workbench.download(image_url, imagesDir)
            filename = os.path.join(imagesDir, filename)
            output_filename = os.path.join(imagesDir,filename.replace(".jpg", ".ptiff"))
            convertor.convert_to_pyramidal_tiff(filename, output_filename)

            self.assertTrue(os.path.exists(output_filename),"pTiff is missing")

             # Uncomment to have a look at the files before they are deleted 
            #print (imagesDir)
            #input("Press Enter to continue...")