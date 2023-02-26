# Rule format explained
General information:
* Every line in the rules.txt is treated as a seperate rule. 

Every rule follows this format: 

From _[camera angles]_ _[actor1]_ must _[ruletype]_ _[actor2]_ focus _[actor#]_ include _[actor3]_

all inputs except for _[actor3]_ are required. 

The term "actor" can refer to the geometry contained within a single or multiple stl-files. 

Example of a single rule: 

_From allAngles RV-BODY must obscure body focus 2nd include MandParts_ 

The point of this rule is to ensure that any parts labelled "body" are fully contained within the reference volume "RV-BODY". The way this is checked is by coloring all the "body" parts red, and coloring RV-body black. Then "pictures" are taken from _all Angles_ to see if any red bits stick out. The ruletype: "obscure" tells the rulechecker that no red pixels are allowed in the pictures. "focus 2nd" indicates that the camera should be centered on the second actor, "body", not the reference volume. Include Mandparts means that mandatory parts are included in the images, but are colored black. Effectively this means it is legal to make geometries that stick out of their designated reference volumes, if the bits that stick out are covered by mandatory parts. This ensures that overlapping geometry, made to avoid small gaps that might confuse SnappyHexMesh, continues to be legal. 

The following sections will go more indepth into how one might create new rules, or new rule options/settings. 

## Camera angles
The current supported sets of camera angles are: 
* allAngles
* below
* above
* sides

The different views to be rendered are defined by a list vectors. Every vector in the list represents a new camera angle, so the length of the list indicate the number of images to be rendered. 

Allangles are rendered in "perspective" while the rest are rendered in "isometric". 

Each set of camera angles are defined in a seperate function. The specific function of interest is then called based on what the rule calls for. This is done in the function views2cam. So if one wanted to add a new set of camera angles, one would first define a function containing the numpy arrays of camera positions and up-vectors. 

## Actors 
### Actor names 
The programme will fetch the files of each actor from the appropriate folder. It assumes that anything starting with RV- or RS- can be found in the referenceGeometry folder. Everything else should refer to a subdirectory in the submission folder.  

### Focus 
One must specify which actor to center the camera on. Usually 2nd for actor 2, colored red. However sometimes it can be advantagous to focus on actor 1, to crop some parts of the car out of the picture.  
### actor coloring, reference actors, mandatory parts... 
### Actor 3 as mask 
The third actor is rendered in a neutral color. Therfor it can be used as a mask, to specify regions of interest. 

## Ruletypes 
The current supported ruletypes are obscure, and obscuremax8%. although the latter is poorly implemented. The behavior of the different ruletypes is implemented directly in the scrutineering report writing/rulechecking loop. 

### obscure

Currently the actors are always colored the same way, no matter the ruletype. 

When the ruletype is "obscure", then any red pixels in the rendered images are interpreted as a violation. 

### ObscureMax_8% 

This rule is cruedly implemented. It renders 2 images for each camera angle, one with actor 1 and one without. it then compares the number of red pixels in the two images. If actor 1 obscures more than 8% of the red pixels, then 

## Repackaging 
