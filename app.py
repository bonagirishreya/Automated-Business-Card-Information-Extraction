from flask import Flask, request, render_template, jsonify
import pytesseract
from PIL import Image
import requests

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Define your API endpoint URL and access token as constants
API_URL = 'https://next.levity.ai/api/ai/v2/50d4e5b4-1291-485c-bad0-cca9d133e90d/generate'  # Replace with your model ID
ACCESS_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImJvbmFnaXJpc2hyZXlhNjAxQGdtYWlsLmNvbSIsImxldml0eVVzZXJJZCI6Ijc2NTc5MzZmLTQyOGYtNGNhYS1iOTg0LWI3OGFkMTRiM2ZjMiIsImxldml0eVdvcmtzcGFjZUlkIjoiNmEzMTliOTAtYmY1Mi00NmM4LTg4ZjItOGE2OWM4NDAzMmYyIiwiaXNzIjoiTGV2aXR5OjIifQ.ajlMc5sr3XzWFzZSn1sLM2Ynh_0Fi7B5XaTVC30QObm8HHRwTgHYmhvyh_lblw1PVp8FTLBJGDgbnUgSPoYJBsv2dtqwcPsOtaDfcyOvr71X5rix5wzdIdgEBl2AnfqLgVYqUDl_QssIJXBf1Av1y3SzXueZbh3WKctF6N5ojC_2_mY68BJPOkp2QjxcXlhI9j3TGbKdG0weMoF2kS8M7IgN8OCa6OI9EvSDJjjBULM3-myy26RgT8xUQTDFA9KxsukgnvoK3JFsA3UgPdwbNQuqcHxj7Kfj92to9FQXXacprM_z025ybpbzzC8mvoYNX7d8-vJnfU-vU6nvM_yQQg'  # Replace with your actual access token

# Create a function for processing an image and sending it to the API
def process_and_send_image(image):
    # Convert the image to monochromatic (black and white)
    image = Image.open(image)
    image = image.convert('L')

    # Use pytesseract to do OCR on the monochromatic image
    text = pytesseract.image_to_string(image)

    # Define the JSON payload with the extracted text
    payload = {
        "text": text
    }

    # Define the headers with the Authorization token and content type
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Make the API request and receive the JSON response
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()  # Get the entire JSON response

        name = data.get("Name", "")
        contact = data.get("Contact", "")
        email = data.get("Email", "")
        

        extracted_data = {
            "name": name,
            "contact": contact,
            "email": email
        }
        return extracted_data
    else:
        return None

# Route for the main page
@app.route('/')
def index():
    return render_template('ocr.html')

# Route for processing an uploaded image and returning the result as JSON
@app.route('/process_image', methods=['POST'])
def process_image():
    image = request.files['image']

    if image:
        extracted_data = process_and_send_image(image)
        if extracted_data:
            return jsonify(extracted_data)
        else:
            return 'Failed to send text to the API', 500
        

if __name__ == '__main__':
    app.run(debug=True)