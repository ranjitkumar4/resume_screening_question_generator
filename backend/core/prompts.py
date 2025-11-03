def behavioral_q_template():
    return """
Few-shot examples for behavioral questions:

Example 1:
Resume: Candidate with 3 years in Python, SQL
JD: Data Analyst
Question: Describe a challenging data analysis project you handled and the outcome.

Example 2:
Resume: Candidate with 5 years in sales
JD: Sales Manager
Question: Tell me about a time you exceeded your sales targets.

Example 3:
Resume: Candidate with team leadership experience
JD: Project Manager
Question: Describe a conflict within your team and how you resolved it.
"""

def resume_parse_prompt(resume_text):
    """
    Prompt template for resume parsing.
    Extracts: Name, Education, Skills, Experience
    """
    return f"""
You are an expert resume parser.
Extract and format the following details clearly:
- Name
- Education
- Skills
- Experience (with years)

Resume:
{resume_text}

Output format:
Name:
Education:
Skills:
Experience:
"""


def jd_match_prompt(resume_info, jd_text):
    """
    Prompt for JD matching.
    """
    return f"""
Compare the candidate resume and the job description.
Highlight matching skills, experience relevance, and give an overall score (0–100).
Resume Info:
{resume_info}

Job Description:
{jd_text}

Output:
- Matching Skills:
- Experience Fit:
- Score:
"""


def qgen_prompt(resume_info, jd_text):
    """
    Prompt for generating technical & behavioral questions.
    """
    return f"""
You are an interview assistant.
Generate:
1. Technical questions (based on resume + JD)
2. Behavioral questions (based on role and experience)
3. General questions (about problem-solving, communication)

Resume Info:
{resume_info}

Job Description:
{jd_text}

Output:
Technical Questions:
Behavioral Questions:
General Questions:
"""
def qgen_prompt(resume_info, jd_text):
    """
    Build prompt for generating interview questions.
    """
    return f"""
    You are an AI interview assistant.

    Based on the following Resume and Job Description, generate 3 categories of interview questions:
    1. Technical Questions related to the candidate's hard skills, tools, and experience.
    2. Behavioral Questions based on soft skills, teamwork, problem-solving, adaptability, etc.
    3. General Questions covering motivation, goals, and cultural fit.

    Resume:
    {resume_info}

    Job Description:
    {jd_text}

    Return your output strictly as JSON with this structure:
    {{
        "technical": [list of 5 questions],
        "behavioral": [list of 5 questions],
        "general": [list of 5 questions]
    }}
    """
