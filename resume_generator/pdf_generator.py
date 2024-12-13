import os
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader
import pdfkit
import tempfile


class PDFGenerator:
    """
    A general-purpose PDF generator that converts Jinja2 templates to PDF files.
    
    This class provides functionality to:
    - Load Jinja2 templates from specified directories
    - Render templates with provided variables
    - Convert rendered HTML to PDF
    """
    
    def __init__(self, template_dirs: Optional[list[str]] = None):
        """
        Initialize the PDF generator with template directories.
        
        Args:
            template_dirs (Optional[list[str]]): List of directories containing templates.
                                               If None, uses current directory.
        """
        self.template_dirs = template_dirs if template_dirs else ["."]
        self.env = Environment(loader=FileSystemLoader(self.template_dirs))
        
    def generate_pdf(
        self,
        template_name: str,
        variables: Dict[str, Any],
        output_path: Optional[str] = None,
        pdf_options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a PDF from a template with the provided variables.
        
        Args:
            template_name (str): Name of the template file
            variables (Dict[str, Any]): Dictionary of variables to render in the template
            output_path (Optional[str]): Path where the PDF should be saved.
                                       If None, generates a temporary file.
            pdf_options (Optional[Dict[str, Any]]): Options to pass to pdfkit
            
        Returns:
            str: Path to the generated PDF file
        """
        # Get the template
        template = self.env.get_template(template_name)
        
        # Render the template with variables
        html_content = template.render(**variables)
        
        # Create a temporary file for the HTML
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
            temp_html.write(html_content.encode('utf-8'))
            temp_html_path = temp_html.name
            
        try:
            # Set default PDF options if none provided
            if pdf_options is None:
                pdf_options = {
                    'page-size': 'A4',
                    'margin-top': '0.75in',
                    'margin-right': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'encoding': 'UTF-8'
                }
            
            # Generate output path if not provided
            if output_path is None:
                output_path = tempfile.mktemp(suffix='.pdf')
                
            # Convert HTML to PDF
            pdfkit.from_file(temp_html_path, output_path, options=pdf_options)
            
            return output_path
            
        finally:
            # Clean up the temporary HTML file
            os.unlink(temp_html_path)
            
    def render_html(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Render a template to HTML without converting to PDF.
        Useful for preview or debugging.
        
        Args:
            template_name (str): Name of the template file
            variables (Dict[str, Any]): Dictionary of variables to render in the template
            
        Returns:
            str: Rendered HTML content
        """
        template = self.env.get_template(template_name)
        return template.render(**variables) 