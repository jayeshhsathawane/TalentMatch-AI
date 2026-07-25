from flask import Flask, request, render_template, jsonify
from werkzeug.datastructures import FileStorage
from dotenv import load_dotenv
import requests
import os
import json
import PyPDF2
import logging


load_dotenv()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder="../templates")

def extract_text_from_file(file: FileStorage) -> str:
    """Extracts and returns text from PDF or TXT files."""
    filename = file.filename.lower()
    text = ""
    try:
        if filename.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        else:
            text = file.read().decode('utf-8', errors='ignore')
    except Exception as e:
        logger.error(f"File extraction failed: {str(e)}")
    return text

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded."}), 400
        
    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    if not job_description or not resume_file.filename:
        return jsonify({"error": "Missing required fields."}), 400
        
    try:
        logger.info(f"Processing evaluation for file: {resume_file.filename}")
        resume_text = extract_text_from_file(resume_file)
        
        
        prompt = f"""
        You are an elite Technical HR AI and ATS Parser. Analyze the candidate's resume against the job description.
        Provide the response strictly in JSON format with exactly these keys:
        - "candidate_name": (string, extract from resume, or "Not Found")
        - "contact_info": (string, extract email/phone, or "Not Found")
        - "match_percentage": (integer between 0 and 100)
        - "authenticity_score": (integer between 0 and 100 representing if the resume looks genuine or contains stuffed/fake keywords)
        - "key_matching_skills": (list of maximum 5 matching skills)
        - "missing_skills": (list of maximum 5 missing requirements)
        - "recommendation": (A 2-sentence professional assessment)
        
        Job Description: {job_description}
        Resume: {resume_text}
        """
        
      
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            logger.error("Gemini API key is missing from environment variables.")
            return jsonify({"error": "Server configuration error. API key missing."}), 500
            
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3.5-flash:generateContent?key={api_key}"
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        if response.status_code != 200:
            error_msg = response_data.get('error', {}).get('message', 'Unknown API Error')
            logger.error(f"Google API Error: {error_msg}")
            return jsonify({"error": f"AI Processing Error: {error_msg}"}), 502
            
        ai_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Robust JSON Parsing
        if ai_text.startswith("```json"):
            ai_text = ai_text[7:-3].strip()
        elif ai_text.startswith("```"):
            ai_text = ai_text[3:-3].strip()
            
        result = json.loads(ai_text)
        logger.info("Successfully generated AI evaluation.")
        return jsonify(result)
        
    except json.JSONDecodeError:
        logger.error("Failed to parse AI response into JSON format.")
        return jsonify({"error": "AI returned malformed data. Please try again."}), 500
    except Exception as e:
        logger.error(f"Unexpected backend error: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal Server Error."}), 500

if __name__ == '__main__':
    app.run(debug=True)