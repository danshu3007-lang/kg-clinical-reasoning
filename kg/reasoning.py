import networkx as nx

def score_path(G, path):
    score = 0
    for i in range(len(path) - 1):
        edge = G[path[i]][path[i+1]]
        conf = edge.get("conf", 0.5)
        rel  = edge.get("rel", "")
        if rel in ("has_symptom", "treats", "DRUGBANK::treats::Compound:Disease",
                   "GNBR::T::Compound:Disease", "Hetionet::CtD::Compound:Disease"):
            score += conf * 1.5
        else:
            score += conf
    return score / len(path)

def get_paths(G, entities, max_hops=3, top_k=5):
    candidates = []
    seen = set()

    def add_path(path):
        key = tuple(path)
        if key not in seen:
            seen.add(key)
            candidates.append({"path": path, "score": score_path(G, path)})

    entity_list = [e for e in entities if e in G]

    # 1. Direct entity-to-entity paths (most important)
    for i, e1 in enumerate(entity_list):
        for e2 in entity_list:
            if e1 == e2:
                continue
            try:
                for path in nx.all_simple_paths(G, e1, e2, cutoff=max_hops):
                    add_path(path)
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue

    # 2. symptom → disease → drug
    drugs = [n for n,d in G.nodes(data=True) if d.get("type") == "drug"]
    for entity in entity_list:
        if G.nodes[entity].get("type") == "symptom":
            for drug in drugs:
                try:
                    for path in nx.all_simple_paths(G, entity, drug, cutoff=max_hops):
                        has_disease = any(
                            G.nodes[n].get("type") == "disease"
                            for n in path[1:-1]
                        )
                        if has_disease:
                            add_path(path)
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    continue

    # 3. drug → all disease neighbors
    for entity in entity_list:
        if G.nodes[entity].get("type") == "drug":
            for neighbor in G.neighbors(entity):
                if G.nodes[neighbor].get("type") == "disease":
                    add_path([entity, neighbor])

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:top_k]

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    from kg.drkg_loader import load_drkg
    from kg.entity_linker import link_entities_drkg

    G = load_drkg()
    questions = [
        "Is metformin effective for type 2 diabetes?",
        "Does ibuprofen help with rheumatoid arthritis?",
        "Is prednisone used for asthma?",
    ]
    for q in questions:
        entities = link_entities_drkg(q, G)
        paths    = get_paths(G, entities)
        print(f"Q: {q}")
        for p in paths:
            print(f"  {' → '.join(p['path'])} (score={p['score']:.2f})")
        print()
