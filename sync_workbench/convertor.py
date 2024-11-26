import pyvips

def convert_to_pyramidal_tiff(input_image_path, output_tiff_path):
    # Load the image using pyvips
    image = pyvips.Image.new_from_file(input_image_path, access="sequential")

    # Save as a pyramidal TIFF
    image.tiffsave(
        output_tiff_path,
        compression="jpeg",
        Q=90,
        tile=True,
        pyramid=True,
        tile_width=256,
        tile_height=256
    )