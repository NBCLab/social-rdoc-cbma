import os
import os.path as op
import numpy as np
import nibabel as nib
from glob import glob
from nilearn import masking
from nimare.io import convert_sleuth_to_dataset
from nimare.meta.kernel import ALEKernel
from nimare.transforms import p_to_z
from nimare.stats import null_to_p


def subtraction_analysis(dset, ids, ids2, image1, image2, ma_maps, n_iters):

    grp1_voxel = image1 > 0
    grp2_voxel = image2 > 0
    n_grp1 = len(ids)
    img1 = masking.unmask(image1, dset.masker.mask_img)

    all_ids = np.hstack((np.array(ids), np.array(ids2)))
    id_idx = np.arange(len(all_ids))
    # Get MA values for both samples.
    ma_arr = masking.apply_mask(ma_maps, dset.masker.mask_img)

    # Get ALE values for first group.
    grp1_ma_arr = ma_arr[:n_grp1, :]
    grp1_ale_values = np.ones(ma_arr.shape[1])
    for i_exp in range(grp1_ma_arr.shape[0]):
        grp1_ale_values *= (1. - grp1_ma_arr[i_exp, :])
    grp1_ale_values = 1 - grp1_ale_values

    # Get ALE values for first group.
    grp2_ma_arr = ma_arr[n_grp1:, :]
    grp2_ale_values = np.ones(ma_arr.shape[1])
    for i_exp in range(grp2_ma_arr.shape[0]):
        grp2_ale_values *= (1. - grp2_ma_arr[i_exp, :])
    grp2_ale_values = 1 - grp2_ale_values

    # A > B contrast
    grp1_p_arr = np.ones(np.sum(grp1_voxel))
    if np.sum(grp1_voxel) > 0:
        diff_ale_values = grp1_ale_values - grp2_ale_values
        diff_ale_values = diff_ale_values[grp1_voxel]

        red_ma_arr = ma_arr[:, grp1_voxel]
        iter_diff_values = np.zeros((n_iters, np.sum(grp1_voxel)))

        for i_iter in range(n_iters):
            np.random.shuffle(id_idx)
            iter_grp1_ale_values = np.ones(np.sum(grp1_voxel))
            for j_exp in id_idx[:n_grp1]:
                iter_grp1_ale_values *= (1. - red_ma_arr[j_exp, :])
            iter_grp1_ale_values = 1 - iter_grp1_ale_values

            iter_grp2_ale_values = np.ones(np.sum(grp1_voxel))
            for j_exp in id_idx[n_grp1:]:
                iter_grp2_ale_values *= (1. - red_ma_arr[j_exp, :])
            iter_grp2_ale_values = 1 - iter_grp2_ale_values

            iter_diff_values[i_iter, :] = iter_grp1_ale_values - iter_grp2_ale_values

        for voxel in range(np.sum(grp1_voxel)):
            # TODO: Check that upper is appropriate
            grp1_p_arr[voxel] = null_to_p(diff_ale_values[voxel],
                                          iter_diff_values[:, voxel],
                                          tail='upper')
        grp1_z_arr = p_to_z(grp1_p_arr, tail='one')
        # Unmask
        grp1_z_map = np.zeros(grp1_voxel.shape[0])
        grp1_z_map[:] = np.nan
        grp1_z_map[grp1_voxel] = grp1_z_arr

    # B > A contrast
    grp2_p_arr = np.ones(np.sum(grp2_voxel))
    if np.sum(grp2_voxel) > 0:
        # Get MA values for second sample only for voxels significant in
        # second sample's meta-analysis.
        diff_ale_values = grp2_ale_values - grp1_ale_values
        diff_ale_values = diff_ale_values[grp2_voxel]

        red_ma_arr = ma_arr[:, grp2_voxel]
        iter_diff_values = np.zeros((n_iters, np.sum(grp2_voxel)))

        for i_iter in range(n_iters):
            np.random.shuffle(id_idx)
            iter_grp1_ale_values = np.ones(np.sum(grp2_voxel))
            for j_exp in id_idx[:n_grp1]:
                iter_grp1_ale_values *= (1. - red_ma_arr[j_exp, :])
            iter_grp1_ale_values = 1 - iter_grp1_ale_values

            iter_grp2_ale_values = np.ones(np.sum(grp2_voxel))
            for j_exp in id_idx[n_grp1:]:
                iter_grp2_ale_values *= (1. - red_ma_arr[j_exp, :])
            iter_grp2_ale_values = 1 - iter_grp2_ale_values

            iter_diff_values[i_iter, :] = iter_grp2_ale_values - iter_grp1_ale_values

        for voxel in range(np.sum(grp2_voxel)):
            # TODO: Check that upper is appropriate
            grp2_p_arr[voxel] = null_to_p(diff_ale_values[voxel],
                                          iter_diff_values[:, voxel],
                                          tail='upper')
        grp2_z_arr = p_to_z(grp2_p_arr, tail='one')
        # Unmask
        grp2_z_map = np.zeros(grp2_voxel.shape[0])
        grp2_z_map[:] = np.nan
        grp2_z_map[grp2_voxel] = grp2_z_arr

    # Fill in output map
    diff_z_map = np.zeros(grp1_voxel.shape[0])
    diff_z_map[grp2_voxel] = -1 * grp2_z_map[grp2_voxel]
    # could overwrite some values. not a problem.
    diff_z_map[grp1_voxel] = grp1_z_map[grp1_voxel]

    return diff_z_map
