import networkx as nx

def score_path(G, path):
    score = 0
    for i in range(len(path) - 1):
        edge = G[path[i]][path[i+1]]
        rel  = edge.get("rel", "")
        conf = edge.get("conf", 0.5)
        if rel in ("has_symptom", "treats"):
            score += conf * 1.5
        else:
            score += conf
    return score / len(path)

def get_paths(G, symptoms, max_hops=3, top_k=5):
    drugs = [n for n,d in G.nodes(data=True) if d.get("type") == "drug"]
    candidates = []

    for symptom in symptoms:
        if symptom not in G:
            continue
        for drug in drugs:
            try:
                for path in nx.all_simple_paths(G, symptom, drug, cutoff=max_hops):
                    # Only keep paths that go through a disease node
                    has_disease = any(
                        G.nodes[n].get("type") == "disease"
                        for n in path[1:-1]
                    )
                    if has_disease:
                        candidates.append({
                            "path":  path,
                            "score": score_path(G, path)
                        })
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:top_k]

if __name__ == "__main__":
    from build_graph import build_graph
    from entity_linker import link_entities

    G = build_graph()
    test = "Patient has fever and dry cough"
    symptoms = link_entities(test, G)
    print(f"Symptoms: {symptoms}")

    paths = get_paths(G, symptoms)
    print(f"\nTop paths:")
    for p in paths:
        print(f"  {' → '.join(p['path'])}  (score={p['score']:.2f})")
