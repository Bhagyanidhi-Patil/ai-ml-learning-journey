from flask import Flask,render_template,request,jsonify
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

#load api key
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def fix_bug(code,language):
    prompt = f"""
    You are senior software engineer.
    Fix the bug in the following {language}code.
    Return:
        1. Fixed code (only code)
        2. Explaination (clear and short)
    Buggy code:
    {code}
"""
    response = client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [
            {"role":"user","content":prompt}
        ],
        temperature = 0.2
    )
    return response.choices[0].message.content

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fix",methods=["POST"])
def fix():
    data = request.json
    code = data.get("code")
    language = data.get("language")

    if not code:
        return jsonify({"error": "No code provided"}) , 400
    result = fix_bug(code,language)
    return jsonify({"result":result})

if __name__ == "__main__":
    app.run(debug=True)

# to run this code, run python app.py in the terminal and 
# open http://127.0.0.1:5000/ in browser