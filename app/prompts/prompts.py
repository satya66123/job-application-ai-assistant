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