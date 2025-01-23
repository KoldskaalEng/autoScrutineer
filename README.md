# autoSctrutineer
Script for automatic scrutineering in MVRC. 
https://mantiumchallenge.com/

For a quick introduction with examples and pictures see the pdf. 

## Important changes
This script requires a particular submission folder structure. stls are now to be placed inside the folder corresponding to the names given in the official rules. For example: all the parts belonging to the **front wing endplate** are to be placed in the **fw_ep** folder etc. You can place multiple stls in each folder.  

Additionally, faces that are **coincident** or **co-planar** with the surfaces of the reference volumes might be considered illegal, due to **z-fighting**. For this reason, it is adviced that competitors stay a few milimeters clear of the reference volume boundaries. 

## Checking submissions
The main scrutineering function is *scrutineer* inside *autoScrut.py*. Running autoScrut.py will check files contained in **test_submission_1** and **test_submission_2**. The first test-submission is completely legal, while the second violates many rules. These *test submissions* can be seen as examples of the new submission folder structure. The rules defined here are a small subsection of the proposed 2025 rules to show the capabilities of the script. The rules will be updated when the 2025 rules are fully defined and approved. 

During scrutineering a report (report.txt) is written in the submission folder. If violations are found then images of these are saved to *submission*/renderedImages. For "obscure"-type rules 2 images are saved. The first image has a *_scrt*-suffix. This image shows exactly what the script sees. Any red pixels in this image is a sign of violations. The second image has a *_ill* suffix. Here some of the geometries are made transparent to better show the location of the violation. 

After scrutineering parts are copied from the submission folder to a *input_files* folder following the familiar MFlow structure.

## Setup
The script is written for python 3.9 it makes use of the following non-standard libraries:
* numpy 
* vtk 
* skimage

If you use Anaconda (recommended) then you only need to add vtk to the default anaconda python environment. 

