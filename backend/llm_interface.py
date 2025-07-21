# backend/llm_interface.py

from openai import OpenAI
def get_tailored_resume(
    resume_text: str, job_description: str, api_key: str, prompt: str = "",  model: str = "anthropic/claude-3.7-sonnet"  # default fallback

) -> str:
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )


    user_prompt = f"""
    JOB DESCRIPTION:
    {job_description}

    RESUME TEXT:
    {resume_text}

    INSTRUCTIONS:
    {prompt}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": user_prompt}],
        temperature=0.4,
        max_tokens=1500,

    )

    return response.choices[0].message.content
























# from openai import OpenAI


# def get_tailored_resume(
#     resume_text: str, job_description: str, api_key: str, prompt: str = ""
# ) -> str:
#     client = OpenAI(api_key=api_key)

#     # You no longer need a fixed system prompt unless you want defaults
#     user_prompt = f"""
#     JOB DESCRIPTION:
#     {job_description}

#     RESUME TEXT:
#     {resume_text}

#     INSTRUCTIONS:
#     {prompt}
#     """

#     response = client.chat.completions.create(
#         model="gpt-4-turbo",
#         messages=[{"role": "user", "content": user_prompt}],
#         temperature=0.4,
#         max_tokens=1500,
#     )

#     return response.choices[0].message.content
