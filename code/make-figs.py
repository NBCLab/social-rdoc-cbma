import argparse
import numpy as np
from nilearn import datasets, surface
from nilearn.plotting import plot_stat_map, plot_surf_stat_map
from glob import glob

parser = argparse.ArgumentParser(description='Makes figures for all NiMARE-style cluster-corrected zmaps in \'map_dir\'')
parser.add_argument('map_dir', type=str,
                    help='Absolute or relative path to directory where niftis live.')
parser.add_argument('out_dir', type=str,
                    help='Absolute or relative path to directory where figures will be saved.')
parser.add_argument('--cmaps', nargs='?', 
                    help='Matplotlib colormaps to be used for the different figures.')
parser.add_argument('--nslices', type=int, 
                    help='''Number of slices in 2D slice figure 
                            (ignored if --orient=\'ortho\' or \'tiled\').
                            Default is 6.''')
parser.add_argument('--orient', type=str, 
                    help='''Orientation of slices 
                    {\'ortho\', \'tiled\', \'x\', \'y\', \'z\', \'yx\', \'xz\', \'yz\'}
                    Choose the direction of the cuts: \'x\' - sagittal, \'y\' - coronal,
                    \'z\' - axial, \'ortho\' - three cuts are performed in orthogonal
                    directions, \'tiled\' - three cuts are performed
                    and arranged in a 2x2 grid. Default is \'z\'''')
parser.add_argument('--verbose', action='store_true', 
                    help='If selected, script will narrate its progress.')
args = parser.parse_args()

if args.cmaps:
    cmaps = args.cmaps
else:
    cmaps = ['PuRd', 'BuPu','GnBu', 'BuGn', 'OrRd']

if args.orient:
    orientation = args.orient
else:
    orientation = 'z'

if args.nslices:
    nslices = args.nslices
else:
    nslices = 6

map_dir = args.map_dir
out_dir = args.out_dir

z_maps = glob('{0}/*z*cluster*.nii.gz'.format(map_dir))

#make the surface + slices plots!
fsaverage = datasets.fetch_surf_fsaverage()

coord_limits = {'z': (80,-60), 
                'y': (70,-100), 
                'x': (70,-70), 
                'yx': (0,0), 
                'yz': (0,0),
                'xz': (0,0), 
                'ortho': (0,0,0), 
                'tiled': (0,0,0)}

if len(orientation) < 2:
    cuts = []
    range_ = coord_limits[orientation][0] - coord_limits[orientation][1]
    interval = range_ / (nslices + 2)
    cut = coord_limits[orientation][0]
    for i in np.arange(0, nslices+1):
        cut -= interval
        cuts.append(np.round(cut,0))
else:
    cuts = None


for i in np.arange(0, len(z_maps)):
    basename = z_maps[i].split('/')[-1][:-7]
    g = plot_stat_map(z_maps[i], colorbar=False, threshold=1.9,
                      display_mode='z', cut_coords=cuts,
                      cmap=cmaps[i], draw_cross=False)
    g.savefig('{0}/{1}-slices.png'.format(out_dir,basename), dpi=300)
    r_texture = surface.vol_to_surf(z_maps[i], fsaverage.pial_right)
    l_texture = surface.vol_to_surf(z_maps[i], fsaverage.pial_left)
    h = plot_surf_stat_map(fsaverage.pial_right, r_texture,
                           colorbar=False, cmap=cmaps[i], threshold=2,
                           bg_map=fsaverage.sulc_right, view='medial')
    h.savefig('{0}/{1}-surf-RL.png'.format(out_dir,basename), dpi=300)
    h = plot_surf_stat_map(fsaverage.pial_right, r_texture,
                           colorbar=False, cmap=cmaps[i], threshold=2,
                           bg_map=fsaverage.sulc_right, view='lateral')
    h.savefig('{0}/{1}-surf-RM.png'.format(out_dir,basename), dpi=300)
    h = plot_surf_stat_map(fsaverage.pial_left, l_texture,
                           colorbar=False, cmap=cmaps[i], threshold=2,
                           bg_map=fsaverage.sulc_left, view='medial')
    h.savefig('{0}/{1}-surf-LM.png'.format(out_dir,basename), dpi=300)
    h = plot_surf_stat_map(fsaverage.pial_left, l_texture,
                           colorbar=False, cmap=cmaps[i], threshold=2,
                           bg_map=fsaverage.sulc_left, view='lateral')
    h.savefig('{0}/{1}-surf-LL.png'.format(out_dir,basename), dpi=300)

