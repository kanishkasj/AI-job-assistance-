from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from database import SessionLocal, engine
import models, schemas, crud
from agent_service.agent import analyze_resume_and_jd, generate_tailored_answer
from agent_service.job_matcher import find_matching_jobs

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Application Assistant API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enhanced structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    """Serve the frontend"""
    return FileResponse("static/index.html")


@app.get("/status")
def health():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.post("/api/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user profile"""
    logger.info(f"Creating user with email: {user.email}")
    try:
        result = crud.create_user(db, user)
        logger.info(f"User created successfully with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user profile by ID"""
    logger.info(f"Fetching user with ID: {user_id}")
    user = crud.get_user(db, user_id)
    if not user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/api/applications")
def create_application(application: schemas.JobApplicationCreate, db: Session = Depends(get_db)):
    """Create a new job application"""
    logger.info(f"Creating application for user {application.user_id} at {application.company_name}")
    try:
        result = crud.create_job_application(db, application)
        logger.info(f"Application created with ID: {result.id}")
        return result
    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/applications/user/{user_id}")
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    """Get all applications for a user (Dashboard)"""
    logger.info(f"Fetching applications for user: {user_id}")
    applications = crud.get_user_applications(db, user_id)
    return applications


@app.put("/api/applications/{app_id}")
def update_application(app_id: int, updates: schemas.JobApplicationUpdate, db: Session = Depends(get_db)):
    """Update application status"""
    logger.info(f"Updating application {app_id} with status: {updates.status}")
    result = crud.update_job_application(db, app_id, updates)
    if not result:
        logger.warning(f"Application not found: {app_id}")
        raise HTTPException(status_code=404, detail="Application not found")
    return result


@app.post("/api/resume/analyze")
def resume_analyze(req: schemas.ResumeRequest):
    """Analyze resume against job description"""
    logger.info(f"Analyzing resume for JD: {req.jd_url}")
    try:
        result = analyze_resume_and_jd(req.resume, req.jd_url)
        logger.info(f"Resume analysis completed with score: {result.score}")
        return result.dict()
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/answer")
def generate_answer(req: schemas.AnswerRequest):
    """Generate tailored answer for application question"""
    logger.info(f"Generating answer for question: {req.question[:50]}...")
    try:
        answer = generate_tailored_answer(req.profile, req.jd_url, req.question)
        logger.info("Answer generated successfully")
        return {"answer": answer}
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/jobs/search")
def search_jobs(req: schemas.JobSearchRequest):
    """Search for jobs matching the resume"""
    logger.info(f"Searching jobs for query: {req.job_query}, location: {req.location}, min score: {req.min_match_score}")
    try:
        jobs = find_matching_jobs(
            resume_text=req.resume,
            job_query=req.job_query,
            location=req.location,
            min_score=req.min_match_score
        )
        logger.info(f"Found {len(jobs)} matching jobs")
        return {"jobs": jobs, "total": len(jobs)}
    except Exception as e:
        logger.error(f"Error searching jobs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))