import os
import os.path as op
import argparse
import numpy as np
import nibabel as nib
from nimare.io import convert_sleuth_to_dataset
from nimare.meta.cbma import ALE, ALESubtraction
from nimare.meta.kernel import ALEKernel
from glob import glob
from utils import get_peaks, thresh_img, plot_dendrogram
from nimare.meta.kernel import ALEKernel
from nilearn.connectome import ConnectivityMeasure
from nilearn import masking
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from nimare.correct import FWECorrector
from subtraction import subtraction_analysis


project_dir = '/home/data/nbc/misc-projects/meta-analyses/meta-analysis_social-rdoc/clustering'

for coding in ['Pure', 'Co-coded']:
    files_dir = op.join(project_dir, 'code', 'text-files', coding)

    affiliation = sorted(glob(op.join(project_dir, 'code', 'text-files', coding, '*Affiliation*.txt')))
    other = sorted(glob(op.join(project_dir, 'code', 'text-files', coding, '*Others*.txt')))
    self = sorted(glob(op.join(project_dir, 'code', 'text-files', coding, '*Self*.txt')))
    soccomm = sorted(glob(op.join(project_dir, 'code', 'text-files', coding, '*Soc_Comm*.txt')))

    for tmp_txts in [affiliation, other, self, soccomm]:
        prefix = '_'.join(op.basename(tmp_txts[0]).split('_')[:-1])
        print(prefix)

        output_dir = op.join(project_dir, 'derivatives', 'ale', prefix)
        os.makedirs(output_dir, exist_ok=True)

        dset = convert_sleuth_to_dataset(tmp_txts, target="mni152_2mm")
        dset.save(op.join(output_dir, prefix + ".pkl.gz"))
        if not op.isfile(op.join(output_dir, '{prefix}_logp_level-cluster_corr-FWE_method-montecarlo.nii.gz'.format(prefix=prefix))):

            ale = ALE()

            results = ale.fit(dset)
            corr = FWECorrector(
                method="montecarlo", n_iters=5000, voxel_thresh=0.001, n_cores=12)
            cres = corr.transform(results)

            cres.save_maps(output_dir=output_dir, prefix=prefix)

        z_img_logp = nib.load(op.join(output_dir, '{prefix}_logp_level-cluster_corr-FWE_method-montecarlo.nii.gz'.format(prefix=prefix)))
        z_img = nib.load(op.join(output_dir, '{prefix}_z.nii.gz'.format(prefix=prefix)))
        z_img_thresh = thresh_img(z_img_logp, z_img, 0.001)
        nib.save(z_img_thresh, op.join(output_dir, '{prefix}_z_corr-cFWE_thresh-001.nii.gz'.format(prefix=prefix)))

        get_peaks(op.join(output_dir, '{prefix}_z_corr-cFWE_thresh-001.nii.gz'.format(prefix=prefix)), output_dir)

        all_txts = []
        for tmp2_txts in [affiliation, other, self, soccomm]:
            for i in tmp2_txts:
                all_txts.append(i)

        other_txts = [i for i in all_txts if i not in tmp_txts]
        prefix2 = []
        for i in other_txts:
            prefix2.append('_'.join(op.basename(i).split('_')[:-1]))
        prefix2 = '+'.join(sorted(list(set(prefix2))))
        print(prefix2)
        output2_dir = op.join(project_dir, 'derivatives', 'ale', prefix2)
        os.makedirs(output2_dir, exist_ok=True)

        dset2 = convert_sleuth_to_dataset(other_txts, target="mni152_2mm")
        dset2.save(op.join(output2_dir, prefix2 + ".pkl.gz"))

        if not op.isfile(op.join(output2_dir, '{prefix}_logp_level-cluster_corr-FWE_method-montecarlo.nii.gz'.format(prefix=prefix2))):

            ale = ALE()

            results = ale.fit(dset2)
            corr = FWECorrector(
                method="montecarlo", n_iters=5000, voxel_thresh=0.001, n_cores=12)
            cres = corr.transform(results)

            cres.save_maps(output_dir=output2_dir, prefix=prefix2)

        z_img_logp = nib.load(op.join(output2_dir, '{prefix}_logp_level-cluster_corr-FWE_method-montecarlo.nii.gz'.format(prefix=prefix2)))
        z_img = nib.load(op.join(output2_dir, '{prefix}_z.nii.gz'.format(prefix=prefix2)))
        z_img_thresh = thresh_img(z_img_logp, z_img, 0.001)
        nib.save(z_img_thresh, op.join(output2_dir, '{prefix}_z_corr-cFWE_thresh-001.nii.gz'.format(prefix=prefix2)))

        get_peaks(op.join(output2_dir, '{prefix}_z_corr-cFWE_thresh-001.nii.gz'.format(prefix=prefix2)), output2_dir)

        dset_combined = convert_sleuth_to_dataset(all_txts, target="mni152_2mm")
        output3_dir = op.join(project_dir, 'derivatives', 'subtraction', '{prefix}_gt_{prefix2}'.format(prefix=prefix, prefix2=prefix2))
        os.makedirs(output3_dir, exist_ok=True)

        image1 = op.join(output_dir, '{prefix}_z_corr-cFWE_thresh-001.nii.gz'.format(prefix=prefix))
        image2 = op.join(output2_dir, '{prefix}_z_corr-cFWE_thresh-001.nii.gz'.format(prefix=prefix2))

        if not op.isfile(op.join(output3_dir, '{prefix}_gt_{prefix2}.nii.gz'.format(prefix=prefix, prefix2=prefix2))):

            k = ALEKernel()
            ma_maps = k.transform(dset_combined, return_type='image')

            n_iters = 5000
            diff_map = subtraction_analysis(dset_combined, dset.ids, dset2.ids, masking.apply_mask(nib.load(image1), dset_combined.masker.mask_img), masking.apply_mask(nib.load(image2), dset_combined.masker.mask_img), ma_maps, n_iters)

            diff_img = dset_combined.masker.inverse_transform(diff_map)
            diff_img.to_filename(op.join(output3_dir, '{prefix}_gt_{prefix2}.nii.gz'.format(prefix=prefix, prefix2=prefix2)))
