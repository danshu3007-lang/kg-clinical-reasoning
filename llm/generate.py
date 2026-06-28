import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM = """You are a clinical reasoning assistant.
Rules:
- If knowledge graph paths are provided, use ONLY those paths to answer.
- If NO paths are provided or paths are irrelevant, use your medical knowledge but state this clearly.
- Answer Yes if the treatment/drug is appropriate for the condition.
- Answer No if the treatment/drug is NOT appropriate or wrong for the condition.
- Answer Maybe only if genuinely uncertain even with background knowledge.
- Always cite your reasoning."""

def format_paths(paths):
    if not paths:
        return "No relevant paths found in knowledge graph."
    lines = []
    for i, p in enumerate(paths):
        chain = " → ".join(p["path"])
        lines.append(f"Path {i+1} (score={p['score']:.2f}): {chain}")
    return "\n".join(lines)

def generate(question, paths):
    path_str = format_paths(paths)
    has_paths = len(paths) > 0

    prompt = f"""Question: {question}

Knowledge graph paths:
{path_str}

{"Use the paths above to answer." if has_paths else "No KG paths found. Use your medical knowledge to answer Yes or No. Do not default to Maybe unless genuinely uncertain."}

Respond in exactly this format:
Answer: Yes / No / Maybe
Justification: [cite path or medical reasoning]
Confidence: High / Medium / Low"""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": prompt}
        ]
    )
    content = resp.choices[0].message.content

    answer = "Maybe"
    for line in content.splitlines():
        if line.startswith("Answer:"):
            answer = line.replace("Answer:", "").strip()
            break

    return answer, content, paths

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    from kg.build_graph import build_graph
    from kg.entity_linker import link_entities
    from kg.reasoning import get_paths

    G = build_graph()
    question = "Is oseltamivir appropriate for a patient with fever and cough?"
    symptoms = link_entities(question, G)
    paths    = get_paths(G, symptoms)
    answer, justification, _ = generate(question, paths)
    print(f"Question: {question}\n")
    print(justification)
