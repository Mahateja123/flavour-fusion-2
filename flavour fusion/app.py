from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import base64
import io

app = Flask(__name__)

# Set up Gemini AI API key
GEMINI_API_KEY = "AIzaSyD_OKVsSrrTsiMEZrmma3_5EF240N9bvRQ"
genai.configure(api_key=GEMINI_API_KEY)

# Function to encode image for Gemini AI
def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    word_count = request.form.get('word_count', type=int)
    dish1 = request.form.get('dish1', '').strip()
    dish2 = request.form.get('dish2', '').strip()
    image = request.files.get('image')

    if not word_count or word_count <= 0:
        return jsonify({'error': 'Invalid word count'}), 400

    prompt = f"Create a unique fusion recipe combining {dish1} and {dish2}. Make it {word_count} words long."

    if image and image.filename:
        img = Image.open(image)
        img_encoded = encode_image(img)
        prompt += " Also, generate a recipe based on this image."

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([prompt])

        generated_content = response.text if response.text else "No content generated."
        return jsonify({'generated_content': generated_content})

    except Exception as e:
        return jsonify({'error': f"Error generating content: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

