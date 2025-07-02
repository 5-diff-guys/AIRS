from fastapi import FastAPI
from app.models import DomainRequest
from app.interview_bot import InterviewBot
from app.question_bank import load_questions_by_domain

app = FastAPI()
bot = None

@app.post("/start_interview")
async def start_interview(data: DomainRequest):
    global bot
    questions = await load_questions_by_domain(data.domain)
    if not questions:
        return {"error": f"No questions found for domain: {data.domain}"}
    bot = InterviewBot(questions)
    return {"message": f"Interview started with {len(questions)} questions in {data.domain}"}
