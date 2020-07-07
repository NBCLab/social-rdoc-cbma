import nimare as nim
from nimare.dataset import Dataset
import nibabel as nib

from nilearn.plotting import plot_stat_map

ro_mni = nim.io.convert_sleuth_to_dataset(['../data/all_coords-mni-copied.txt', '../data/all_coords-tal-copied.txt'])

meta = nim.meta.cbma.ALE()
result = meta.fit(ro_mni)
corrector = nim.correct.FWECorrector(method='montecarlo', n_iters=10000, n_cores=2)
cresult = corrector.transform(result)

for map_ in cresult.maps:
    nib.save(cresult.get_map(map_), '../results/brain-maps/ALL_SOCIAL-{0}-07.05.nii.gz'.format(map_))