import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text, prompt_type="summary"):
    if prompt_type == "concept":
        system_prompt = (
            "You are an AI learning assistant. Explain the following AI concept in clear, concise, and professional language suitable for a beginner. Avoid overly casual or chatty tone."
        )
    else:
        system_prompt = (
            "You are an AI learning assistant. Summarize the following article in clear, concise, and professional language suitable for a beginner. Avoid overly casual or chatty tone."
        )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()


def extract_concepts(text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're an AI tutor. Read this content and list 3–5 important AI-related concepts or terms a beginner might want to learn more about. Return them as a numbered list."},
            {"role": "user", "content": text}
        ]
    )
    concepts = response.choices[0].message.content.strip().split("\n")
    return [c.lstrip("12345. ").strip() for c in concepts if c.strip()]


def suggest_followup(concept):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're an AI tutor helping someone explore AI."},
            {"role": "user", "content": (
                f"What is a natural follow-up question someone might ask after learning about {concept}? "
                "Keep it beginner-friendly and thoughtful."
            )}
        ]
    )
    return response.choices[0].message.content.strip()


def check_accuracy(article_text, generated_text):
    system_prompt = (
        "You are an expert fact-checker. Compare the following article and its summary or explanation. "
        "Does the summary or explanation accurately reflect the article? "
        "If yes, respond with 'Accurate'. If not, list specific inaccuracies or hallucinations."
    )
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"ARTICLE:\n{article_text}\n\nSUMMARY/EXPLANATION:\n{generated_text}"}
        ]
    )
    return response.choices[0].message.content.strip()

