# Automatic Scrutineering script by Christian aka 'Koldskaal' on f1Technical
# For use in MVRC: https://mantiumchallenge.com/

import vtk
import numpy as np
import numpy.matlib
from vtk.util.numpy_support import vtk_to_numpy
import os
from matplotlib.image import imread
import time
#from tkinter import filedialog
import shutil
from PIL import Image

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
    if geostr[0:3] in ('RV-', 'RV_', 'RS-', 'RS_'):
        source = vtk.vtkSTLReader()
        source.SetFileName(referenceGeometryPath + geostr + '.stl')
        
    else:
        source = appendStls(geostr)
    
    mapper.SetInputConnection(source.GetOutputPort())
    actor.SetMapper(mapper)
    return source, actor

def colorActors(actor_1, actor_2, rule, renderMode):
    if not renderMode:
        actor_1.GetProperty().LightingOff() #"Flat" coloring is best for scrutineering
        actor_2.GetProperty().LightingOff() 

        actor_1.GetProperty().SetColor( 0.1, 0.1, 0.1 )
        actor_2.GetProperty().SetColor( 0.9, 0.1, 0.1 )

    elif renderMode:
        actor_1.GetProperty().LightingOn() # Shaded coloring 
        actor_2.GetProperty().LightingOn()
        actor_1.GetProperty().SetOpacity(0.5)

        actor_1.GetProperty().SetColor( 0.1, 0.1, 0.1 )
        actor_2.GetProperty().SetColor( 0.9, 0.1, 0.1 )

    return actor_1, actor_2
# ------------------------- 
# Defining camera angles
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

# ------------------------
# Parse repackaging instructions
def parseRepackagefile(file): 
    repackDict = {'a': 1} 

    with open(file) as repackfile:
        repackStr = repackfile.readlines()
    
    for line in repackStr:
        line = line.strip()
        line = line.split(' ')
        try: 
            repackDict.update({line[0]: line[2]})
        except:
            pass

    return repackDict 

def combinePNGsToGIF(img1, img2, name):

    image1 = Image.open(img1)
    image2 = Image.open(img2)

    frames = []

    frames.append(image1.convert("P",palette=Image.ADAPTIVE))
    frames.append(image2.convert("P",palette=Image.ADAPTIVE))

    frames[0].save(name + '.gif', format='GIF', append_images=frames[1:], save_all=True, optimize = False, duration=1000, loop=0)
   
# ------------------------- 
# Read and parse Rule file: 
with open('rules.txt') as ruleFile:
    rulesStr = ruleFile.readlines()

rules = []
for line in rulesStr:
    line = line.strip()
    b = line.split(' ')
    try:
        include = b[10]
    except:
        include = False
    rule={'name': b[0], 'views': b[2], '1st': b[3], 'rule type': b[5], '2nd' : b[6], 'focus': b[8], 'include': include}

    rules.append(rule) 

# ------------------------- 
# Create a folder for rendered images 
path = os.getcwd()
rendImgPath = path + '/renderedImages'
try: 
    os.mkdir(rendImgPath)
except:
    pass

# -------------------------
# Create a function for each ruletype 
def ruleObscure(rule, ruleNumber):
    source_1, actor_1 = ruleStr2vtk(rule['1st'])
    source_2, actor_2 = ruleStr2vtk(rule['2nd'])

    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.SetOffScreenRendering(1)
    renWin.AddRenderer(ren)
    renWin.SetSize(1920,1080)

    actor_1, actor_2 = colorActors(actor_1, actor_2, rule, False)
    
    ren.AddActor(actor_1)
    ren.AddActor(actor_2)

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
    
    camPos, camViewUp, camBool = views2cam(rule['views'])
    camera = vtk.vtkCamera()
    camera = setCameraProj(camera, camBool)
    ren.SetActiveCamera(camera)

    renderedNonCompliace = False

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

        # Creating vtk array from a vtk-image from the hidden renderwindow, then converting said vtk_array into a numpy array to check for red pixels. 
        w2if = vtk.vtkWindowToImageFilter() # w2if -> window to image filter
        w2if.SetInput(renWin)
        w2if.Update()

        vtk_img = w2if.GetOutput()

        width, height, _ = vtk_img.GetDimensions()
        vtk_array = vtk_img.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        # only extract the red channel, and don't bother reshaping? 
        img = vtk_to_numpy(vtk_array).reshape(height, width, components)
        
        ## Checking the numpy array for red pixels 
        if np.max(img[:,:,0])>200: # Clearly visible red pixel should be ~229
            #print(np.max(img[:,:,0]))
            reportStr = 'Submission violates ' + rule['name'] + '\n'
            # write the image to png, change the colors and write the same image in a human readable way
            if not renderedNonCompliace:
                # Write the image used for scrutineering. 
                writer = vtk.vtkPNGWriter()
                writer.SetInputConnection(w2if.GetOutputPort())

                w2if.Update()
                renderedImageScrt = 'renderedImages/Rule' + str(ruleNumber) + '_Image' + str(j) + '_scrt.png'

                writer.SetFileName(renderedImageScrt)
                writer.Update()
                writer.Write()

                # Write an illustration image.
                actor_2.GetProperty().LightingOn()
                actor_1.GetProperty().LightingOn()
                ren.SetBackground( 0.9, 0.9, 0.9 )
                actor_1.GetProperty().SetOpacity(0.5)
                renWin.Render()

                w2if2 = vtk.vtkWindowToImageFilter()
                w2if2.SetInput(renWin)
                w2if2.Update()
                
                renderedImageIll = 'renderedImages/Rule' + str(ruleNumber) + '_Image' + str(j) + '_ill.png'
                writer2 = vtk.vtkPNGWriter()
                writer2.SetInputConnection(w2if2.GetOutputPort())
                writer2.SetFileName(renderedImageIll)
                writer2.Update()
                writer2.Write()

                # undo illustration settings
                actor_2.GetProperty().LightingOff()
                actor_1.GetProperty().LightingOff()
                ren.SetBackground( 0.05, 0.05, 0.05 )
                actor_1.GetProperty().SetOpacity(1)

                combinePNGsToGIF(renderedImageScrt, renderedImageIll, 'renderedImages/Rule' + str(ruleNumber) + '_Image' + str(j))
                renderedNonCompliace = True # change this to render all non complying images. 
                del w2if, w2if2, writer, writer2
        else:
            reportStr = 'Submission complies with ' + rule['name'] + '\n'

    return reportStr

# ------------------------- 
# Main Scrutineering Loop 
reportStr = ""
for i in range(len(rules)):
    rule = rules[i]
    print('Testing rule number: ' + str(i))
    if rule['rule type'] == 'obscure':
        reportStr = reportStr + ruleObscure(rule,i)
    # add other rules like this: 
    #elif rule['ruleType'] == 'somthing else':
    #    reportStr = reportStr + someOtherRule(inputs)...
    # 

reportStr = reportStr + "NB! Geometry shouldn't touch the outer bounds of reference volumes \n"
reportFile = "reportFile.txt"

with open(reportFile, "w") as f:
        f.write(reportStr)

# -----------------------
# submission repackaging loop. 
repackDict = parseRepackagefile('submissionRepackaging.txt')

try:
    os.mkdir(path + '/input_files/')
    os.mkdir(path + '/input_files/geometry/')
except:
    pass

subfolders = [
    'vehicle_body',
    'high_res_surfaces',
    'porous_media',
    'monitoring_surfaces',
    'specialBC']
for i in subfolders:
    try: 
        os.mkdir(path + '/input_files/geometry/' + i)
    except:
        pass

mflowgeoPath = path + '/input_files/geometry'
# Create the inputfiles folder structure... 

submission_subfolders = os.listdir(path+'/submission')
for subfolder in submission_subfolders:
    destinationFolder = repackDict[subfolder] # finding the destination folder from the dict. 
    subfolderPath = os.path.join(path, 'submission', subfolder)
    files = [f for f in os.listdir(subfolderPath) if os.path.isfile(os.path.join(subfolderPath, f))]
    for file in files:
        shutil.copy(os.path.join(subfolderPath, file), os.path.join(mflowgeoPath, destinationFolder, file))

print('Total runtime: ', time.time()-startTime) 
