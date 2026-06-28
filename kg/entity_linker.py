SYNONYM_MAP = {
    "high temperature": "fever",
    "pyrexia":          "fever",
    "running a temperature": "fever",
    "dry cough":        "cough",
    "persistent cough": "cough",
    "tiredness":        "fatigue",
    "exhaustion":       "fatigue",
    "breathlessness":   "shortness_of_breath",
    "difficulty breathing": "shortness_of_breath",
    "flu":              "influenza",
    "tb":               "tuberculosis",
    "chest infection":  "pneumonia",
}

def link_entities(text, G):
    text_lower = text.lower()
    matched = []

    # Exact match on graph nodes
    for node in G.nodes():
        if node.replace("_", " ") in text_lower:
            matched.append(node)

    # Synonym match
    for synonym, canonical in SYNONYM_MAP.items():
        if synonym in text_lower and canonical not in matched:
            matched.append(canonical)

    return matched

if __name__ == "__main__":
    from build_graph import build_graph
    G = build_graph()

    tests = [
        "Patient has fever and dry cough",
        "Experiencing tiredness and persistent cough",
        "Difficulty breathing and cough since 2 weeks",
    ]
    for t in tests:
        print(f"Input:   {t}")
        print(f"Matched: {link_entities(t, G)}\n")
