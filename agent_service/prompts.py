resume_score_prompt = """
You are an expert AI career coach.

Compare Resume vs Job Description and return ONLY a valid JSON object.

Resume:
{resume}

Job Description:
{jd}

Return STRICT JSON format (no markdown, no extra text):
{{
 "score": 75,
 "missing_skills": ["Docker", "Kubernetes"],
 "suggestions": ["Add Docker containerization experience", "Highlight any cloud platform experience"]
}}

Your response:"""


tailored_answer_prompt = """
You are a professional career advisor helping a candidate write compelling application answers.

User Profile:
{profile}

Job Description:
{jd}

Application Question: {question}

Write a concise, professional answer (2-3 paragraphs maximum) that:
- Directly addresses the question
- Highlights relevant experience from the profile
- Shows alignment with the job requirements
- Uses confident, professional language

Answer:"""