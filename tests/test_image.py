from pathlib import Path
from PIL import Image
import pytest

from src.converter.image import convert_image


def test_convert_png_to_jpeg(tmp_path: Path) -> None:
    # Arrange
    input_path = tmp_path / "sample.png"
    image = Image.new("RGB", (10, 10), color="red")
    image.save(input_path)

    # Act
    output_path = convert_image(input_path, "jpeg")

    # Assert
    assert output_path.exists()
    assert output_path.suffix == ".jpg"
    with Image.open(output_path) as result:
        assert result.format == "JPEG"

def test_unsupported_format(tmp_path:Path) -> None:
    input_path = tmp_path / 'sample.png'
    with pytest.raises(ValueError):
        convert_image(input_path, 'ttt')

def test_rgba(tmp_path:Path):
    input_path=tmp_path/'transparent.png'
    image=Image.new('RGBA',(10,10), color=(255, 0, 0, 128))
    image.save(input_path)

    output_path = convert_image(input_path, 'jpeg')

    with Image.open(output_path) as result:
        assert result.mode =='RGB'