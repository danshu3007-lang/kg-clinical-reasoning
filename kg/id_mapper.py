# Manual mapping of DRKG IDs to readable names
# Add more as needed based on PubMedQA questions

DRUGBANK_TO_NAME = {
    "db00945": "aspirin",
    "db00316": "acetaminophen",
    "db00563": "methotrexate",
    "db00331": "metformin",
    "db00398": "sibutramine",
    "db00999": "hydrochlorothiazide",
    "db00681": "amphotericin_b",
    "db01234": "dexamethasone",
    "db00635": "prednisone",
    "db00783": "estradiol",
    "db00741": "hydrocortisone",
    "db00993": "azathioprine",
    "db00280": "disopyramide",
    "db00176": "fluvoxamine",
    "db00477": "chlorpromazine",
    "db00289": "atomoxetine",
    "db00758": "clopidogrel",
    "db01050": "ibuprofen",
    "db00328": "indomethacin",
    "db00503": "ritonavir",
    "db00709": "lamivudine",
    "db00755": "tretinoin",
    "db00495": "zidovudine",
    "db00198": "oseltamivir",
    "db01082": "streptomycin",
    "db00951": "isoniazid",
    "db01045": "rifampicin",
    "db01234": "dexamethasone",
    "db00693": "fluorouracil",
    "db00773": "etoposide",
}

MESH_TO_NAME = {
    "mesh:d003550": "cystic_fibrosis",
    "mesh:d013167": "speech_disorders",
    "mesh:d006086": "graft_rejection",
    "mesh:d001249": "asthma",
    "mesh:d003920": "diabetes_mellitus",
    "mesh:d003924": "type2_diabetes",
    "mesh:d006973": "hypertension",
    "mesh:d009765": "obesity",
    "mesh:d000755": "anemia_sickle_cell",
    "mesh:d006333": "heart_failure",
    "mesh:d007333": "insulin_resistance",
    "mesh:d011014": "pneumonia",
    "mesh:d014376": "tuberculosis",
    "mesh:d007239": "infections",
    "mesh:d009369": "neoplasms",
    "mesh:d002318": "cardiovascular_diseases",
    "mesh:d001714": "bipolar_disorder",
    "mesh:d003866": "depressive_disorder",
    "mesh:d012559": "schizophrenia",
    "mesh:d000544": "alzheimer_disease",
    "mesh:d010300": "parkinson_disease",
    "mesh:d006261": "headache",
    "mesh:d008103": "liver_cirrhosis",
    "mesh:d003550": "cystic_fibrosis",
    "mesh:d006937": "hypercholesterolemia",
    "mesh:d001172": "arthritis_rheumatoid",
    "mesh:d009103": "multiple_sclerosis",
    "mesh:d015179": "colorectal_neoplasms",
    "mesh:d001943": "breast_neoplasms",
    "mesh:d008175": "lung_neoplasms",
}

def get_readable_name(node_id):
    node_lower = node_id.lower()
    if node_lower in DRUGBANK_TO_NAME:
        return DRUGBANK_TO_NAME[node_lower]
    if node_lower in MESH_TO_NAME:
        return MESH_TO_NAME[node_lower]
    return node_id  # return as-is if no mapping

if __name__ == "__main__":
    tests = ["db00331", "mesh:d003924", "db01050", "mesh:d001249"]
    for t in tests:
        print(f"{t} -> {get_readable_name(t)}")
