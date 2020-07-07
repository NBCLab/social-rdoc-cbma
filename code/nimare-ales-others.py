import nimare as nim
import nibabel as nib
from nilearn.plotting import plot_stat_map

ro_mni = nim.io.convert_sleuth_to_dataset(['../data/others_mni_copied.txt', '../data/others_tal_copied.txt'])

meta = nim.meta.cbma.ALE()
result = meta.fit(ro_mni)
corrector = nim.correct.FWECorrector(method='montecarlo', n_iters=10000, n_cores=2)
cresult = corrector.transform(result)

for map_ in cresult.maps:
    nib.save(cresult.get_map(map_), 'ro_flux_{0}-OTHERS.nii.gz'.format(map_))