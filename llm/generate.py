import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM = """You are a clinical reasoning assistant.
Rules:
- Use ONLY the provided knowledge graph paths.
- Do NOT add medical facts not present in the paths.
- If paths are insufficient to answer confidently, answer Maybe.
- Always cite the exact path in your justification."""

def format_paths(paths):
    lines = []
    for i, p in enumerate(paths):
        chain = " → ".join(p["path"])
        lines.append(f"Path {i+1} (score={p['score']:.2f}): {chain}")
    return "\n".join(lines)

def generate(question, paths):
    if not paths:
        return "Maybe", "No relevant paths found in knowledge graph.", []

    path_str = format_paths(paths)
    prompt = f"""Question: {question}

Knowledge graph paths:
{path_str}

Respond in exactly this format:
Answer: Yes / No / Maybe
Justification: [cite the exact path used]
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
