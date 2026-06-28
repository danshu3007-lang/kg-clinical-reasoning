import sys
sys.path.append(".")
from kg.build_graph import build_graph
from kg.entity_linker import link_entities
from kg.reasoning import get_paths
from llm.generate import generate

G = build_graph()

questions = [
    "Is oseltamivir appropriate for a patient with fever and cough?",
    "What treatment is recommended for a patient with persistent cough and fatigue?",
    "Should a patient with shortness of breath and cough be given salbutamol?",
]

for q in questions:
    symptoms = link_entities(q, G)
    paths    = get_paths(G, symptoms)
    answer, justification, _ = generate(q, paths)
    print(f"Q: {q}")
    print(f"Symptoms: {symptoms}")
    print(f"Paths found: {len(paths)}")
    print(justification)
    print("-"*50)
