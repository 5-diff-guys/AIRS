# app/interview_bot.py
from app.evaluator import evaluate_answer

class InterviewBot:
    def __init__(self, question_bank):
        self.questions = question_bank
        self.index = 0
        self.scores = []

    def get_question(self):
        if self.index < len(self.questions):
            return self.questions[self.index]["question"]
        return None

    def submit(self, user_answer):
        q = self.questions[self.index]
        result = evaluate_answer(user_answer, q["expected_answer"], q["keywords"])
        self.scores.append(result["final_score"])
        self.index += 1
        return result

    def is_done(self):
        return self.index >= len(self.questions)

    def get_summary(self):
        avg = sum(self.scores) / len(self.scores) if self.scores else 0
        return {"average": round(avg, 2), "questions_answered": len(self.scores)}
