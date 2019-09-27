# Customizing cortical parcellation colors to be seen with the Connectome Workbench
# This code works with nibabel 2.4.0

'''
# Customizing cortical parcellation colors to be seen with the Connectome Workbench.

This script uses a label file from a cortical parcellation and changes its colors.
This example customizes the Multi-modal Parcellation of Human Cerebral Cortex by M. Glasser
by modifying a *.dlabel.nii file containing both label names and colors for every grayordinate

More info regarding this file format can be found at: 
<https://wiki.humanconnectome.org/display/PublicData/HCP+Users+FAQ>

Reference: 
- Matthew F. Glasser, et al (2016) - A multi-modal parcellation of human cerebral cortex
    Paper : <https://www.nature.com/articles/nature18933>
    Source files: <https://balsa.wustl.edu/study/show/RVVG>
- Original discussion in the nibabel github repository:
    <https://github.com/nipy/nibabel/issues/758>

'''
 
import numpy as np
import nibabel.cifti2 as ci

# Select the folder containing your *.dlabel.nii file
import os
os.chdir(MAIN_FOLDER)
label_filename = 'Q1-Q6_RelatedParcellation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii'

# Define the rgba for the new labels. This toy example sets every grayordinate to gray 
new_labels = {0: ('0', (1., 1., 1., 0.))}
for i in np.arange(0, 360):
    new_labels[i+1] = (str(i + 1), (0.5, 0.5, 0.5, 1.))

img = ci.Cifti2Image.from_filename(label_filename)

# extracting the Axis describing the labels (i.e., along the first dimension)
label_axis = img.header.get_axis(0)

# updating the labels for the first (in this case only) column
label_axis.label[0] = new_labels

# Create a new header with new labels across the first axis and the original brain model with the vertices across the other axis.
new_header = ci.Cifti2Header.from_axes((label_axis, img.header.get_axis(1)))

# Create a new *.dlabel.nii file containing the new colors included in the new_header
new_img = ci.Cifti2Image(img.get_fdata(), header=new_header)
new_img.to_filename('new_labels.dlabel.nii')