from resume_generator.pdf_generator import PDFGenerator
import os

def main():
    # Create templates directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    
    # Create a sample template
    sample_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }
            .header {
                color: #333;
                border-bottom: 2px solid #333;
                margin-bottom: 20px;
            }
            .content {
                margin: 20px 0;
            }
            .footer {
                margin-top: 30px;
                font-size: 0.9em;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{{ title }}</h1>
            <p>Generated on: {{ date }}</p>
        </div>
        
        <div class="content">
            <h2>{{ section_title }}</h2>
            <p>{{ content }}</p>
            
            {% if items %}
            <ul>
                {% for item in items %}
                <li>{{ item }}</li>
                {% endfor %}
            </ul>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>Created using PDFGenerator</p>
        </div>
    </body>
    </html>
    """
    
    # Save the template
    with open("templates/sample.html", "w", encoding="utf-8") as f:
        f.write(sample_template)
    
    # Initialize the PDF generator with templates directory
    generator = PDFGenerator(template_dirs=["templates"])
    
    # Prepare sample data
    from datetime import datetime
    variables = {
        "title": "Sample PDF Document",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "section_title": "Test Section",
        "content": "This is a sample PDF generated using our PDFGenerator class. It demonstrates template rendering with various types of content.",
        "items": [
            "First sample item",
            "Second sample item",
            "Third sample item with some longer text to demonstrate wrapping"
        ]
    }
    
    # Generate PDF with default options
    pdf_path = generator.generate_pdf(
        template_name="sample.html",
        variables=variables,
        output_path="sample_output.pdf"
    )
    print(f"PDF generated at: {pdf_path}")
    
    # Generate another PDF with custom options
    custom_pdf_path = generator.generate_pdf(
        template_name="sample.html",
        variables=variables,
        output_path="sample_output_custom.pdf",
        pdf_options={
            'page-size': 'Letter',
            'margin-top': '1in',
            'margin-right': '1in',
            'margin-bottom': '1in',
            'margin-left': '1in',
            'encoding': 'UTF-8'
        }
    )
    print(f"Custom PDF generated at: {custom_pdf_path}")
    
    # Demonstrate HTML preview
    html_content = generator.render_html(
        template_name="sample.html",
        variables=variables
    )
    print("\nHTML Preview (first 200 characters):")
    print(html_content[:200] + "...")

if __name__ == "__main__":
    main() 