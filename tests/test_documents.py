from pathlib import Path

from pypdf import PdfReader

from src.converter.documents import pdf_to_txt, txt_to_pdf


def test_txt_to_pdf_empty_file(tmp_path: Path) -> None:
    # Arrange
    input_path = tmp_path / "empty.txt"
    input_path.write_text("", encoding="utf-8")

    # Act
    output_path = txt_to_pdf(input_path)

    # Assert
    assert output_path.exists()
    reader = PdfReader(str(output_path))
    assert len(reader.pages) == 1


def test_pdf_to_txt_extracts_cyrillic_text(tmp_path: Path) -> None:
    # Arrange
    txt_path = tmp_path / "note.txt"
    txt_path.write_text("Привет, мир!", encoding="utf-8")
    pdf_path = txt_to_pdf(txt_path)

    # Act
    result_path = pdf_to_txt(pdf_path)

    # Assert
    extracted = result_path.read_text(encoding="utf-8")
    assert "Привет" in extracted