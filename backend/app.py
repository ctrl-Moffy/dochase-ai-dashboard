from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from root .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)


# 🔍 ANALYZE CAMPAIGN
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json

        # If it's a chat message
        if "question" in data:
            user_question = data["question"]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketing campaign expert."},
                    {"role": "user", "content": user_question}
                ]
            )

            return jsonify({
                "analysis": response.choices[0].message.content
            })

        # If it's campaign data
        impressions = data.get("impressions", 0)
        clicks = data.get("clicks", 0)
        ctr = data.get("ctr", 0)
        cpc = data.get("cpc", 0)
        cpm = data.get("cpm", 0)

        prompt = f"""
        Analyze this marketing campaign:

        Impressions: {impressions}
        Clicks: {clicks}
        CTR: {ctr}%
        CPC: ${cpc}
        CPM: ${cpm}

        Provide:
        1. Key Issues
        2. Why it's happening
        3. Recommendations
        4. Priority actions

        Keep it clear, structured, and professional.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional digital marketing analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({
            "analysis": response.choices[0].message.content
        })

    except Exception as e:
        print("ERROR:", str(e))  # shows error in terminal
        return jsonify({"error": str(e)}), 500


# 🚀 RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)