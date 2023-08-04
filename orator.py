import argparse
import sys
import re
import pandas as pd
from math import log, floor, ceil

from google.cloud import bigquery

bigquery_client = bigquery.Client()

import synapseclient

syn = synapseclient.Synapse()
syn.login(silent=True)


def get_bq_table(id, id_col, component, folder="combined_assays"):
    # print(f'Getting {component} information from {id}')

    query = f"""
    SELECT * FROM `htan-dcc.{folder}.{component}`
    WHERE {id_col} = '{id}'
    """

    results = bigquery_client.query(query).to_dataframe().to_dict()

    return results


def days_to_age(days):
    age = floor(int(days) / 365)
    return age


def human_format(number):
    units = ["", "K", "M", "G", "T", "P"]
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return "%.2f%s" % (number / k**magnitude, units[magnitude])


def first_lower(s):
    if not s:  # Added to handle case where s == None
        return
    else:
        return s[0].lower() + s[1:]


htan_centers = {
    "HTA1": "HTAN HTAPP",
    "HTA2": "PCAPP Pilot Project",
    "HTA3": "HTAN BU",
    "HTA4": "HTAN CHOP",
    "HTA5": "HTAN DFCI",
    "HTA6": "HTAN Duke",
    "HTA7": "HTAN HMS",
    "HTA8": "HTAN MSK",
    "HTA9": "HTAN OHSU",
    "HTA10": "HTAN Stanford",
    "HTA11": "HTAN Vanderbilt",
    "HTA12": "HTAN WUSTL",
    "HTA13": "HTAN TNP SARDANA",
    "HTA14": "HTAN TNP - TMA",
    "HTA14": "HTAN SRRS",
}


def orate(synid: str):
    """Takes a Synapse ID of a HTAN Data File and returns a natural language description of the dataset"""
    # Get annotations
    annotations = syn.get_annotations(synid)

    # Get biospecimen information
    biospecimen_id = annotations["HTANParentBiospecimenID"][0]
    biospecimen = get_bq_table(biospecimen_id, "HTAN_Biospecimen_Id", "Biospecimen")

    # Extract particpant ID
    participant_id = re.match("HTA\d+\_\d+", biospecimen_id).group(0)

    # Get demographics information
    demographics = get_bq_table(participant_id, "HTAN_Participant_Id", "Demographics")

    # Get diagnosis information
    diagnosis = get_bq_table(participant_id, "HTAN_Participant_Id", "Diagnosis")

    # Look up the HTAN Center

    center_id = re.match("HTA\d+", biospecimen_id).group(0)

    if annotations["Component"][0] == "ImagingLevel2":
        assay = annotations["ImagingAssayType"][0]
    else:
        assay = annotations["Component"][0]

    general = (
        f"{annotations['HTANDataFileID'][0]} is a {assay} file submitted by the {htan_centers[center_id]} center "
        f"of a {first_lower(biospecimen['Acquisition_Method_Type'][0])} (Biospecimen {biospecimen_id}) "
        f"from a {days_to_age(biospecimen['Collection_Days_from_Index'][0])} year old {demographics['Gender'][0]} "
        f"(Participant {participant_id}) "
        f"with a primary diagnosis of \"{diagnosis['Primary_Diagnosis'][0]}.\""
    )

    if annotations["Component"][0] == "ImagingLevel2":
        pixels = (
            int(annotations["SizeX"][0])
            * int(annotations["SizeY"][0])
            * int(annotations["SizeZ"][0])
        )

        imaging = (
            f"The image contains {annotations['SizeC'][0]} channels, approximately {human_format(pixels)} pixels, and measures "
            f"{ceil(int(annotations['SizeX'][0])*float(annotations['PhysicalSizeX'][0]))} {annotations['PhysicalSizeXUnit'][0]} wide "
            f"by {ceil(int(annotations['SizeY'][0])*float(annotations['PhysicalSizeY'][0]))} {annotations['PhysicalSizeYUnit'][0]} high. "
            f"It was acquired on a {annotations['Microscope'][0]} microscope at {annotations['NominalMagnification'][0]}x magnification."
        )

        oration = "\n".join([general, imaging])

    else:
        oration = general

    return oration


def orate_miti(synid: str):
    """Takes a Synapse ID of a HTAN Data File and returns a natural language description of the dataset"""
    # Get annotations
    annotations = syn.get_annotations(synid)

    # Get biospecimen information
    assayed_id = annotations["HTANParentBiospecimenID"][0]
    biospecimen = get_bq_table(assayed_id, "HTAN_Biospecimen_Id", "Biospecimen")

    # Extract particpant ID
    participant_id = re.match("HTA\d+\_\d+", assayed_id).group(0)

    # Get demographics information
    demographics = get_bq_table(participant_id, "HTAN_Participant_Id", "Demographics")

    # Get diagnosis information
    diagnosis = get_bq_table(participant_id, "HTAN_Participant_Id", "Diagnosis")

    # Get diagnosis information
    therapy = get_bq_table(participant_id, "HTAN_Participant_Id", "Therapy")

    molecular_test = get_bq_table(
        participant_id, "HTAN_Participant_Id", "MolecularTest"
    )

    provenance = get_bq_table(
        assayed_id,
        "HTAN_Assayed_Biospecimen_Id",
        "biospecimen_ids",
        folder="id_provenance",
    )

    # Look up the HTAN Center

    center_id = re.match("HTA\d+", assayed_id).group(0)

    if annotations["Component"][0] == "ImagingLevel2":
        assay = annotations["ImagingAssayType"][0]
    else:
        assay = annotations["Component"][0]

    # prepare values
    dictionary = {
        "age_at_diagnosis": days_to_age(diagnosis["Age_at_Diagnosis"][0]),
        "primary_diagnosis": diagnosis["Primary_Diagnosis"][0],
        "site_of_resection_or_biopsy": "Unknown",  # not exposed in htan-dcc.combined_assays.Biospecimen at the moment,
        "tumor_grade": diagnosis["Tumor_Grade"][0],
        "stage_at_diagnosis": diagnosis["AJCC_Pathologic_Stage"][0],
        "species": "Human",
        "vital_status": demographics["Vital_Status"][0],
        "cause_of_death": "Coming soon!",  # not exposed in htan-dcc.combined_assays.Demographics at the moment
        "gender": demographics["Gender"][0],
        "race": demographics["Race"][0],
        "ethnicity": demographics["Ethnicity"][0],
        "therapy_type": therapy["Treatment_Type"][0],
        "therapy_agents": therapy["Therapeutic_Agents"][0],
        "therapy_regimen": therapy["Regimen_or_Line_of_Therapy"][0],
        "initial_disease_status": therapy["Initial_Disease_Status"][0],
        "progression": diagnosis["Progression_or_Recurrence"][0],
        "last_known_disease_status": diagnosis["Last_Known_Disease_Status"][0],
        "age_at_follow_up": days_to_age(
            int(diagnosis["Age_at_Diagnosis"][0])
            + int(diagnosis["Days_to_Last_Follow_up"][0])
        ),
        "days_to_progression": "Coming soon!",  # not exposed in htan-dcc.combined_assays.Diagnosis at the moment
        "biospecimen_type": biospecimen["Acquisition_Method_Type"][0],
        "fixative_type": biospecimen["Fixative_Type"][0],
        "imaging_assay_type": annotations["ImagingAssayType"][0],
        "microscope": annotations["Microscope"][0],
        "objective": f"{annotations['NominalMagnification'][0]}X {annotations['Objective'][0]}",
        "data_citation": "Coming soon!",
        "story_citation": "Coming soon!",
        "htan_center": htan_centers[center_id],
        "data_file_id": annotations["HTANDataFileID"][0].replace("_", "\_"),
        "participant_id": provenance["HTAN_Participant_ID"][0].replace("_", "\_"),
        "assayed_id": annotations["HTANParentBiospecimenID"][0].replace("_", "\_"),
        "originating_id": provenance["HTAN_Originating_Biospecimen_ID"][0].replace(
            "_", "\_"
        ),
    }

    if dictionary["vital_status"] != "Dead":
        dictionary["cause_of_death"] = "Not applicable"

    with open("miti_fstring.md") as file:
        miti_fstring = file.read()

    formatted = miti_fstring.format(**dictionary)
    # user_input = "The answer is {foo} and {bar}"
    # namespace = {'foo': 42, 'bar': 'spam, spam, spam, ham and eggs'}
    # formatted = user_input.format(**namespace)

    return formatted


def main():
    parser = argparse.ArgumentParser(
        description="Run orate or orate_miti function based on the provided arguments"
    )
    parser.add_argument(
        "synid",
        help="Input entity ID. Must have bene annotated with HTAN Imaging Level 2 templates",
    )
    parser.add_argument(
        "--miti",
        action="store_true",
        help="If present, runs the orate_miti function. If not, runs the orate function.",
    )

    args = parser.parse_args()

    if args.miti:
        miti = orate_miti(args.synid)
        print(miti)
    else:
        oration = orate(args.synid)
        print(oration)


if __name__ == "__main__":
    main()
