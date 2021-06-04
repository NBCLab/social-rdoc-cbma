import argparse
import os
import nimare as nim
#from nimare.dataset import Dataset
import nibabel as nib
from datetime import date
from nilearn.plotting import plot_stat_map, plot_surf_stat_map
from nilearn.surface import vol_to_surf
from nilearn.datasets import fetch_surf_fsaverage
from nimare.dataset import Dataset

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
args = parser.parse_args()

dset1 = args.dset1
print('dset1:', dset1)
dset2 = args.dset2
print('dset2:', dset2)
basename = dset1[0].split('/')[-1][:-4] + '+' + dset2[0].split('/')[-1][:-4]
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

print(dset1, '\n', dset2, '\n', basename, '\n', out_dir, '\n', today, '\nniters =', n_iters)

if any('.txt' in string for string in dset1):
    print('Converting Sleuth coordinate file to NiMARE dataset...')
    dset1 = nim.io.convert_sleuth_to_dataset(dset1)

elif any('.pkl' in string for string in dset1):
    print('Converting pickled dataset file to NiMARE dataset...')
    dset1 = Dataset.load(dset1[0])

if any('.txt' in string for string in dset2):
    print('Converting Sleuth coordinate file to NiMARE dataset...')
    dset2 = nim.io.convert_sleuth_to_dataset(dset2)

elif any('.pkl' in string for string in dset2):
    print('Converting pickled dataset file to NiMARE dataset...')
    dset2 = Dataset.load(dset2[0])

print('Starting subtraction analysis...')
meta = nim.meta.ale.ALESubtraction(n_iters=n_iters)
result = meta.fit(dset1, dset2)
print(result.maps)

for map_ in result.maps:
    nib.save(result.get_map(map_), '{0}/results/{1}-{2}-{3}.nii.gz'.format(out_dir, basename, map_, today))
    try:
        g = plot_stat_map(result.get_map(map_), colorbar=False, title=map_, cut_coords=(0,0,0))
        g.savefig('{0}/figures/{1}-{2}-{3}.png'.format(out_dir, basename,map_, today))
    except Exception as e:
        print('Figure for {0} not made because {1}'.format(map_,e))
