# autoSctrutineer
Script for automatic scrutineering in MVRC. This version of the script contains an older version of the reference geometry. This will be updated to reflect 2024 rules once the rules are finalized and published to the website. 

## Important changes
This automated scrutineering script requires a particular submission folder structure. stls are now to be places inside the folder corresponding to the names given in the official rules. For example: all the parts belonging to the **front wing** are to be placed in the **front_wing** folder. 
You can place multiple stls in each folder.  

NB! Faces that are **coincident** or **co-planar** with the surfaces of the reference volumes might be considered illegal, due to **z-fighting**. For this reason, it is adviced that you stay a few mm clear of the reference volume boundaries. 

## Checking submissions
The main scrutineering function is *scrutineer* inside *autoScrut.py*. Running autoScrut.py as a script will check files contained in **team1_submission**. This folder can be used as a template for race submissions. 

An example of checking multiple submissino is also provided in autoScrut.py, but has been commented out. 

After scrutineering, a report (report.txt) is written in the submission folder. If violations are found then images of these are saved to submission/renderedImages. For "obscure"-type rules (see section [Can and Can't](#Capabilities) ), 2 images are saved. The first image has a *_scrt*-suffix. This image shows exactly what the script sees. Any red pixels in this image is a sign of violations. The second image has a *_ill* suffix. Here some of the geometries are made transparent to better show the location of the violation. 

Finally parts are copied from the submission folder to a *input_files* folder that can be read by MFlow.

## Setup
Settings 
submitted geometry, if you change folder names or choose to store geometries elsewhere  
Mand parts
Reference geometry 

### Dependencies
The script is written for python 3.9 
it makes use of the following libraries:
* Numpy (https://numpy.org/)
* vtk (https://docs.vtk.org/en/latest/getting_started/index.html)

Both of these can easily be installed with *pip install xxx*. 

## <a name="Capabilities"></a> Can and Can't
Currently the script can test if parts are within their designated reference volume and if parts cover the reference surfaces they are supposed to cover. These rules essentially test for the same thing: Does geometry X completely obscure/conceal geometry Y? For this reason this is referred to as an obscure-type rule, and is tested using *obscure_rule.py*.

*Masks* can be added to obscure-type rules to only check certain areas. Camera angles can be specified if some parts only need to be obscured from certain angles.  

The script cannot test: the 10 mm rule, overall symmetry, only z-extrusion for the fences or Rear wing chord lenghts  

## 2Do
These functionalities are in the process of being implemented

### Count number of cut sections 
cut_test1.py and cut_test2.py contain some experiments in creating cut sections with VTK. It seems that creating only the outline, as in cut_test2.py, is the most robust. The outline can then be further analysed with numpy. 

The outline can be used to determine number of cut sections by the following process:
1. Convert VKT-image to numpy array
2. Convert numpy array to boolean array, based on some red color threshold = 1, other = 0
3. Search array for first 1.
4. "Bucket-fill" all the pixels with value 1 that touch the first 1, add +1 to a counter, and make all these pixels = 0 
5. return to step 3 until entire image has been searched. 

### Find regions that are not visible from directly above/below
It might be possible to render the given geometry as transparent. Here overlapping regions will have a slightly different color compared to regions with no overlap. Multiple parts might be a problem though. 

### Section arrangement for front wing sections 
If the section outlines, found during section counting, are stored in memory then section arrangement can be determined like so:
1. Sort sections based on lowest x-value 
2. Skipping the first section: 
    *  Check that the previous section contains at least one point with the same x-value as the leading edge, and that this point is below the leading edge. 
3. Something similar can be done for the trailing edge. 

### Area of each cut section
It should be possible to get bounding box coordinates from the cut-section using vtk. Once sections are counted, one can determine the bounding box in the rendered image. With these it is possible to determine the size of each pixel in the rendered image. 

Bucket fill the sections in the image, and count the number of pixels to find area of each section in the image. 

