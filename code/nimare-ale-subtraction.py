import argparse
import os
import nimare as nim
#from nimare.dataset import Dataset
import nibabel as nib
from datetime import date
from nilearn.plotting import plot_stat_map, plot_surf_stat_map
from nilearn.surface import vol_to_surf
from nilearn.datasets import fetch_surf_fsaverage

print('NiMARE version:', nim.__version__)
print('Nibabel version:', nib.__version__)
  

parser = argparse.ArgumentParser(description='Read in text file(s) and ')
parser.add_argument('-1', '--dset1', nargs='+', type=str,
                    help='Sleuth-style text files with coordinates of first dataset (separate files for MNI, Talairach).')
parser.add_argument('-2', '--dset2', nargs='+', type=str,
                    help='Sleuth-style text files with coordinates tof second dataset (separate files for MNI, Talairach).')
parser.add_argument('--out_dir', type=str, help='Absolute or relative path to directory where output (figures and results) will be saved.')
parser.add_argument('--iters', type=int, 
                    help='The number of iterations the FWE corrector should run.')
parser.add_argument('--cores', type=int, 
                    help='Number of computational cores this to be used for meta-analysis.')
args = parser.parse_args()

sleuth1 = args.dset1
print('dset1:', sleuth1)
sleuth2 = args.dset2
print('dset2:', sleuth2)
basename = sleuth1[0].split('/')[-1][:-4] + '+' + sleuth2[0].split('/')[-1][:-4]
print(basename)
out_dir = args.out_dir
today = date.today().strftime('%d_%m_%Y')

if not os.path.exists('{0}/results'.format(out_dir)):
    os.mkdir('{0}/results'.format(out_dir))
    os.mkdir('{0}/figures'.format(out_dir))

if args.iters:
    n_iters = args.iters
else:
    n_iters = 10000

if args.cores:
    n_cores = args.cores
else:
    n_cores = 2
print(sleuth1, '\n', sleuth2, '\n', basename, '\n', out_dir, '\n', today,  '\nncores =', n_cores, '\nniters =', n_iters)

dset1 = nim.io.convert_sleuth_to_dataset(sleuth1)
dset2 = nim.io.convert_sleuth_to_dataset(sleuth2)

meta = nim.meta.ale.ALESubtraction()
result = meta.fit(dset1, dset2)
corrector = nim.correct.FWECorrector(method='montecarlo', n_iters=n_iters, n_cores=n_cores)
cresult = corrector.transform(result)
print(cresult.maps)

for map_ in cresult.maps:
    nib.save(cresult.get_map(map_), '{0}/results/{1}-{2}-{3}.nii.gz'.format(out_dir, basename, map_, today))
    try:
        g = plot_stat_map(cresult.get_map(map_), colorbar=False, title=map_, cut_coords=(0,0,0))
        g.savefig('{0}/figures/{1}-{2}-{3}.png'.format(out_dir, basename,map_, today))
    except Exception as e:
        print('Figure for {0} not made because {1}'.format(map_,e))