import os
import json
from dotenv import load_dotenv
from mistralai import Mistral

from .scraper import scrape_job_description
from .prompts import resume_score_prompt, tailored_answer_prompt
from .models import ResumeScore
load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def call_mistral(prompt):

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def extract_json(text):
    """Extract JSON from markdown code blocks or raw text."""
    import re
    
    # Try to find JSON in markdown code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # Try to find JSON object directly
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    return text


# ================================
# Resume + JD Analyzer Agent
# ================================

def analyze_resume_and_jd(resume_text, jd_url):

    jd_text = scrape_job_description(jd_url)

    prompt = resume_score_prompt.format(
        resume=resume_text,
        jd=jd_text
    )

    raw = call_mistral(prompt)

    try:
        json_text = extract_json(raw)
        data = json.loads(json_text)
    except Exception as e:
        print(f"Raw LLM response:\n{raw}\n")
        raise ValueError(f"LLM returned invalid JSON: {e}")

    validated = ResumeScore(**data)

    return validated


# ================================
# Tailored Answer Agent
# ================================

def generate_tailored_answer(profile, jd_url, question):

    jd_text = scrape_job_description(jd_url)

    prompt = tailored_answer_prompt.format(
        profile=profile,
        jd=jd_text,
        question=question
    )

    return call_mistral(prompt)
