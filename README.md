---
README.md:
---

# HTAN Orator

HTAN Orator is a tool for generating a natural language description of [Human Tumor Atlas Network (HTAN)](https://humantumoratlas.org/) data. The tool takes a Synapse ID of a HTAN Data File and returns a natural language description of the dataset.

## Features

- **Natural language generator**: Generates a human understandable description of a HTAN dataset given a Synapse ID.
- **BigQuery integration**: Retrieves additional information about the dataset from Google BigQuery tables.
- **Assay support**: Supports ImagingLevel2 component type and will add more types in future.

## Requirements

HTAN Orator requires Python 3.11.

Other requirements include:

- Google Cloud BigQuery Python client: Allows querying data stores on BigQuery.
- SynapseClient: Enables programmatic interaction with Synapse, a data sharing platform.
- Pandas: For data manipulation and analysis.

These can be installed by creating a Conda environment with the supplied 'environment.yml' file.

## Installation

1. Clone this repository.
2. Set up a new Conda environment using 'environment.yml':

```bash
conda env create -f environment.yml
conda activate htan-orator
```

3. Run the tool with your input Synapse ID

```bash
python orator.py <synapse_id>
```

Note: Credentials setup for Google Cloud and Synapse is required.

## Usage

You can use HTAN Orator in two ways:

1. Running the stand-alone `orator.py` script which takes a Synapse ID as input and prints a natural language text on the console.
2. As a Python module in your own Python scripts. It provides an 'orate' function that takes a Synapse ID and returns a string.

Both methods require a valid Google Cloud service account and Synapse credentials if interacting with Google's BigQuery tables or Synapse respectively.

## Examples

### Example 1: Default

Python:

```
import orator

orator.orate('syn24829433')
```

CLI:

```
python orate.py syn24829433
```

returns the following (inserted elements in <u>**_underlined bold italic_**</u>)

> '<u>**_HTA9_1_19362_**</u> is a <u>**_mIHC_**</u> file submitted by the <u>**_HTAN OHSU_**</u> center of a <u>**_biopsy_**</u> (Biospecimen<u>**_HTA9_1_17_**</u>) from a <u>**_70_**</u> year old <u>**_female_**</u> (Participant <u>**_HTA9_1_**</u>) diagnosed with <u>**_infiltrating duct carcinoma NOS_**</u>.
> The image contains <u>**12**</u> channels, approximately <u>**_8.96M_**</u> pixels, and measures <u>**_1939_**</u><u>**_µm_**</u> wide by <u>**_1157_**</u><u>**_µm_**</u> high. It was acquired on a <u>**_Leica, Aperio AT2_**</u> at <u>**_20_**</u>x magnification

### Example 2: MITI for Minerva

```
import orator

orator.orate_miti('syn24829433')
```

CLI:

```
python orate.py syn24829433 --miti
```

returns the following

> ### Diagnosis
>
> **Age at Diagnosis**: 63  
> **Primary Diagnosis**: Infiltrating duct carcinoma NOS  
> **Site of Resection or Biopsy**: Unknown  
> **Tumor Grade**: G3  
> **Stage at Diagnosis**: None
>
> ### Demographics
>
> **Species**: Human  
> **Vital Status**: Dead  
> **Cause of death**: Coming soon!  
> **Gender**: female  
> **Race**: white  
> **Ethnicity**: not hispanic or latino
>
> ### Therapy
>
> **Type**: Hormone Therapy  
> **Therapeutic agents**: Exemestane  
> **Treatment Regimen**: Exemestane  
> **Initial Disease Status**: None
>
> ### Follow Up
>
> **Progression**: Yes - Progression or Recurrence  
> **Last Known Disease Status**: Distant met recurrence/> progression  
> **Age at Follow Up**: 75  
> **Days to Progression**: Coming soon!
>
> ### Biospecimen
>
> **Acquisition Method Type**: Biopsy
>
> ## Imaging
>
> **Imaging Assay Type**: mIHC  
> **Fixative Type**: Formalin  
> **Microscope**: Leica, Aperio AT2  
> **Objective**: 20X
>
> ## Publication and Data Availability
>
> ### Associated Data:
>
> **Visit the [HTAN Data Portal](data.humantumoratlas.org) > to learn more.**
>
> ### Attribution:
>
> **Please cite the underlying data as:**  
> Coming soon!
>
> **Please cite this Minerva Story as:**  
> Coming soon!
>
> ### Associated Identifiers
>
> | ID Type                         | ID           |
> | ------------------------------- | ------------ |
> | HTAN Data File ID               | HTA9_1_19362 |
> | HTAN Participant ID             | HTA9_1       |
> | HTAN Assayed Biospecimen ID     | HTA9_1_17    |
> | HTAN Originating Biospecimen ID | HTA9_1_6     |

### Further examples

| Input       | Output                                                                                                                                                                                                                                                                                                                                                                             |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| syn24829433 | HTA9_1_19362 is a mIHC image submitted by the HTAN OHSU center of a biopsy (Biospecimen HTA9_1_17) from a 70 year old female (Participant HTA9_1) diagnosed with infiltrating duct carcinoma NOS. The image contains 12 channels, approximately 8.96M pixels, and measures 1939 µm wide by 1157 µm high. It was acquired on a Leica, Aperio AT2 at 20x magnification               |
| syn25074523 | HTA13_1_7000 is a H&E image submitted by the HTAN TNP SARDANA center of a surgical Resection (Biospecimen HTA13_1_5) from a 69 year old male (Participant HTA13_1) diagnosed with mucous adenocarcinoma. The image contains 3 channels, approximately 3.12G pixels, and measures 18638 µm wide by 17656 µm high. It was acquired on a Rarecyte;HT;3 at 20x magnification           |
| syn26642484 | HTA7_927_1002 is a t-CyCIF image submitted by the HTAN HMS center of a surgical Resection (Biospecimen HTA7_927_4) from a 40 year old year old female (Participant HTA7_927) diagnosed with adenocarcinoma NOS. The image contains 52 channels, approximately 485.63M pixels, and measures 17791 µm wide by 11533 µm high. It was acquired on a RareCyte;HT;3 at 20x magnification |
| syn24191311 | HTA10_01_10193094173699420948081950544055 is a ScRNA-seqLevel1 file submitted by the HTAN Stanford center of a surgical Resection (Biospecimen HTA10_01_023) from a 45 year old male (Participant HTA10_01) diagnosed with familial adenomatous polyposis.                                                                                                                         |

## Contributing

We welcome contributions! Please submit your changes via pull request.

## License

This project is licensed under [Insert License Name Here].

## Contact

Please raise an issue in the HTAN Orator repository if you have any questions or feedback.
