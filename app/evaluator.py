# app/evaluator.py
import spacy
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_keywords(text):
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.pos_ in ("NOUN", "VERB", "PROPN")]

def match_keywords(user_answer, expected_keywords):
    user_keywords = set(extract_keywords(user_answer))
    matched = user_keywords & set(expected_keywords)
    score = len(matched) / len(expected_keywords) if expected_keywords else 0
    return matched, round(score * 100, 2)

def semantic_similarity(user_answer, expected_answer):
    embeddings = model.encode([user_answer, expected_answer], convert_to_tensor=True)
    sim_score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    return round(sim_score * 100, 2)

def evaluate_answer(user_answer, expected_answer, expected_keywords):
    matched, keyword_score = match_keywords(user_answer, expected_keywords)
    sem_score = semantic_similarity(user_answer, expected_answer)
    final = (sem_score * 0.6) + (keyword_score * 0.4)
    return {
        "final_score": round(final, 2),
        "semantic_score": sem_score,
        "keyword_score": keyword_score,
        "matched_keywords": list(matched)
    }
