# social-rdoc-cbma
Coordinate-based meta-analysis of social neuroimaging research, including a focus on NIH's RDoC social domains.

## Data
`/data` contains text files with stereotaxic coordinates from studies included in the meta-analysis, styled like UTHSCSA's Sleuth application outputs, along with the original excel files in which the corpus was curated.

## Code
`/code` contains Python scripts used to run each meta-analysis using [NiMARE](https://github.com/neurostuff/NiMARE), a Python library for coordinate- and image-based meta-analysis, along with a Python Jupyter notebook used to create figures following analyses using [Nilearn](https://nilearn.github.io/).
### Instructions for ALE meta-analysis
1. Download this repository (or at least the `code` folder) and prepare your Sleuth-style text file with all coordinates for your meta-analysis.
2. To install dependencies using `pip`, run `setup.sh`.
3. Perform meta-analysis using `nimare-ales.py`:
```
usage: nimare-ales.py [-h] [--iters ITERS] [--cores CORES]
                      in_file [in_file ...] out_dir

Read in text file(s) and

positional arguments:
  in_file        Sleuth-style text file(s) with coordinates to be meta-analyzed
                 (separate files for MNI, Talairach).
  out_dir        Absolute or relative path to directory where output (figures
                 and results) will be saved.

optional arguments:
  -h, --help     show this help message and exit
  --iters ITERS  The number of iterations the FWE corrector should run, default=10000.
  --cores CORES  Number of computational cores this to be used for meta-
                 analysis.
```
4. Make surface + slice figures with `make-figs.py`:
```
usage: make-figs.py [-h] [--cmaps [CMAPS]] [--nslices NSLICES]
                    [--orient ORIENT] [--verbose]
                    map_dir out_dir

Makes figures for all NiMARE-style cluster-corrected zmaps in 'map_dir'

positional arguments:
  map_dir            Absolute or relative path to directory where niftis live.
  out_dir            Absolute or relative path to directory where figures will
                     be saved.

optional arguments:
  -h, --help         show this help message and exit
  --cmaps [CMAPS]    Matplotlib colormaps to be used for the different
                     figures.
  --nslices NSLICES  Number of slices in 2D slice figure (ignored if
                     --orient='ortho' or 'tiled'). Default is 6.
  --orient ORIENT    Orientation of slices {'ortho', 'tiled', 'x', 'y', 'z',
                     'yx', 'xz', 'yz'} Choose the direction of the cuts: 'x' -
                     sagittal, 'y' - coronal, 'z' - axial, 'ortho' - three
                     cuts are performed in orthogonal directions, 'tiled' -
                     three cuts are performed and arranged in a 2x2 grid.
                     Default is 'z'
  --verbose          If selected, script will narrate its progress. 
```
5. Compare patterns of convergent activation with `nimare-ale-subtraction.py`
```
usage: nimare-ale-subtraction.py [-h] [-1 DSET1 [DSET1 ...]]
                                 [-2 DSET2 [DSET2 ...]] [--out_dir OUT_DIR]
                                 [--iters ITERS]

Read in text or dataset files and perform an activation likelihood estimation
subtraction analysis to compare patterns of convergent activation between
meta-analytic datasets.

optional arguments:
  -h, --help            show this help message and exit
  -1 DSET1 [DSET1 ...], --dset1 DSET1 [DSET1 ...]
                        Sleuth-style text file(s) with coordinates of first
                        dataset (separate files for MNI, Talairach) OR a
                        gzipped, pickled file (`.pkl.gz`) containing both MNI
                        and Talairach coordinateds.
  -2 DSET2 [DSET2 ...], --dset2 DSET2 [DSET2 ...]
                        Sleuth-style text files with coordinates tof second
                        dataset (separate files for MNI, Talairach) OR a
                        gzipped, pickled file (`.pkl.gz`) containing both MNI
                        and Talairach coordinateds..
  --out_dir OUT_DIR     Absolute or relative path to directory where output
                        (figures and results) will be saved.
  --iters ITERS         The number of iterations the FWE corrector should run.
```
Overall, you can use the code included here to run a meta-analysis and make figures with 3 commands, once you've prepared your Sleuth-style coordinate text files, navigate to the folder in which you've saved the `code` folder and run the following commands in a command line (e.g., Terminal on MacOS):
```
bash code/setup.sh
python code/nimare-ales.py /path/to/sleuth_file-mni.txt /path/to/sleuth_file-tal.txt /path/to/output-directory
python code/make-figs.py /path/to/output-directory/results /path/to/output-directory/figures
# optionally
python code/nimare-ale-subtraction.py -1 /path/to/dataset1_file [/path/to/dataset1_file2 ...] -2 /path/to/dataset2_file [/path/to/dataset2_file2 ...] /path/to/output-directory
```
All other arguments are optional and without them, you'll run a perfectly good ALE meta-analysis. Make sure you replace all the `path/to/...` with file paths to your text files and to your output directory, respectively.

## Figures
`/figs` contains .png files of the results of each meta-analysis performed by the scripts in `/code`.
