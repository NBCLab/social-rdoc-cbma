# social-rdoc-cbma
Coordinate-based meta-analysis of social neuroimaging research, including a focus on NIH's RDoC social domains.

## Data
`/data` contains text files with stereotaxic coordinates from studies included in the meta-analysis, styled like UTHSCSA's Sleuth application outputs, along with the original excel files in which the corpus was curated.

## Code
`/code` contains Python scripts used to run each meta-analysis using [NiMARE](https://github.com/neurostuff/NiMARE), a Python library for coordinate- and image-based meta-analysis, along with a Python Jupyter notebook used to create figures following analyses using [Nilearn](https://nilearn.github.io/).

## Figures
`/figs` contains .png files of the results of each meta-analysis performed by the scripts in `/code`.
