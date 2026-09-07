from pathlib import Path
from PIL import Image

_FORMAT_TO_EXTENSION = {
    "JPEG": ".jpg",
    "PNG": ".png",
    "GIF": ".gif",
    "BMP": ".bmp",
    "WEBP": ".webp",
}

def convert_image(input_path: Path, output_format: str)-> Path:

    output_format = output_format.upper()

    if output_format not in _FORMAT_TO_EXTENSION:
        raise ValueError(f'unsupported format:{output_format}')
    with Image.open(input_path) as image:
        if output_format=='JPEG' and image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        output_path = input_path.with_suffix(_FORMAT_TO_EXTENSION[output_format])
        image.save(output_path, format= output_format)
    return output_path