RESUME_PROMPT = """
You are a senior technical recruiter.

Candidate Resume:
{resume}

Job Description:
{job_description}

Task:
- Generate 5 highly relevant resume bullet points
- Match the job requirements
- Use strong action verbs
- Keep points concise
- Focus on measurable impact
- Make content ATS friendly

Output:
Bullet points only
"""

COVER_LETTER_PROMPT = """
You are an expert HR recruiter.

Candidate Resume:
{resume}

Job Description:
{job_description}

Task:
Write a professional ATS-friendly cover letter.

Rules:
- Keep it concise
- Professional tone
- Highlight matching skills
- Mention business impact
- No markdown
- No headings

Output:
Only the cover letter
"""

INTERVIEW_QUESTIONS_PROMPT = """
You are a senior technical interviewer.

Candidate Resume:
{resume}

Job Description:
{job_description}

Task:
Generate exactly 10 interview questions.

Rules:
- Focus on backend technical questions
- Include FastAPI/Python questions if relevant
- Include AI integration questions if relevant
- Include 2 scenario/problem-solving questions
- No introduction text
- No headings
- No numbering
- No markdown
- Output questions only
"""

ATS_PROMPT = """
You are an ATS resume screening system.

Candidate Resume:
{resume}

Job Description:
{job_description}

Task:
Analyze resume against job description.

Rules:
Return ONLY:

Match Percentage: XX%

Missing Keywords:
- keyword 1
- keyword 2

Improvement Suggestions:
1. suggestion
2. suggestion

No explanations.
No markdown formatting.
"""