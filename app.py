from flask import Flask, request, send_file
from docx import Document
from utils.docx_editor import replace_placeholders
from utils.patent_scraper import scrape_google_patent
from utils.generate_concepts import generate_overview_and_concepts

import os
from datetime import datetime

app = Flask(__name__)

# Ensure output directory exists
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/upload-template', methods=['POST'])
def upload_and_edit():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    if file.filename == '':
        return 'Empty filename', 400

    if not file.filename.endswith('.docx'):
        return 'Only .docx files are supported.', 400

    try:
        doc = Document(file)
    except Exception as e:
        return f'Invalid .docx file: {str(e)}', 400

    # Base replacements
    replacements = {
        'name': request.form.get('name', 'John Doe'),
        'date': request.form.get('date', datetime.today().strftime('%d-%m-%Y')),
        'company': request.form.get('company', 'ExampleCorp'),
        'patent': request.form.get('patent', 'ExamplePatent'),
        'cutoff_date': request.form.get('cutoff_date', 'December, 12 2010'),
        'priority_date': 'N/A'
    }

    # Auto-generate overview, in-depth concept, and priority date if patent ID is provided
    patent_id = request.form.get('patent', '')
    if patent_id and patent_id != 'ExamplePatent':
        try:
            patent_data = scrape_google_patent(patent_id)
            concepts = generate_overview_and_concepts(
                patent_data['description'],
                patent_data['claims']
            )
            replacements['overview'] = concepts.get('overview', 'N/A')
            replacements['in_depth_concept'] = concepts.get('in_depth_concept', 'N/A')
            replacements['priority_date'] = patent_data.get('priority_date', 'N/A')
        except Exception as e:
            print("Patent scraping or concept generation failed:", e)
            replacements['overview'] = 'Failed to generate overview.'
            replacements['in_depth_concept'] = 'Failed to generate in-depth concept.'
            replacements['priority_date'] = 'Failed to retrieve priority date.'

    # Replace placeholders in doc
    replace_placeholders(doc, replacements)

    # Save updated document
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"first_update_{patent_id}_{timestamp}.docx"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    doc.save(output_path)

    return send_file(output_path, as_attachment=True, download_name=output_filename)

if __name__ == '__main__':
    app.run(debug=True)
