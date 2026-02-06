"""
Job Matcher - Scrapes real LinkedIn jobs and matches against resume
"""

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from typing import List, Dict

# Fallback mock jobs if scraping fails
MOCK_JOBS = [
    {
        "title": "Senior Python Developer",
        "company": "Tech Innovations Inc",
        "location": "Remote",
        "description": "We are seeking a Senior Python Developer with expertise in FastAPI, Django, and cloud technologies. You will work on building scalable microservices and APIs. Required skills include Python, FastAPI, PostgreSQL, Docker, AWS, and experience with CI/CD pipelines.",
        "url": "https://example.com/jobs/senior-python-dev",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker", "AWS", "CI/CD", "Microservices"]
    },
    {
        "title": "Full Stack Engineer",
        "company": "StartupXYZ",
        "location": "San Francisco, CA",
        "description": "Join our fast-growing startup as a Full Stack Engineer. Work with React, Node.js, Python, and MongoDB. Build innovative products from scratch. Looking for someone with 3+ years experience in full stack development.",
        "url": "https://example.com/jobs/fullstack-engineer",
        "required_skills": ["React", "Node.js", "Python", "MongoDB", "JavaScript", "REST APIs", "Git"]
    },
    {
        "title": "Backend Software Engineer",
        "company": "CloudTech Solutions",
        "location": "New York, NY",
        "description": "Backend engineer needed for cloud-native applications. Experience with Python, Django, Kubernetes, and AWS required. You'll design and implement RESTful APIs and work with distributed systems.",
        "url": "https://example.com/jobs/backend-engineer",
        "required_skills": ["Python", "Django", "Kubernetes", "AWS", "REST APIs", "PostgreSQL", "Redis"]
    },
    {
        "title": "DevOps Engineer",
        "company": "Infrastructure Co",
        "location": "Remote",
        "description": "We need a DevOps engineer to manage our cloud infrastructure. Terraform, Docker, Kubernetes, AWS, and Python scripting experience required. Help us build CI/CD pipelines and improve deployment processes.",
        "url": "https://example.com/jobs/devops-engineer",
        "required_skills": ["Docker", "Kubernetes", "Terraform", "AWS", "CI/CD", "Python", "Linux"]
    },
    {
        "title": "Data Engineer",
        "company": "BigData Corp",
        "location": "Austin, TX",
        "description": "Build data pipelines using Python, Spark, and Airflow. Work with large-scale datasets and design ETL processes. Experience with SQL, NoSQL databases, and cloud platforms required.",
        "url": "https://example.com/jobs/data-engineer",
        "required_skills": ["Python", "Spark", "Airflow", "SQL", "AWS", "ETL", "Data Modeling"]
    },
    {
        "title": "Machine Learning Engineer",
        "company": "AI Startups Ltd",
        "location": "Remote",
        "description": "ML Engineer to build and deploy machine learning models. TensorFlow, PyTorch, Python, and cloud experience required. Work on cutting-edge AI applications.",
        "url": "https://example.com/jobs/ml-engineer",
        "required_skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "AWS", "Docker", "MLOps"]
    },
    {
        "title": "Software Development Engineer",
        "company": "Enterprise Solutions Inc",
        "location": "Seattle, WA",
        "description": "SDE role working on enterprise applications. Java, Spring Boot, and microservices experience preferred. Work with distributed systems and cloud technologies.",
        "url": "https://example.com/jobs/sde",
        "required_skills": ["Java", "Spring Boot", "Microservices", "AWS", "PostgreSQL", "Kafka", "Docker"]
    },
    {
        "title": "Cloud Solutions Architect",
        "company": "CloudFirst Technologies",
        "location": "Remote",
        "description": "Design cloud infrastructure for enterprise clients. AWS, Azure, Terraform, and Python automation skills needed. 5+ years cloud architecture experience required.",
        "url": "https://example.com/jobs/cloud-architect",
        "required_skills": ["AWS", "Azure", "Terraform", "Python", "Kubernetes", "Architecture", "Security"]
    },
    {
        "title": "API Developer",
        "company": "Integration Systems",
        "location": "Boston, MA",
        "description": "Build robust APIs using FastAPI and Python. Work with microservices architecture, PostgreSQL, and deploy to AWS. Experience with API design and documentation required.",
        "url": "https://example.com/jobs/api-developer",
        "required_skills": ["Python", "FastAPI", "REST APIs", "PostgreSQL", "Docker", "AWS", "Swagger"]
    },
    {
        "title": "Platform Engineer",
        "company": "TechScale Inc",
        "location": "Remote",
        "description": "Platform engineering role focused on developer experience. Build internal tools and platforms using Python, Kubernetes, and cloud services. Strong automation and DevOps background needed.",
        "url": "https://example.com/jobs/platform-engineer",
        "required_skills": ["Python", "Kubernetes", "Docker", "AWS", "Terraform", "CI/CD", "Automation"]
    }
]


def extract_skills_from_resume(resume_text: str) -> List[str]:
    """Extract skills from resume text - simplified version"""
    skills_keywords = [
        "Python", "Java", "JavaScript", "TypeScript", "React", "Node.js", "FastAPI", "Django",
        "Flask", "Spring Boot", "Docker", "Kubernetes", "AWS", "Azure", "GCP", "PostgreSQL",
        "MySQL", "MongoDB", "Redis", "Kafka", "RabbitMQ", "Microservices", "REST APIs",
        "GraphQL", "CI/CD", "Terraform", "Ansible", "Linux", "Git", "Agile", "Scrum",
        "Machine Learning", "TensorFlow", "PyTorch", "Spark", "Airflow", "ETL", "SQL",
        "NoSQL", "Elasticsearch", "Prometheus", "Grafana", "Jenkins", "GitHub Actions"
    ]
    
    resume_upper = resume_text.upper()
    found_skills = []
    
    for skill in skills_keywords:
        if skill.upper() in resume_upper:
            found_skills.append(skill)
    
    return found_skills


def calculate_match_score(resume_skills: List[str], job_skills: List[str]) -> int:
    """Calculate match percentage between resume and job requirements"""
    if not job_skills:
        return 50
    
    resume_skills_upper = [s.upper() for s in resume_skills]
    matching = sum(1 for skill in job_skills if skill.upper() in resume_skills_upper)
    
    score = int((matching / len(job_skills)) * 100)
    return min(score, 100)


def scrape_linkedin_jobs(job_query: str, location: str = "", max_results: int = 15) -> List[Dict]:
    """
    Scrape real LinkedIn jobs based on search query
    Returns list of job dictionaries
    """
    jobs = []
    
    try:
        # Clean and encode search parameters
        keywords = urllib.parse.quote(job_query)
        location_param = urllib.parse.quote(location) if location else ""
        
        # LinkedIn job search URL
        base_url = f"https://www.linkedin.com/jobs/search?keywords={keywords}"
        if location_param:
            base_url += f"&location={location_param}"
        base_url += "&position=1&pageNum=0"
        
        # Headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        # Fetch the page
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job cards
        job_cards = soup.find_all('div', class_='base-card', limit=max_results)
        
        if not job_cards:
            # Try alternative selectors
            job_cards = soup.find_all('li', limit=max_results)
        
        for card in job_cards[:max_results]:
            try:
                # Extract job title
                title_elem = card.find('h3', class_='base-search-card__title')
                if not title_elem:
                    title_elem = card.find('a', class_='base-card__full-link')
                title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
                
                # Extract company name
                company_elem = card.find('h4', class_='base-search-card__subtitle')
                if not company_elem:
                    company_elem = card.find('a', class_='hidden-nested-link')
                company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                
                # Extract location
                location_elem = card.find('span', class_='job-search-card__location')
                job_location = location_elem.get_text(strip=True) if location_elem else "Not specified"
                
                # Extract job URL
                link_elem = card.find('a', class_='base-card__full-link')
                if not link_elem:
                    link_elem = card.find('a', href=True)
                job_url = link_elem.get('href', '') if link_elem else ""
                
                # Make sure URL is absolute
                if job_url and isinstance(job_url, str) and not job_url.startswith('http'):
                    job_url = 'https://www.linkedin.com' + job_url
                
                # Extract snippet/description
                snippet_elem = card.find('p', class_='base-search-card__snippet')
                description = snippet_elem.get_text(strip=True) if snippet_elem else title
                
                # Only add if we have at least title and company
                if title != "Unknown Title" and company != "Unknown Company":
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "description": description,
                        "url": job_url,
                        "required_skills": extract_skills_from_resume(description)  # Extract skills from description
                    })
                    
            except Exception as e:
                # Skip this job if parsing fails
                continue
        
        # Add small delay to be respectful
        time.sleep(0.5)
        
    except Exception as e:
        print(f"LinkedIn scraping error: {str(e)}")
        # Return empty list, will fall back to mock data
        return []
    
    return jobs


def find_matching_jobs(resume_text: str, job_query: str, location: str = "", min_score: int = 60) -> List[Dict]:
    """
    Find jobs matching the resume by scraping LinkedIn
    Falls back to mock data if scraping fails
    """
    # Extract skills from resume
    resume_skills = extract_skills_from_resume(resume_text)
    
    # Try to scrape real LinkedIn jobs first
    print(f"Attempting to scrape LinkedIn jobs for: {job_query}")
    linkedin_jobs = scrape_linkedin_jobs(job_query, location, max_results=15)
    
    # Use LinkedIn jobs if we got any, otherwise fall back to mock data
    if linkedin_jobs:
        print(f"Successfully scraped {len(linkedin_jobs)} jobs from LinkedIn")
        jobs_to_process = linkedin_jobs
        source = "LinkedIn"
    else:
        print("Falling back to mock job data")
        jobs_to_process = MOCK_JOBS
        source = "Mock"
    
    # Filter and score jobs
    filtered_jobs = []
    query_lower = job_query.lower()
    location_lower = location.lower() if location else ""
    
    for job in jobs_to_process:
        # Check if job matches search query
        if query_lower not in job["title"].lower() and query_lower not in job["description"].lower():
            continue
        
        # Check location if specified
        if location_lower and location_lower != "remote":
            if location_lower not in job["location"].lower():
                continue
        
        # Calculate match score
        score = calculate_match_score(resume_skills, job["required_skills"])
        
        # Filter by minimum score
        if score < min_score:
            continue
        
        # Find matching and missing skills
        resume_skills_upper = [s.upper() for s in resume_skills]
        matching_skills = [s for s in job["required_skills"] if s.upper() in resume_skills_upper]
        missing_skills = [s for s in job["required_skills"] if s.upper() not in resume_skills_upper]
        
        filtered_jobs.append({
            "title": job["title"],
            "company": job["company"],
            "location": job["location"],
            "description": job["description"],
            "url": job["url"],
            "score": score,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills
        })
    
    # Sort by score descending
    filtered_jobs.sort(key=lambda x: x["score"], reverse=True)
    
    return filtered_jobs
