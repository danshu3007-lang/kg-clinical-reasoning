SYNONYM_MAP = {
    "high temperature": "fever",
    "pyrexia":          "fever",
    "febrile":          "fever",
    "dry cough":        "cough",
    "persistent cough": "cough",
    "chronic cough":    "cough",
    "tiredness":        "fatigue",
    "exhaustion":       "fatigue",
    "weakness":         "fatigue",
    "breathlessness":   "shortness_of_breath",
    "difficulty breathing": "shortness_of_breath",
    "dyspnea":          "shortness_of_breath",
    "dyspnoea":         "shortness_of_breath",
    "flu":              "influenza",
    "tb":               "tuberculosis",
    "chest infection":  "pneumonia",
    "bronchial asthma": "asthma",
    "tamiflu":          "oseltamivir",
    "ventolin":         "salbutamol",
    "albuterol":        "salbutamol",
    "rifampin":         "rifampicin",
    "inh":              "isoniazid",
}

DRKG_SYNONYM_MAP = {
    "type 2 diabetes":      "type2_diabetes",
    "type2 diabetes":       "type2_diabetes",
    "t2dm":                 "type2_diabetes",
    "diabetes mellitus":    "diabetes_mellitus",
    "diabetes":             "type2_diabetes",
    "rheumatoid arthritis": "arthritis_rheumatoid",
    "heart failure":        "heart_failure",
    "high blood pressure":  "hypertension",
    "blood pressure":       "hypertension",
    "depression":           "depressive_disorder",
    "alzheimer":            "alzheimer_disease",
    "parkinson":            "parkinson_disease",
    "multiple sclerosis":   "multiple_sclerosis",
    "breast cancer":        "breast_neoplasms",
    "lung cancer":          "lung_neoplasms",
    "colon cancer":         "colorectal_neoplasms",
    "colorectal cancer":    "colorectal_neoplasms",
    "bipolar":              "bipolar_disorder",
    "obesity":              "obesity",
    "cholesterol":          "hypercholesterolemia",
    "cirrhosis":            "liver_cirrhosis",
    "metformin":            "metformin",
    "ibuprofen":            "ibuprofen",
    "prednisone":           "prednisone",
    "dexamethasone":        "dexamethasone",
    "aspirin":              "aspirin",
    "acetaminophen":        "acetaminophen",
    "hypertension":         "hypertension",
    "schizophrenia":        "schizophrenia",
}

def link_entities(text, G):
    text_lower = text.lower()
    matched = []
    for node in G.nodes():
        if node.replace("_", " ") in text_lower and node not in matched:
            matched.append(node)
    for synonym, canonical in SYNONYM_MAP.items():
        if synonym in text_lower and canonical not in matched:
            matched.append(canonical)
    return matched

def link_entities_drkg(text, G):
    text_lower = text.lower()
    matched = []

    # DRKG-aware synonyms first
    for synonym, canonical in DRKG_SYNONYM_MAP.items():
        if synonym in text_lower and canonical not in matched:
            if G.has_node(canonical):
                matched.append(canonical)

    # Exact node match
    for node in G.nodes():
        if node.replace("_", " ") in text_lower and node not in matched:
            matched.append(node)

    # Original synonyms
    for synonym, canonical in SYNONYM_MAP.items():
        if synonym in text_lower and canonical not in matched:
            matched.append(canonical)

    return matched

if __name__ == "__main__":
    from kg.build_graph import build_graph
    G = build_graph()
    tests = [
        "Patient has fever and dry cough",
        "Is metformin effective for type 2 diabetes?",
        "Does ibuprofen help with rheumatoid arthritis?",
    ]
    for t in tests:
        print(f"Input:   {t}")
        print(f"Matched: {link_entities_drkg(t, G)}\n")
