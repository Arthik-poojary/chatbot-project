# 🤖 AI Chatbot with Google Gemini & MongoDB Atlas

An intelligent chatbot application powered by Google Gemini API with MongoDB Atlas caching for faster responses. Built with Flask and deployed on Render for 24/7 accessibility.

---

## 🚀 Live Application

Try the chatbot now: **[https://chatbot-project-y8m9.onrender.com/](https://chatbot-project-y8m9.onrender.com/)**


## 🌟 Features

- **AI-Powered Responses**: Uses Google Gemini 2.5 Flash model for intelligent answers
- **Smart Caching**: Stores previous Q&A pairs in MongoDB Atlas to save API calls
- **RESTful API Endpoints**: Multiple endpoints for testing and monitoring
- **Secure Deployment**: Environment variables protect sensitive API keys
- **Online Accessibility**: Deployed on Render for worldwide access
- **Real-time Model Updates**: Built-in endpoint to check latest available Gemini models

---

## 🛠️ Technologies Used

### **Backend**
- **Python 3.11.7** - Core programming language
- **Flask 3.1.2** - Web framework for API and routing
- **Gunicorn 21.2.0** - Production WSGI server

### **AI & Database**
- **Google Gemini API** - AI model for generating responses
- **MongoDB Atlas** - Cloud-based NoSQL database for caching
- **PyMongo 4.6.0** - MongoDB driver for Python

### **Frontend**
- **HTML5** - Structure and layout
- **CSS3** - Styling and design
- **JavaScript** - Client-side interactivity

### **Deployment & Security**
🌐 **Live Demo:** [https://chatbot-project-y8m9.onrender.com/](https://chatbot-project-y8m9.onrender.com/)
- **Render.com** - Cloud hosting platform (free tier)
- **Python-dotenv** - Environment variable management
- **Certifi** - SSL certificate verification
- **Git & GitHub** - Version control and repository hosting

---

## 📁 Project Structure

```
chatbot-project/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Render deployment configuration
├── runtime.txt            # Python version specification
├── .env                   # Environment variables (NOT in GitHub)
├── .gitignore             # Files to exclude from Git
└── templates/
    └── index.html         # Frontend HTML template
```

---

## 🔑 Environment Variables (Secured)

The following sensitive keys are stored as environment variables and **NOT** pushed to GitHub:

```env
GEMINI_API_KEY=your_google_gemini_api_key
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### **Security Measures:**
- ✅ `.env` file is listed in `.gitignore`
- ✅ Keys are stored in Render's Environment Variables
- ✅ No sensitive data exposed in source code
- ✅ Keys are never logged or displayed publicly

---

## 🚀 How It Works

### **Workflow Diagram:**

```
User Input
    ↓
Check MongoDB Cache
    ↓
┌─────────────────┐
│  Found in DB?   │
└────┬────────┬───┘
     │ YES    │ NO
     ↓        ↓
Return      Query Gemini API
Cached          ↓
Answer      Get AI Response
     ↓           ↓
     │      Save to MongoDB
     │           ↓
     └──────→ Return Answer
```

### **Step-by-Step Process:**

1. **User submits a question** through the web interface
2. **App checks MongoDB Atlas** for existing answer
   - If found → Return cached answer instantly (fast, no API call)
   - If not found → Proceed to step 3
3. **Query Google Gemini API** for fresh answer
4. **Save the response** to MongoDB for future use
5. **Return answer** to user
6. Next time same question is asked → Retrieved from cache (step 2)

### **Benefits:**
- ⚡ **Faster responses** for repeated questions
- 💰 **Saves API quota** by caching results
- 🌐 **Works offline** for cached questions (if MongoDB is accessible)

---

## 🔗 API Endpoints

### **Main Chatbot**
```
GET/POST  /
Description: Main chatbot interface
```

### **Testing & Monitoring**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/test-api` | GET | Test Google Gemini API connection |
| `/test-mongo` | GET | Test MongoDB Atlas connection |
| `/list-models` | GET | List all available Gemini models |
| `/view-db` | GET | View cached Q&A pairs (up to 50) |
| `/clear-db` | GET | Clear all cached data |

### **Example Usage:**

```bash
# Check if Gemini API is working
https://your-app.onrender.com/test-api

# Verify MongoDB connection
https://your-app.onrender.com/test-mongo

# See available Gemini models (helpful for updates)
https://your-app.onrender.com/list-models

# View cached conversations
https://your-app.onrender.com/view-db
```

---

## 📦 Dependencies (requirements.txt)

```txt
Flask==3.1.2                    # Web framework
pymongo[srv]==4.6.0             # MongoDB driver
python-dotenv==1.2.1            # Environment variable loader
google-generativeai==0.8.5      # Google Gemini API client
gunicorn==21.2.0                # Production server
dnspython==2.8.0                # DNS resolver for MongoDB
certifi==2025.11.12             # SSL certificates
pyOpenSSL==24.0.0               # SSL/TLS support
```

---

## 🖥️ Local Development Setup

### **Prerequisites:**
- Python 3.11 or higher
- MongoDB Atlas account (free tier)
- Google Gemini API key

### **Installation Steps:**

1. **Clone the repository:**
```bash
git clone https://github.com/arthik-poojary/chatbot-project.git
cd chatbot-project
```

2. **Create virtual environment:**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file:**
```bash
GEMINI_API_KEY=your_gemini_api_key_here
MONGO_URI=your_mongodb_atlas_connection_string_here
```

5. **Run the application:**
```bash
python app.py
```

6. **Open in browser:**
```
http://127.0.0.1:5000
```

---

## 🌐 Deployment (Render.com)

### **Why Render?**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Built-in HTTPS
- ✅ Easy environment variable management

### **Deployment Steps:**

1. **Push code to GitHub** (with `.gitignore` protecting `.env`)
2. **Create account** on [Render.com](https://render.com)
3. **Create new Web Service** and connect GitHub repository
4. **Configure build settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Instance Type:** Free
5. **Add environment variables:**
   - `GEMINI_API_KEY`
   - `MONGO_URI`
6. **Deploy** and wait 3-5 minutes
7. **Access** your live chatbot at: `https://your-app.onrender.com`

### **Free Tier Limitations:**
- Apps sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- 512 MB RAM limit

---

## 🔐 Privacy & Security

### **API Key Protection:**
- All sensitive keys stored in environment variables
- `.env` file excluded from Git via `.gitignore`
- No API keys in source code or logs
- Render's environment variables are encrypted

### **Data Privacy:**
- Q&A pairs stored in private MongoDB cluster
- No personal user data collected
- Connection secured with SSL/TLS

### **Access Control:**
- MongoDB Atlas IP whitelist configured
- API rate limiting enabled (Gemini: 15 req/min)
- HTTPS enforced on production

---

## 🐛 Troubleshooting

### **MongoDB Connection Issues:**

If you see SSL handshake errors:

1. **Check `pymongo` version** in `requirements.txt`:
```txt
pymongo[srv]==4.6.0
```

2. **Verify MongoDB Atlas IP whitelist:**
   - Go to MongoDB Atlas → Network Access
   - Ensure `0.0.0.0/0` is allowed

3. **Test locally first:**
```bash
python app.py
# Check console for "✅ MongoDB Atlas connected successfully"
```

### **Gemini API Errors:**

- Verify API key is valid at [Google AI Studio](https://aistudio.google.com/app/apikey)
- Check rate limits (15 requests/minute on free tier)
- Use `/test-api` endpoint to diagnose issues

### **Deployment Failures:**

- Check Render logs for specific errors
- Ensure all environment variables are set
- Verify `Procfile` and `runtime.txt` exist
- Clear build cache and redeploy

---

## 📊 Performance Optimization

- **Caching:** MongoDB stores repeated queries (instant responses)
- **Connection pooling:** Efficient database connections
- **Timeout management:** 10-second timeouts prevent hanging
- **Error handling:** Graceful fallbacks if services are unavailable

---

## 🎯 Future Enhancements

- [ ] User authentication system
- [ ] Conversation history tracking
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Custom domain integration
- [ ] Advanced analytics dashboard
- [ ] Rate limiting per user
- [ ] Improved UI/UX design

---

## 📝 License

This project is open-source and available for educational purposes.

---

## 👤 Author

**Arthik Poojary**
- GitHub: [@arthik-poojary](https://github.com/arthik-poojary)
- Project: [chatbot-project](https://github.com/arthik-poojary/chatbot-project)

---

## 🙏 Acknowledgments

- **Google Gemini** - AI model provider
- **MongoDB Atlas** - Cloud database service
- **Render.com** - Free hosting platform
- **Flask** - Python web framework

---

## ⚠️ Status

**🚧 WORK IN PROGRESS**

This project is actively being developed. Some features may be incomplete or under testing. MongoDB SSL connection is currently being debugged for production deployment.

**Current Status:**
- ✅ Gemini API integration - Working
- ✅ Local MongoDB caching - Working
- ✅ Frontend interface - Working
- ✅ Render deployment - Working

---

## 📞 Support

For issues, questions, or contributions, please:
1. Check the troubleshooting section above
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Use `/test-api` and `/test-mongo` endpoints for diagnostics

---

**Built with ❤️ using Python, Flask, Google Gemini, and MongoDB Atlas**
