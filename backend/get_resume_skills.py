from openai import OpenAI

def extract_skills_from_resume(
    resume_text: str,
    api_key: str,
    model: str = "moonshotai/kimi-k2"
) -> str:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )

    system_prompt = (
        "You are an expert resume analyzer. Given a resume text, "
        "your task is to extract a **clean and precise list of skills** "
        "mentioned in the resume, including both technical and soft skills. "
        "Only return the skills as a single, comma-separated string, with no explanation."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": resume_text}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
