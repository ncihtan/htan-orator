import re
import pandas as pd
from math import log, floor, ceil

from google.cloud import bigquery
bigquery_client = bigquery.Client()

import synapseclient
syn = synapseclient.Synapse()
syn.login(silent=True)

def get_bq_table ( id, id_col, component):
    #print(f'Getting {component} information from {id}')

    query = f"""
    SELECT * FROM `htan-dcc.combined_assays.{component}`
    WHERE {id_col} = '{id}'
    """

    results = bigquery_client.query(query).to_dataframe().to_dict()

    return(results)

def days_to_age (days):
    age = floor(int(days)/365)
    return(age)


def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))
    return '%.2f%s' % (number / k**magnitude, units[magnitude])

def first_lower(s):
    if not s: # Added to handle case where s == None
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
    "HTA14": "HTAN SRRS"
}

def orate(synid: str):
    '''Takes a Synapse ID of a HTAN Data File and returns a natural language description of the dataset'''
    # Get annotations
    annotations = syn.get_annotations(synid)

    # Get biospecimen information
    biospecimen_id = annotations['HTANParentBiospecimenID'][0]
    biospecimen = get_bq_table(biospecimen_id, 'HTAN_Biospecimen_Id', 'Biospecimen')


    # Extract particpant ID
    participant_id = re.match('HTA\d+\_\d+', biospecimen_id).group(0)

    # Get demographics information
    demographics = get_bq_table(participant_id, 'HTAN_Participant_Id', 'Demographics')

    # Get diagnosis information
    diagnosis = get_bq_table(participant_id, 'HTAN_Participant_Id', 'Diagnosis')

    # Look up the HTAN Center

    center_id = re.match('HTA\d+', biospecimen_id).group(0)

    if annotations['Component'][0] == 'ImagingLevel2':
        assay = annotations['ImagingAssayType'][0]
    else:
        assay = annotations['Component'][0]

    general =  (
        f"{annotations['HTANDataFileID'][0]} is a {assay} file submitted by the {htan_centers[center_id]} center "
        f"of a {first_lower(biospecimen['Acquisition_Method_Type'][0])} (Biospecimen {biospecimen_id}) "
        f"from a {days_to_age(biospecimen['Collection_Days_from_Index'][0])} year old {demographics['Gender'][0]} "
        f"(Participant {participant_id}) "
        f"diagnosed with {first_lower(diagnosis['Primary_Diagnosis'][0])}. "
    )

    if annotations['Component'][0] == 'ImagingLevel2':

        pixels = int(annotations['SizeX'][0])*int(annotations['SizeY'][0])*int(annotations['SizeZ'][0])

        imaging = (
            f"The image contains {annotations['SizeC'][0]} channels, approximately {human_format(pixels)} pixels, and measures "
            f"{ceil(int(annotations['SizeX'][0])*float(annotations['PhysicalSizeX'][0]))} {annotations['PhysicalSizeXUnit'][0]} wide "
            f"by {ceil(int(annotations['SizeY'][0])*float(annotations['PhysicalSizeY'][0]))} {annotations['PhysicalSizeYUnit'][0]} high. "
            f"It was acquired on a {annotations['Microscope'][0]} microscope at {annotations['NominalMagnification'][0]}x magnification"
        )

        oration = "\n".join([general, imaging])
    
    else:
        oration = general

    return(oration)