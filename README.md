# social-rdoc-cbma
Coordinate-based meta-analysis of social neuroimaging research, including a focus on NIH's RDoC social domains.

## Data
`/data` contains text files with stereotaxic coordinates from studies included in the meta-analysis, styled like UTHSCSA's Sleuth application outputs, along with the original excel files in which the corpus was curated.

## Code
`/code` contains Python scripts used to run each meta-analysis using [NiMARE](https://github.com/neurostuff/NiMARE), a Python library for coordinate- and image-based meta-analysis, along with a Python Jupyter notebook used to create figures following analyses using [Nilearn](https://nilearn.github.io/).
### Instructions for ALE meta-analysis
1. To install dependencies using `pip`, run `setup.sh`.
2. Perform meta-analysis using `nimare-ales.py`:
```
usage: nimare-ales.py [-h] [--iters ITERS] [--cores CORES]
                      in_file [in_file ...] out_dir

Read in text file(s) and

positional arguments:
  in_file        Sleuth-style text files with coordinates to be meta-analyzed
                 (separate files for MNI, Talairach).
  out_dir        Absolute or relative path to directory where output (figures
                 and results) will be saved.

optional arguments:
  -h, --help     show this help message and exit
  --iters ITERS  The number of iterations the FWE corrector should run, default=10000.
  --cores CORES  Number of computational cores this to be used for meta-
                 analysis.
```


## Figures
`/figs` contains .png files of the results of each meta-analysis performed by the scripts in `/code`.
