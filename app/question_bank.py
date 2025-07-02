# app/question_bank.py
from app.db import question_collection

async def load_questions_by_domain(domain: str):
    print(f"[DEBUG] Looking for domain: {domain}")
    cursor = question_collection.find({"domain": domain})
    questions = []
    async for doc in cursor:
        print(f"[DEBUG] Found doc: {doc}")
        questions.append({
            "question": doc["question"],
            "expected_answer": doc["expected_answer"],
            "keywords": doc["keywords"]
        })
    print(f"[DEBUG] Total questions loaded: {len(questions)}")
    return questions
