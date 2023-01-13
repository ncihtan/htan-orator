# HTAN Orator

This repo holds scripts to describe HTAN data in natural language

# Usage

**currently only in Jupyter notebook**

```
orate('syn24829433')
```

returns

> 'HTA9_1_19362 is a mIHC image of a biopsy (Biospecimen HTA9_1_17) from a 70 female (Participant HTA9_1) diagnosed with infiltrating duct carcinoma NOS. The image contains 12 channels, approximately 8.96M pixels, and measures 1939 µm wide by 1157 µm high'


### Conda environment

To replicate the environment use

```
conda create --name htan-orator --file environment.yml
```

then activate the environment

```
conda activate htan-orator
```