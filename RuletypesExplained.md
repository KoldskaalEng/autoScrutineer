# Rule format explained
Every line in the rules.txt is treated as a seperate rule. Currently all rules must follow this format: 

_[Rule name]_ From _[camera angles]_ _[actor1]_ must _[ruletype]_ _[actor2]_ focus _[actor#]_ include _[actor3]_

All inputs except for _[actor3]_ are required. 

The term "actor" can refer to the geometry contained within one or more stl-files. 

Example of a single rule: 

§9 From allAngles RV_Vehiclebody_MVRC_v02 must obscure body focus 2nd include MandParts

The point of this rule is to ensure that any parts labelled "body" are fully contained within the reference volume "RV-BODY". The way this is checked is by coloring all the "body" parts red, and coloring RV-Vehiclebody black. Then "pictures" are taken from _all Angles_ to see if any red bits stick out. The ruletype: "obscure" tells the rulechecker that no red pixels are allowed in the pictures. "focus 2nd" indicates that the camera should be centered on the second actor, the "body", not the reference volume. Include Mandparts means that mandatory parts are included in the images, but are colored black. Effectively this means it is legal to make geometries that protrude from their designated reference volumes, if the bits that stick out are covered by mandatory parts. This ensures a bit of leway. And allows for the kind of overlapping that SnappyHexMesh prefers. 

This rule-format is meant to be easily parse-able by the programme, easy to read by humans and easy to edit. Whether or not this was accomplised might be debated. 

The following sections will go more indepth into how one might create new rules, or new rule options/settings. 

## Main rule checking loop
Rules are read from the rule.txt file, and then checked one by one. In this loop different functions can be called depending on the ruletype of the rule being checked. 

## Ruletypes 
The current the only supported ruletype is _obscure_. This ruletype is defined in the function _ruleObscure_. 

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
### Using actor 3
The third actor is rendered in a neutral color. The 3rd actor can be used as a mask, to specify regions of interest. Focussing the camera on actor 3 is not supported. 

## Repackaging 
Submission files are repackaged according to the instructions in the file submissionRepackaging.txt. AutoScrutineer creates a folder ready for MFlow. 