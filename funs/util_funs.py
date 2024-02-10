import vtk
import os
from vtk.util.numpy_support import vtk_to_numpy
from camera_funs import *
from settings import * 
# from PIL import Image

# Get the bounding box coordinates of a vtk geometry, used to focus camera
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

# Combines several stl-files into a single vtk-object
def appendStls(name):
    if name == 'MandParts':
        folder = runSettings['mandatory geometry path']
    else:
        folder = runSettings['submission geometry path'] + name

    geometries2combine = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

    appendFilter = vtk.vtkAppendPolyData()

    for file in geometries2combine:
        reader = vtk.vtkSTLReader()
        reader.SetFileName(folder + '\\' + file)
        reader.Update()

        appendInput = vtk.vtkPolyData()
        appendInput.ShallowCopy(reader.GetOutput())

        appendFilter.AddInputData(appendInput)
        appendFilter.Update()
    
    return appendFilter

# Takes the name of a geometry from the rules, and loads the geometry as vtk object. 
def ruleStr2vtk(geo_name):
    referenceGeometryPath = runSettings['reference geometry path']
    mapper = vtk.vtkPolyDataMapper()
    actor = vtk.vtkActor()
    if geo_name[0:3] in ('RV-', 'RV_', 'RS-', 'RS_'): # If the name starts with one of these, then look for the geometry in the reference geometry folder 
        # list files in reference folder 
        ref_files = [f for f in os.listdir(referenceGeometryPath) if os.path.isfile(os.path.join(referenceGeometryPath, f))]
        
        # pick the one that most closely matches the given geo_name. 
        file_no = next((i for i, j in enumerate(ref_files) if geo_name.lower() in j.lower()), None)

        source = vtk.vtkSTLReader()
        
        source.SetFileName(referenceGeometryPath + ref_files[file_no])
        
    else: # Otherwise look for the name in the submitted geometry
        source = appendStls(geo_name)
    
    mapper.SetInputConnection(source.GetOutputPort())
    actor.SetMapper(mapper)
    return source, actor

def colorActors(actor_1, actor_2, ren): # Color Actors for scrutineering.
    # Actor1 = reference geometry, Actor2 = given geometry
    actor_1.GetProperty().LightingOff() #"Flat" coloring is best for scrutineering
    actor_2.GetProperty().LightingOff() 
    actor_1.GetProperty().SetOpacity(1)

    actor_1.GetProperty().SetColor( 0.1, 0.1, 0.1 )
    actor_2.GetProperty().SetColor( 0.9, 0.1, 0.1 )

    ren.SetBackground( 0.05, 0.05, 0.05 ) # Background color for scrutineering 

    return actor_1, actor_2, ren

def illustrationColors(actor_1, actor_2, ren, settings): # Coloring for report images. 
    # Actor1 = reference geometry, Actor2 = given geometry
    rGeoC = settings['saved image settings']['Reference geometry color']
    geoC = settings['saved image settings']['Geometry color']
    opacity = settings['saved image settings']['Reference geometry opacity']
    bgC = settings['saved image settings']['Background color']

    actor_1.GetProperty().LightingOn() # Shaded coloring 
    actor_2.GetProperty().LightingOn()
    actor_1.GetProperty().SetOpacity(opacity)

    actor_1.GetProperty().SetColor( rGeoC[0], rGeoC[1], rGeoC[2] )
    actor_2.GetProperty().SetColor( geoC[0], geoC[1], geoC[2] )

    ren.SetBackground( bgC[0], bgC[1], bgC[2] )

    return 


# def combinePNGsToGIF(img1, img2, name):

#     image1 = Image.open(img1)
#     image2 = Image.open(img2)

#     frames = []

#     frames.append(image1.convert("P",palette=Image.ADAPTIVE))
#     frames.append(image2.convert("P",palette=Image.ADAPTIVE))

#     frames[0].save(name + '.gif', format='GIF', append_images=frames[1:], save_all=True, optimize = False, duration=1000, loop=0)

def views2cam(views):
    return {
        'all' : cameraAllAngles(),
        'below' : cameraBelow(),
        'above': cameraAbove(),
        'sides': cameraSides(),
        'front': cameraFront()}[views]