import os
import numpy as np
import nibabel as nib
import nilearn as nil


def rescale_affine(input_affine, voxel_dims=[1, 1, 1], target_center_coords=None):
    """
    This function uses a generic approach to rescaling an affine to arbitrary
    voxel dimensions. It allows for affines with off-diagonal elements by
    decomposing the affine matrix into u,s,v (or rather the numpy equivalents)
    and applying the scaling to the scaling matrix (s).

    Parameters
    ----------
    input_affine : np.array of shape 4,4
        Result of nibabel.nifti1.Nifti1Image.affine
    voxel_dims : list
        Length in mm for x,y, and z dimensions of each voxel.
    target_center_coords: list of float
        3 numbers to specify the translation part of the affine if not using the same as the input_affine.

    Returns
    -------
    target_affine : 4x4matrix
        The resampled image.
    """
    # Initialize target_affine
    target_affine = input_affine.copy()
    # Decompose the image affine to allow scaling
    u, s, v = np.linalg.svd(target_affine[:3, :3], full_matrices=False)

    # Rescale the image to the appropriate voxel dimensions
    s = voxel_dims

    # Reconstruct the affine
    target_affine[:3, :3] = u @ np.diag(s) @ v

    # Set the translation component of the affine computed from the input
    # image affine if coordinates are specified by the user.
    if target_center_coords is not None:
        target_affine[:3, 3] = target_center_coords
    return target_affine

def calculate(target_shape, voxel_dims, load, save):
    img = nib.load(load)
    target_affine = img.affine.copy()
    # Calculate the translation part of the affine
    spatial_dimensions = (img.header['dim'] * img.header['pixdim'])[1:4]
    # Calculate the translation affine as a proportion of the real world
    # spatial dimensions
    image_center_as_prop = img.affine[0:3, 3] / spatial_dimensions
    # Calculate the equivalent center coordinates in the target image
    dimensions_of_target_image = (np.array(voxel_dims) * np.array(target_shape))
    target_center_coords =  dimensions_of_target_image * image_center_as_prop

    target_affine = rescale_affine(target_affine,voxel_dims,target_center_coords)

    resampled_img = nil.image.resample_img(img, target_affine=target_affine, target_shape=target_shape)
    resampled_img.header.set_zooms((np.absolute(voxel_dims)))
    nib.save(resampled_img, save)


calculate((480, 480, 190),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat0_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat0_label_A.nii.gz')
calculate((480, 480, 110),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat1_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat1_label_A.nii.gz')
calculate((384, 384, 210),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat2_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat2_label_A.nii.gz')
calculate((560, 560, 190),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat3_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat3_label_A.nii.gz')
calculate((384, 384, 180),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat4_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat4_label_A.nii.gz')
calculate((640, 640, 215),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat5_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat5_label_A.nii.gz')
calculate((384, 384, 200),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat6_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat6_label_A.nii.gz')
calculate((432, 432, 225),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat7_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat7_label_A.nii.gz')
calculate((480, 480, 200),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat8_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat8_label_A.nii.gz')
calculate((480, 480, 225),[1, 1, 1],'C:/Users/Silviu/Desktop/Old/training_axial_full_pat9_label_A.nii.gz'
          ,'C:/Users/Silviu/Desktop/New/training_axial_full_pat9_label_A.nii.gz')

