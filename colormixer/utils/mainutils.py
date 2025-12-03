import os, logging

def listAllFiles(directory=None):
    """
    Lists all files of a given folder
    :param directory: str
    :return: file_paths: list(str)
    """
    if not directory:
        logging.error("Directory error")
        return None
    file_paths = []
    for root, dirs, files in os.walk(directory):
        depth = root[len(directory):].count(os.sep)
        if depth < 1:
            for filename in files:
                basename, ext = os.path.splitext(filename)
                ext = ext[1:]
                file_paths.append(os.path.join(root, filename))
    return file_paths

def exr_to_jpeg(input_path, output_path):
    """
    Get Absolute path for input and output
    :param input_path: str
    :param output_path: str
    :return: output_path: OpenImageIO.OpenImageIO.ImageBuf
    """
    import OpenImageIO as oiio
    # Load Exr Image
    img = oiio.ImageBuf(input_path)

    # "Linear" -> "sRGB"
    img_srgb = oiio.ImageBufAlgo.colorconvert(
        img,
        "Linear",
        "sRGB",
        unpremult=True
    )

    # Convert to 8-bit for JPEG
    img_8 = oiio.ImageBufAlgo.copy(img_srgb, oiio.UINT8)

    # Save image to disk
    img_8.write(output_path)
    return img_8
