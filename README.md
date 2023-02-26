# autoSctrutineer

## Description 
Script for automatic scrutineering in MVRC.

## Tutorial 
This automated scrutineering requires a new submission folder structure. stls are now to be places inside the folder corresponing to the names given in the official rules. For example: all the parts belonging to the frontwing are to be placed in the frontwing folder. It is ok to place multiple stls in each folder.  

Be aware that faces that are coincident with the surfaces of the referencevolumes might be considered illegal, due to "z-flickering". It is adviced that you stay a few mm clear of the reference volume boundaries. 

### Checking one submission


### Checking multiple submissions
_we are checking..._ 

### Submission folder buildup 

## Todo: 
* make the new default submission folder template availible for download. 
* define paths in the beginning of the file and streamline naming 
* implement a neat way to check multiple submissions. 
* Rework the rendering loop to render directly to numpy array. 
* Check legality directly in the rendering loop
* Implement rendering prettier scrutineering images for report. 