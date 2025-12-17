from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# MongoDB connection
 # MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")

try:
    client =  MongoClient(
        MONGO_URI, 
        serverSelectionTimeoutMS=5000,
        tls=True,
        tlsAllowInvalidCertificates=True
    )
    client.admin.command('ping')
    db = client["chatbot_db"]
    collection = db["qa"]
    print("✅ MongoDB Atlas connected successfully")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")

app = Flask(__name__)

# Configure Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ Warning: GEMINI_API_KEY not found in .env file")
else:
    print(f"✅ Gemini API Key loaded: {GEMINI_API_KEY[:10]}...")
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('models/gemini-2.5-flash')

def query_gemini(question):
    """Query Google Gemini AI"""
    try:
        # Generate response
        response = model.generate_content(
            f"Answer this question concisely in 2-3 sentences: {question}",
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 200,
            }
        )
        
        answer = response.text.strip()
        print(f"✅ Gemini Response: {answer[:100]}...")
        return answer
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Gemini Error: {error_msg}")
        
        if "API_KEY_INVALID" in error_msg or "401" in error_msg:
            return "❌ Invalid API key. Please check your GEMINI_API_KEY in .env file."
        elif "quota" in error_msg.lower() or "429" in error_msg:
            return "⏰ Rate limit exceeded. Please wait a moment and try again."
        elif "SAFETY" in error_msg:
            return "⚠️ Response blocked by safety filters. Try rephrasing your question."
        else:
            return f"❌ Error: {error_msg}"

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None

    if request.method == "POST":
        question = request.form.get("question")

        if not question:
            return render_template("index.html", answer="Please ask a question.")

        question_lower = question.strip().lower()

        # 1️⃣ Check MongoDB for cached answer
        try:
            record = collection.find_one({"question": question_lower})
            if record:
                answer = record["answer"]
                print(f"📦 Found in MongoDB: {answer[:50]}...")
                return render_template("index.html", answer=answer)
        except Exception as e:
            print(f"MongoDB error: {e}")

        # 2️⃣ Query Google Gemini
        answer = query_gemini(question)

        # 3️⃣ Save to MongoDB (only if valid answer)
        if answer and not answer.startswith("❌") and not answer.startswith("⏰") and not answer.startswith("⚠️"):
            try:
                collection.insert_one({
                    "question": question_lower,
                    "answer": answer
                })
                print(f"💾 Saved to MongoDB")
            except Exception as e:
                print(f"Failed to save to MongoDB: {e}")

    return render_template("index.html", answer=answer)

@app.route("/test-api")
def test_api():
    """Test Gemini API connection"""
    if not GEMINI_API_KEY:
        return {"status": "error", "message": "GEMINI_API_KEY not found in .env"}
    
    try:
        response = model.generate_content("What is 2+2? Answer in one sentence.")
        
        return {
            "status": "success",
            "response": response.text,
            "message": "✅ Gemini API is working!",
            "model": "gemini-1.5-flash"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.route("/test-mongo")
def test_mongo():
    """Test MongoDB connection"""
    try:
        client.admin.command('ping')
        count = collection.count_documents({})
        sample = list(collection.find({}, {"_id": 0}).limit(3))
        return {
            "status": "success", 
            "message": "MongoDB connected",
            "documents": count,
            "sample": sample
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/view-db")
def view_db():
    """View all stored Q&A pairs"""
    try:
        records = list(collection.find({}, {"_id": 0}).limit(50))
        return {
            "total": collection.count_documents({}), 
            "data": records
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route("/clear-db")
def clear_db():
    """Clear all cached data (optional - for testing)"""
    try:
        result = collection.delete_many({})
        return {
            "status": "success",
            "message": f"Deleted {result.deleted_count} records"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.route("/list-models")
def list_models():
    """List all available Gemini models"""
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append({
                    "name": m.name,
                    "display_name": m.display_name
                })
        return {
            "status": "success",
            "available_models": available_models
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    app.run(debug=True)