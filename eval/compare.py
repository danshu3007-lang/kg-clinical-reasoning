import sys, os
sys.path.append(".")
from eval.test_questions import HARD_QUESTIONS
from kg.drkg_loader import load_drkg
from kg.entity_linker import link_entities_drkg
from kg.reasoning import get_paths
from llm.generate import generate
from baselines.llm_only import llm_only

print("Loading KG...")
G = load_drkg()

kg_results  = []
llm_results = []

print(f"\n{'Q':<55} {'Gold':<6} {'KG+LLM':<8} {'LLM':<6}")
print("-"*80)

for question, gold in HARD_QUESTIONS:
    # KG + LLM
    entities = link_entities_drkg(question, G)
    paths    = get_paths(G, entities)
    kg_answer, _, _ = generate(question, paths)
    kg_correct = kg_answer.strip().lower() == gold

    # LLM only
    llm_answer, _ = llm_only(question)
    llm_correct = llm_answer.strip().lower() == gold

    kg_results.append(kg_correct)
    llm_results.append(llm_correct)

    print(f"{question[:54]:<55} {gold:<6} {kg_answer.strip()[:7]:<8} {llm_answer.strip()[:5]:<6}")

kg_acc  = sum(kg_results)  / len(kg_results)
llm_acc = sum(llm_results) / len(llm_results)

print(f"\n{'='*80}")
print(f"KG + LLM Accuracy:  {kg_acc:.2%}  ({sum(kg_results)}/{len(kg_results)})")
print(f"LLM-only Accuracy:  {llm_acc:.2%}  ({sum(llm_results)}/{len(llm_results)})")
print(f"KG Improvement:     {(kg_acc - llm_acc):+.2%}")
