import sys, json, os
sys.path.append(".")
from kg.build_graph import build_graph
from kg.entity_linker import link_entities
from kg.reasoning import get_paths
from llm.generate import generate

def path_coverage(justification, path):
    hits = sum(1 for node in path if node.lower() in justification.lower())
    return hits / len(path)

def run_eval(n_samples=20):
    print("Loading PubMedQA...")
    with open("data/ori_pqal.json") as f:
        raw = json.load(f)

    items = list(raw.items())[:n_samples]
    G = build_graph()
    results = []

    for i, (pmid, ex) in enumerate(items):
        question   = ex["QUESTION"]
        gold_label = ex["final_decision"]

        symptoms = link_entities(question, G)
        paths    = get_paths(G, symptoms)
        answer, justification, _ = generate(question, paths)

        correct  = answer.strip().lower() == gold_label.strip().lower()
        coverage = max(
            (path_coverage(justification, p["path"]) for p in paths),
            default=0
        )

        results.append({
            "question":    question[:60],
            "gold":        gold_label,
            "predicted":   answer.strip(),
            "correct":     correct,
            "coverage":    round(coverage, 2),
            "paths_found": len(paths),
        })

        print(f"[{i+1}/{n_samples}] gold={gold_label} pred={answer.strip()} correct={correct} paths={len(paths)}")

    accuracy     = sum(r["correct"]  for r in results) / len(results)
    avg_coverage = sum(r["coverage"] for r in results) / len(results)
    abstain_rate = sum(1 for r in results if r["predicted"].lower() == "maybe") / len(results)

    print(f"\n{'='*40}")
    print(f"Samples:      {n_samples}")
    print(f"Accuracy:     {accuracy:.2%}")
    print(f"Avg Coverage: {avg_coverage:.2%}")
    print(f"Abstain Rate: {abstain_rate:.2%}")
    return results

if __name__ == "__main__":
    run_eval(n_samples=20)
