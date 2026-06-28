import sys, os
sys.path.append(".")
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def llm_only(question):
    prompt = f"""You are a biomedical question answering assistant.
Answer the following question with Yes, No, or Maybe.
Then provide a brief justification.

Question: {question}

Respond in this format:
Answer: Yes / No / Maybe
Justification: [your reasoning]"""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    content = resp.choices[0].message.content
    answer = "Maybe"
    for line in content.splitlines():
        if line.startswith("Answer:"):
            answer = line.replace("Answer:", "").strip()
            break
    return answer, content

def run_baseline(questions):
    results = []
    for q, gold in questions:
        answer, justification = llm_only(q)
        correct = answer.strip().lower() == gold.lower()
        results.append({
            "question":  q[:60],
            "gold":      gold,
            "predicted": answer.strip(),
            "correct":   correct,
        })
        print(f"gold={gold} pred={answer.strip()} correct={correct}")

    accuracy = sum(r["correct"] for r in results) / len(results)
    print(f"\nLLM-only Accuracy: {accuracy:.2%}")
    return results

if __name__ == "__main__":
    questions = [
        ("Is oseltamivir appropriate for influenza with fever and cough?", "yes"),
        ("Is metformin used for type 2 diabetes?", "yes"),
        ("Does ibuprofen treat rheumatoid arthritis?", "yes"),
        ("Is salbutamol used for asthma with shortness of breath?", "yes"),
        ("Is amoxicillin used for pneumonia?", "yes"),
        ("Is isoniazid used for tuberculosis?", "yes"),
        ("Does aspirin treat tuberculosis?", "no"),
        ("Is metformin used for asthma?", "no"),
        ("Does salbutamol treat diabetes?", "no"),
        ("Is rifampicin effective for influenza?", "no"),
    ]
    run_baseline(questions)
