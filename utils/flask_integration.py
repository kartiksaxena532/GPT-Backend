import openai
import requests

openai.api_key = 'your-openai-api-key'

def call_flask_backend(data):
    """
    This function sends input data to the Flask backend and returns the response (the modified DOCX).
    """
    # URL of the Flask backend
    backend_url = 'https://gpt-backend-uykv.onrender.com/edit-template'

    # Send data to the backend using a POST request
    response = requests.post(backend_url, json=data)

    if response.status_code == 200:
        # If successful, return the modified document content
        return response.content
    else:
        # If there’s an error, return the error message
        return f"Error: {response.text}"

# Define the action function for GPT to use
def edit_template_action(template_name, name, patent, cutoff_date):
    """
    This action function prepares the data and calls the backend to edit the template.
    """
    data = {
        'template_name': template_name,
        'name': name,
        'patent': patent,
        'cutoff_date': cutoff_date
    }

    # Call the backend API to edit the template
    updated_file = call_flask_backend(data)

    return updated_file  # The GPT will return this updated file to the user