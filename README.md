# HTAN Orator

This repo holds scripts to describe HTAN data in natural language

## Requirements

Module requirements in the conda environment.yml file

Requires `syn.login()` to pass (eg with credentials in `~/.synapseCreds`)  
Requires `bigquery.Client()` to authenticate to the `htan-dcc` project

## Usage

```
import orator

orator.orate('syn24829433')
```

returns the following (inserted elements in <u>***underlined bold italic***</u>)

>'<u>***HTA9_1_19362***</u> is a <u>***mIHC***</u> file submitted by the <u>***HTAN OHSU***</u> center of a <u>***biopsy***</u> (Biospecimen<u>***HTA9_1_17***</u>) from a <u>***70***</u> year old <u>***female***</u> (Participant <u>***HTA9_1***</u>) diagnosed with <u>***infiltrating duct carcinoma NOS***</u>. 
The image contains <u>**12**</u> channels, approximately <u>***8.96M***</u> pixels, and measures <u>***1939***</u><u>***µm***</u> wide by <u>***1157***</u><u>***µm***</u> high. It was acquired on a <u>***Leica, Aperio AT2***</u> at <u>***20***</u>x magnification

Other examples

| Input | Output |
| ----  | --- |
| syn24829433 | HTA9_1_19362 is a mIHC image submitted by the HTAN OHSU center of a biopsy (Biospecimen HTA9_1_17) from a 70 year old female (Participant HTA9_1) diagnosed with infiltrating duct carcinoma NOS. The image contains 12 channels, approximately 8.96M pixels, and measures 1939 µm wide by 1157 µm high. It was acquired on a Leica, Aperio AT2 at 20x magnification |
| syn25074523 | HTA13_1_7000 is a H&E image submitted by the HTAN TNP SARDANA center of a surgical Resection (Biospecimen HTA13_1_5) from a 69 year old male (Participant HTA13_1) diagnosed with mucous adenocarcinoma. The image contains 3 channels, approximately 3.12G pixels, and measures 18638 µm wide by 17656 µm high. It was acquired on a Rarecyte;HT;3 at 20x magnification|
| syn26642484 | HTA7_927_1002 is a t-CyCIF image submitted by the HTAN HMS center of a surgical Resection (Biospecimen HTA7_927_4) from a 40 year old year old female (Participant HTA7_927) diagnosed with adenocarcinoma NOS. The image contains 52 channels, approximately 485.63M pixels, and measures 17791 µm wide by 11533 µm high. It was acquired on a RareCyte;HT;3 at 20x magnification |
| syn24191311 | HTA10_01_10193094173699420948081950544055 is a ScRNA-seqLevel1 file submitted by the HTAN Stanford center of a surgical Resection (Biospecimen HTA10_01_023) from a 45 year old male (Participant HTA10_01) diagnosed with familial adenomatous polyposis. |

### Conda environment

To replicate the environment use

```
conda create --name htan-orator --file environment.yml
```

then activate the environment

```
conda activate htan-orator
```