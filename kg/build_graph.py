import networkx as nx

def build_graph():
    G = nx.DiGraph()

    nodes = [
        ("fever",        {"type": "symptom"}),
        ("cough",        {"type": "symptom"}),
        ("fatigue",      {"type": "symptom"}),
        ("shortness_of_breath", {"type": "symptom"}),
        ("influenza",    {"type": "disease"}),
        ("tuberculosis", {"type": "disease"}),
        ("pneumonia",    {"type": "disease"}),
        ("asthma",       {"type": "disease"}),
        ("oseltamivir",  {"type": "drug"}),
        ("isoniazid",    {"type": "drug"}),
        ("rifampicin",   {"type": "drug"}),
        ("amoxicillin",  {"type": "drug"}),
        ("salbutamol",   {"type": "drug"}),
    ]
    G.add_nodes_from(nodes)

    edges = [
        ("fever",               "influenza",    {"rel": "has_symptom",  "conf": 0.9,  "src": "manual"}),
        ("cough",               "influenza",    {"rel": "has_symptom",  "conf": 0.8,  "src": "manual"}),
        ("cough",               "tuberculosis", {"rel": "has_symptom",  "conf": 0.85, "src": "manual"}),
        ("fatigue",             "tuberculosis", {"rel": "has_symptom",  "conf": 0.7,  "src": "manual"}),
        ("fever",               "pneumonia",    {"rel": "has_symptom",  "conf": 0.75, "src": "manual"}),
        ("cough",               "pneumonia",    {"rel": "has_symptom",  "conf": 0.8,  "src": "manual"}),
        ("shortness_of_breath", "asthma",       {"rel": "has_symptom",  "conf": 0.9,  "src": "manual"}),
        ("cough",               "asthma",       {"rel": "has_symptom",  "conf": 0.75, "src": "manual"}),
        ("influenza",           "oseltamivir",  {"rel": "treats",       "conf": 0.95, "src": "manual"}),
        ("tuberculosis",        "isoniazid",    {"rel": "treats",       "conf": 0.95, "src": "manual"}),
        ("tuberculosis",        "rifampicin",   {"rel": "treats",       "conf": 0.9,  "src": "manual"}),
        ("pneumonia",           "amoxicillin",  {"rel": "treats",       "conf": 0.9,  "src": "manual"}),
        ("asthma",              "salbutamol",   {"rel": "treats",       "conf": 0.95, "src": "manual"}),
    ]
    G.add_edges_from(edges)
    return G

if __name__ == "__main__":
    G = build_graph()
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    print(f"Symptom nodes: {[n for n,d in G.nodes(data=True) if d['type']=='symptom']}")
    print(f"Drug nodes: {[n for n,d in G.nodes(data=True) if d['type']=='drug']}")
