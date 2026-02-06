from agent import analyze_resume_and_jd, generate_tailored_answer

resume = """
AI student with experience in ML, NLP and React.
Built YOLO attention models and DTI prediction systems.
"""

jd_url = "https://boards.greenhouse.io/example"

result = analyze_resume_and_jd(resume, jd_url)

print("Resume Score:")
print(result)

profile = """
Skills: Python, ML, DL, Transformers
Education: AI & DS student
Projects: YOLOv8 Attention, Drug Discovery
"""

answer = generate_tailored_answer(
    profile,
    jd_url,
    "Why are you a good fit?"
)

print("\nTailored Answer:")
print(answer)
