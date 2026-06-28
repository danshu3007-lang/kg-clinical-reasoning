import csv
import sys
sys.path.append(".")
from kg.build_graph import build_graph
from kg.id_mapper import get_readable_name

ALLOWED_RELATIONS = {
    "GNBR::T::Compound:Disease",
    "GNBR::C::Compound:Disease",
    "GNBR::Sa::Compound:Disease",
    "GNBR::Pa::Compound:Disease",
    "DRUGBANK::treats::Compound:Disease",
    "Hetionet::CtD::Compound:Disease",
    "Hetionet::CpD::Compound:Disease",
}

def load_drkg(path="data/drkg.tsv", max_rows=6000000):
    print(f"Loading DRKG from {path}...")
    G = build_graph()
    added = 0

    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")
        for i, row in enumerate(reader):
            if i >= max_rows:
                break
            if len(row) != 3:
                continue

            src, rel, dst = row
            if rel not in ALLOWED_RELATIONS:
                continue

            src_id = src.split("::")[-1].lower()
            dst_id = dst.split("::")[-1].lower()

            src_clean = get_readable_name(src_id).replace(" ", "_")
            dst_clean = get_readable_name(dst_id).replace(" ", "_")

            if "Compound" in src:
                src_type = "drug"
                dst_type = "disease"
            else:
                src_type = "disease"
                dst_type = "drug"

            if not G.has_node(src_clean):
                G.add_node(src_clean, type=src_type)
            if not G.has_node(dst_clean):
                G.add_node(dst_clean, type=dst_type)

            G.add_edge(src_clean, dst_clean, rel=rel, conf=0.8, src="drkg")
            added += 1

    print(f"Added {added} edges from DRKG")
    print(f"Total nodes: {G.number_of_nodes()}")
    print(f"Total edges: {G.number_of_edges()}")
    return G

if __name__ == "__main__":
    G = load_drkg()
    # Show some readable nodes
    drugs = [(n,d) for n,d in G.nodes(data=True) if d.get("type")=="drug"][:10]
    diseases = [(n,d) for n,d in G.nodes(data=True) if d.get("type")=="disease"][:10]
    print("\nSample drugs:", [n for n,d in drugs])
    print("Sample diseases:", [n for n,d in diseases])
