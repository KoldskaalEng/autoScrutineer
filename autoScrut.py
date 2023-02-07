# Automatic Scrutineering script by Christian aka 'Koldskaal' on f1Technical
# For use in MVRC 

import vtk
import numpy as np
import numpy.matlib
import os
from matplotlib.image import imread
import time
from tkinter import filedialog

startTime = time.time()
referenceGeometryPath = 'referenceGeometry/'
submittedGeometryPath = 'submission/'
testMode = False # At this point I dont even know what testmode does 
# make som tkinter bullshit to make it easier to select the submission folder. 

# ------------------------- 
# some functions 
def getBoundingBoxCoords(geometry):
    outline = vtk.vtkOutlineFilter()
    outline.SetInputConnection(geometry.GetOutputPort())

    outlineMapper = vtk.vtkPolyDataMapper()
    outlineMapper.SetInputConnection(outline.GetOutputPort())

    outlineActor = vtk.vtkActor()
    outlineActor.SetMapper(outlineMapper)

    coords = outlineActor.GetBounds() 
    center = [(coords[0]+coords[1])/2, (coords[2]+coords[3])/2, (coords[4]+coords[5])/2]
    radius = (((coords[1]-center[0])**2) + ((coords[3]-center[1])**2) + ((coords[5]-center[2])**2))**(1/2)

    return coords, center, radius

def views2cam(views):
    return {
        'allAngles' : cameraAllAngles(),
        'below' : cameraBelow(),
        'above': cameraAbove(),
        'sides': cameraSides()}[views]

def appendStls(folder):
    geometries2combine = [f for f in os.listdir(submittedGeometryPath + folder) if os.path.isfile(os.path.join(submittedGeometryPath + folder, f))]

    appendFilter = vtk.vtkAppendPolyData()

    for file in geometries2combine:
        reader = vtk.vtkSTLReader()
        reader.SetFileName(submittedGeometryPath + folder + '/' + file)
        reader.Update()

        appendInput = vtk.vtkPolyData()
        appendInput.ShallowCopy(reader.GetOutput())

        appendFilter.AddInputData(appendInput)
        appendFilter.Update()
    
    return appendFilter

def ruleStr2vtk(geostr):
    mapper = vtk.vtkPolyDataMapper()
    actor = vtk.vtkActor()
    if geostr[0:3] == 'RV-' or geostr[0:3] == 'RS-':
        source = vtk.vtkSTLReader()
        source.SetFileName(referenceGeometryPath + geostr + '.stl')
        
    else:
        source = appendStls(geostr)
    
    mapper.SetInputConnection(source.GetOutputPort())
    actor.SetMapper(mapper)
    return source, actor

def colorActors(actor_1, actor_2, rule, testMode):
    # add a color palette for displaying scrutineering results
    if not testMode:
        actor_1.GetProperty().LightingOff() #Flat coloring is best for this purpose
        actor_2.GetProperty().LightingOff() 

        actor_1.GetProperty().SetColor( 0.1, 0.1, 0.1 )
        actor_2.GetProperty().SetColor( 0.9, 0.1, 0.1 )

    else:
        actor_1.GetProperty().SetOpacity(0.5)

        actor_1.GetProperty().SetColor( 0.1, 0.1, 0.1 )
        actor_2.GetProperty().SetColor( 0.9, 0.1, 0.1 )

    return actor_1, actor_2
# ------------------------- 
# Defining camera angles
# "AllAngles" are rendered in "perspective", and other camera angles are rendered with parallel projection. 
# Probably put all the camera functions in a seperate file.
def cameraBelow():
    camPos = np.array([
        [0, 0, -1]
    ])
    camViewUp = np.array([
        [0, 1, 0]
    ])
    camBool = True
    return camPos, camViewUp, camBool

def cameraSides():
    camPos = np.array([
        [0, 1, 0],
        [0, -1, 0]
    ])
    camViewUp = np.array([
        [0, 0, 1],
        [0, 0, 1]
    ])
    camBool = True
    return camPos, camViewUp, camBool

def cameraAbove():
    camPos = np.array([
        [0, 0, 1]
    ])
    camViewUp = np.array([
        [0, 1, 0]
    ])
    camBool = True
    return camPos, camViewUp, camBool

def cameraAllAngles():
    camPos = np.array([ 
        [-1, 0, -1], # Camera position: in front, on centerline, from below
        [-1, 1, -1], # in front, from right, from below
        [0, 1, -1], # from middle of car, right, below
        [1, 1, -1], # behind, from right, below. 
        [1, 0, -1], # behind, centerline, below...
        [1, -1, -1],
        [0, -1, -1],
        [-1, -1, -1],
        [-1, 0, 0], # <- front from 0 height 
        [-1, 1, 0], 
        [0, 1, 0], # <- side1
        [1, 1, 0],  
        [1, 0, 0], # <- back
        [1, -1, 0],
        [0, -1, 0], # <- side2
        [-1, -1, 0],
        [-1, 0, 1], # from above
        [-1, 1, 1], 
        [0, 1, 1], 
        [1, 1, 1],  
        [1, 0, 1], 
        [1, -1, 1],
        [0, -1, 1],
        [-1, -1, 1],
        [0, 0, -1], #From directly below
        [0, 0, 1] #From directly above
    ])
    camViewUp = numpy.matlib.repmat(np.array([0, 0, 1]),24, 1) # Allmost all views have the same camera "up-vector" (z). 
    camViewUp = np.append(camViewUp, [[0, 1, 0],[0, 1, 0]], axis=0) # Directly above, and below have y as "up-vector". 
    camBool = False

    return camPos, camViewUp, camBool 

def setCameraProj(camera, bool_):
    if bool_:
        camera.ParallelProjectionOn()
    else:
        camera.ParallelProjectionOff()
    return camera

# ------------------------- 
# Read and parse Rule file: 
with open('rules.txt') as ruleFile:
    rulesStr = ruleFile.readlines()

rules = []
for line in rulesStr:
    line = line.strip()
    b = line.split(' ')
    try:
        include = b[9]
    except:
        include = False
    rule={'views': b[1], '1st': b[2], 'rule type': b[4], '2nd' : b[5], 'focus': b[7], 'include': include}
    if rule['rule type'] == 'obscureMax_8%_of':
        rule['number of setups'] = 2
    else:
        rule['number of setups'] = 1
    rules.append(rule) 

# Parse rules from a xml file instead? 

# ------------------------- 
# Create a folder for rendered images 
path = os.getcwd()
rendImgPath = path + '/renderedImages'
try: 
    os.mkdir(rendImgPath)
except:
    pass

# ------------------------- 
# Create+write image loop:
for i in range(len(rules)):
    rule = rules[i]

    for k in range(rule['number of setups']):
        
        source_1, actor_1 = ruleStr2vtk(rule['1st'])
        source_2, actor_2 = ruleStr2vtk(rule['2nd'])

        ren = vtk.vtkRenderer()
        renWin = vtk.vtkRenderWindow()
        renWin.SetOffScreenRendering(1)
        renWin.AddRenderer(ren)
        renWin.SetSize(1920,1080)

        actor_1, actor_2 = colorActors(actor_1, actor_2, rule, testMode)
        
        altTxt = ''
        if k == 1:
            actor_1.GetProperty().SetOpacity(0)
            altTxt = '_alt'

        ren.AddActor(actor_1)
        ren.AddActor(actor_2)

        if testMode:
            ren.SetBackground( 0.9, 0.9, 0.9 )
        else:
            ren.SetBackground( 0.05, 0.05, 0.05 )

        if rule['include']:
            s3, actor_3 = ruleStr2vtk(rule['include'])
            actor_3.GetProperty().SetColor( 0.1, 0.1, 0.1 )
            actor_3.GetProperty().LightingOff()
            ren.AddActor(actor_3)

        if rule['focus'] == '1st':
            bbCords, center, radius = getBoundingBoxCoords(source_1)
        else:
            bbCords, center, radius = getBoundingBoxCoords(source_2)
        
        #print(i, bbCords, center, radius)
        
        camPos, camViewUp, camBool = views2cam(rule['views'])
        camera = vtk.vtkCamera()
        camera = setCameraProj(camera, camBool)
        ren.SetActiveCamera(camera)

        for j in range(len(camPos)):
            ren.ResetCamera()

            camera.SetFocalPoint(center)
            camera.SetViewUp(camViewUp[j,:])

            p = camPos[j,:]
            mag = ((p[0]**2) + (p[1]**2) + (p[2]**2))**(0.5)
            p1 = center + 4*radius*p/mag
            camera.SetClippingRange(0.1*radius,100*radius)

            camera.SetPosition(p1)

            renWin.Render()

            w2if = vtk.vtkWindowToImageFilter()
            w2if.SetInput(renWin)

            writer = vtk.vtkPNGWriter()
            writer.SetInputConnection(w2if.GetOutputPort())

            w2if.Update()
            renderedImageName = 'renderedImages/Rule' + str(i) + '_Image' + str(j) + altTxt + '.png'

            writer.SetFileName(renderedImageName)
            writer.Update()
            writer.Write()

            del w2if, writer

# ------------------------- 
# Read all rendered images and determine legality 

images = [f for f in os.listdir(rendImgPath) if os.path.isfile(os.path.join(rendImgPath, f))]

legalSubmission = True
reportFile = "reportFile.txt"

with open(reportFile, "w") as f:
    for i in range(len(rules)):
        if testMode:
            break

        rule = rules[i]

        selectedImages = []
        for image in images:
            if 'Rule' + str(i) + '_' in image:
                selectedImages.append(image)
        
        ruleViolation = False

        if rule['rule type'] == 'obscure':
            for sImage in selectedImages:
                img = imread(rendImgPath + '/' + sImage)

                if np.max(img[:,:,0])>0.8:
                    #print('Submission violates rule no: ' + str(i))
                    f.write('Submission violates rule no: ' + str(i) + '\n')
                    break
        
        elif rule['rule type'] == 'obscureMax_8%_of':
            imgw = imread(rendImgPath + '/Rule' + str(i) + '_Image0.png')
            w = (imgw[:,:,0]>0.8).sum()
            #print('Number of visible pixels: ', wo)
            f.write('Number of visible pixels: ', wo, '\n')

            imgwo = imread(rendImgPath + '/Rule' + str(i) + '_Image0_alt.png')
            wo = (imgwo[:,:,0]>0.8).sum()
            #print('Total number of red pixels: ', w)
            f.write('Total number of red pixels: ', w, '\n')

            covered = (wo-w)/wo
            #print('Obscured percentage of pixels: ', covered*100, '%')
            f.write('Obscured percentage of pixels: ', covered*100, '%\n')

            if covered > 0.08:
                #print('Submission violates rule no: ' + str(i))
                f.write('Submission violates rule no: ' + str(i)+ '\n')

time2run= time.time()-startTime
print('Total runtime: ', time2run) 
# Lav det om så den skriver en txtfil som rapport i stedet for at skrive til terminalen 
# Compile scriptet til en exe som nemmere kan køres. 
# flyt rundt på filerne, så mappen overholder MVRC standart mappen. 
# Lav det så den sletter alle de filer som ikke er vigtige. 
# Is it possible to have vtk render an image to a bitmap and not to a png file, so I dont have to create files and then delete them afterwards. 
