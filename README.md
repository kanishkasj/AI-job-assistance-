# Job Application Assistant 
An AI-powered job application platform that helps users optimize their resumes, generate tailored answers, and track applications.

## Features 

### 1. **Profile Management (Autofill Agent)**
- Store user information (name, email, phone, skills, education, work history)
- Quick autofill for job applications
- Secure profile storage in SQLite database

### 2. **Resume-to-JD Scorer Agent**
- Analyze resume against job descriptions
- Get AI-powered match score
- Receive missing skills analysis
- Get actionable suggestions for improvement

### 3. **Tailored Answer Generator**
- Generate personalized answers for application questions
- AI analyzes job description and your profile
- Creates compelling, customized responses

### 4. **Application Dashboard**
- Track all job applications in one place
- Monitor application status:
  - Not Submitted
  - Submitted
  - Initial Response Received
  - Interview Requested
  - Onsite/Video Interview
  - Rejected
- View application history and notes

## Tech Stack 

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for data storage
- **Mistral AI**: Large Language Model for AI capabilities
- **BeautifulSoup**: Web scraping for job descriptions

### Frontend
- **HTML/CSS/JavaScript**: Simple, clean interface
- **Vanilla JavaScript**: No framework dependencies
- **Responsive Design**: Works on all devices

## Architecture 
```
├── Backend (FastAPI)
│   ├── API Endpoints
│   ├── Database Layer (SQLAlchemy)
│   └── Agent Service (AI Logic)
├── AI Agents (Data Science)
│   ├── Web Scraper
│   ├── Resume Analyzer
│   └── Answer Generator
└── Frontend (Static HTML)
    └── Interactive UI
```

## Installation & Setup 

### Prerequisites
- Python 3.8+
- Mistral AI API Key

### Steps

1. **Clone/Navigate to Project**
```powershell
cd E:\pma\assessment
```

2. **Create Virtual Environment**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Install Dependencies**
```powershell
pip install -r requirements.txt
pip install -r agent_service/requirements.txt
```

4. **Set Environment Variables**
Create a `.env` file:
```
MISTRAL_API_KEY=your_api_key_here
```

5. **Run the Application**
```powershell
uvicorn main:app --reload
```

6. **Access the Application**
- Frontend: http://127.0.0.1:8000/
- API Docs: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/status

## API Endpoints 

### User Management
- `POST /api/users` - Create user profile
- `GET /api/users/{user_id}` - Get user profile

### AI Agents
- `POST /api/resume/analyze` - Analyze resume vs JD
- `POST /api/generate/answer` - Generate tailored answer

### Application Tracking
- `POST /api/applications` - Create job application
- `GET /api/applications/user/{user_id}` - Get user's applications
- `PUT /api/applications/{app_id}` - Update application status

### System
- `GET /status` - Health check

## Usage Guide 

### 1. Create Your Profile
1. Go to "Profile" tab
2. Fill in your information
3. Click "Save Profile"
4. Note your User ID for later use

### 2. Analyze Your Resume
1. Go to "Resume Analyzer" tab
2. Paste your resume text
3. Enter job description URL
4. Click "Analyze Match"
5. Review score, missing skills, and suggestions

### 3. Generate Tailored Answers
1. Go to "Answer Generator" tab
2. Enter your profile summary
3. Provide job description URL
4. Enter the application question
5. Click "Generate Answer"
6. Copy the AI-generated response

### 4. Track Applications
1. Go to "Dashboard" tab
2. Enter your User ID
3. Add new applications with company, role, and status
4. Click "Load Applications" to view all your applications

## Logging 

Enhanced structured logging includes:
- Timestamp for each request
- Log level (INFO, WARNING, ERROR)
- Detailed error messages
- API endpoint tracking
- User action monitoring

Logs format:
```
2026-02-05 10:30:15 - __main__ - INFO - Creating user with email: john@example.com
2026-02-05 10:30:16 - __main__ - INFO - User created successfully with ID: 1
```

## Database Schema 

### Users Table
```sql
- id: Integer (Primary Key)
- name: String
- email: String (Unique)
- phone: String
- skills: Text
- education: Text
- work_history: Text
- created_at: DateTime
```

### Job Applications Table
```sql
- id: Integer (Primary Key)
- user_id: Integer
- company_name: String
- job_title: String
- jd_url: Text
- status: String
- score: Integer
- applied_date: DateTime
- notes: Text
```

## File Structure 

```
assessment/
├── main.py                 # FastAPI application
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── crud.py                 # Database operations
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── assessment.db           # SQLite database
├── static/
│   └── index.html         # Frontend UI
└── agent_service/
    ├── agent.py           # AI agent logic
    ├── scraper.py         # Web scraping tool
    ├── prompts.py         # LLM prompts
    ├── models.py          # Data models
    └── requirements.txt   # Agent dependencies
```

## Security Notes 

- `.env` file contains sensitive API keys - **never commit to version control**
- Add `.env` to `.gitignore`
- Use environment variables for all secrets
- CORS enabled for development (restrict in production)

## Future Enhancements 

- [ ] User authentication and authorization
- [ ] File upload for resume PDFs
- [ ] Email notifications for application updates
- [ ] Chrome extension for autofill
- [ ] Advanced analytics dashboard
- [ ] Export applications to CSV/PDF
- [ ] Integration with LinkedIn API
- [ ] Multi-language support

## Troubleshooting 

### Server won't start
- Check if port 8000 is available
- Ensure all dependencies are installed
- Verify `.env` file exists with valid API key

### AI features not working
- Verify Mistral API key is correct
- Check internet connection
- Review terminal logs for detailed errors

### Database errors
- Delete `assessment.db` and restart server
- Check SQLite installation
- Verify file permissions

## Team Roles Implementation 

### Backend Engineers
✔ Robust FastAPI architecture  
✔ RESTful API endpoints  
✔ Database management with SQLAlchemy  
✔ Structured logging 
✔ Error handling and validation  
✔ CORS configuration  
✔ Health monitoring  

### Data Scientists
✔ Web scraping implementation  
✔ LLM prompt engineering  
✔ Resume analysis agent  
✔ Answer generation agent  
✔ Structured data parsing  
✔ AI workflow design  

## License 

This project is for educational purposes.

## Support 

For issues or questions, check the logs or API documentation at `/docs`.

---

**Built with ❤️ using FastAPI, Mistral AI, and Modern Web Technologies**
