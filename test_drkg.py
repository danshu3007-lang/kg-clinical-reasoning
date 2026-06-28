import sys
sys.path.append(".")
from kg.drkg_loader import load_drkg
from kg.entity_linker import link_entities_drkg
from kg.reasoning import get_paths
from llm.generate import generate

G = load_drkg()

questions = [
    "Is metformin effective for type 2 diabetes?",
    "Does ibuprofen help with rheumatoid arthritis?",
    "Is prednisone used for asthma treatment?",
    "Does aspirin reduce cardiovascular disease risk?",
]

for q in questions:
    entities = link_entities_drkg(q, G)
    paths    = get_paths(G, entities)
    answer, justification, _ = generate(q, paths)
    print(f"Q: {q}")
    print(f"Entities: {entities}")
    print(f"Paths: {len(paths)}")
    print(justification)
    print("-"*50)
