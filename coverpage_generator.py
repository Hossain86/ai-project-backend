from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docxtpl import DocxTemplate

def replace_placeholder_in_paragraph(paragraph, cover_data):
    """
    Replaces placeholders in a paragraph by joining all runs,
    performing the replacement, and then rebuilding the paragraph.
    Note: This approach may lose detailed formatting across runs.
    """
    # Reconstruct the full text from all runs.
    full_text = "".join(run.text for run in paragraph.runs)
    original_text = full_text  # for debugging

    # Replace all placeholders in the full text.
    for key, value in cover_data.items():
        placeholder = f"{{{key}}}"
        if placeholder in full_text:
            full_text = full_text.replace(placeholder, value)

    # If changes were made, rebuild the paragraph.
    if full_text != original_text:
        # Remove all existing runs.
        p_element = paragraph._element
        for child in list(p_element):
            p_element.remove(child)
        # Add a new run with the updated text.
        new_run = paragraph.add_run(full_text)
        # Optionally, copy formatting from the first run if it exists.
        if paragraph.runs and paragraph.runs[0].font:
            new_run.font.size = paragraph.runs[0].font.size or Pt(12)
            new_run.font.bold = paragraph.runs[0].font.bold

def generate_coverpage(cover_data, template_path="coverpage_template.docx"):
    """
    Loads a coverpage template using DocxTemplate and renders it with cover_data.
    Expected cover_data keys: department, course_code, course_name, assignment_name,
    date_of_submission, submitted_by_name, submitted_by_roll, submitted_by_section,
    submitted_by_series, submitted_to.
    """
    doc = DocxTemplate(template_path)
    doc.render(cover_data)
    return doc