# autoSctrutineer
Script for automatic scrutineering in MVRC. 
https://mantiumchallenge.com/

For a quick introduction with examples and pictures see the pdf. 

## Important changes
This script requires a particular submission folder structure. stls are now to be placed inside the folder corresponding to the names given in the official rules. For example: all the parts belonging to the **front wing endplate** are to be placed in the **fw_ep** folder etc. You can place multiple stls in each folder.  

## Checking submissions
The main scrutineering function is *scrutineer* inside *autoScrut.py*. Running autoScrut.py will check files contained in **test_submission_1** and **test_submission_2**. The first test-submission is mostly legal, while the second violates many rules. These *test submissions* can be seen as examples of the new submission folder structure. Two sets of rules are defined. The first is the full set of the most current rules (version 0.9), this is the default setting. The second is a set of "test-rules"  to quickly verify that the script works correctly. You can change between the two sets by commenting/uncommenting around line 120 in autoscrut.py   

During scrutineering a report (report.txt) is written in the submission folder. If violations are found then images of these are saved to *submission*/renderedImages. For "obscure"-type rules 2 images are saved. The first image has a *_scrt*-suffix. This image shows exactly what the script sees. Any red pixels in this image is a sign of violations. The second image has a *_ill* suffix. Here some of the geometries are made transparent to help identify the location of the violation. 

After scrutineering parts are copied from the submission folder to a *input_files* folder following the familiar MFlow structure.

## Setup
The script is written for python 3.9 it makes use of the following non-standard libraries:  

* [numpy](https://numpy.org/)  
* [vtk](https://pypi.org/project/vtk/)  
* [skimage](https://pypi.org/project/scikit-image/)  

If you use Anaconda (recommended) then you only need to add vtk to the default anaconda python environment: in Anaconda go to *Environments, select one, open Terminal, pip install vtk*

## New to this version
* Implemented version 0.9 of the 2025 rules, in rules.py 
* Obscure rule can now take lists as geometry input, eliminating the need for *mask*-actors. Now only reference- and given actors are created. Thus expanding the capabilities of the script and somewhat simplifying writing the rules. 
* Obscure-rule is no longer susceptible to Z-fighting (Due to implementing input from Max Taylor, thanks!) now 6 versions of the reference geometry is loaded, and offset 1 mm positive and negative along x, y and z respectivley. This gives some of the *_ill* images a "fuzzy" boundary 
* Added Top/Bottom visibility rule-type. 
* Added "Bounding-Box-size" rule-type.
* Added script to create submission-folder
* Added a template submission-folder (just ran the script lol, you're welcome ;) ). 


