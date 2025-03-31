import vtk
import os
from vtk.util.numpy_support import vtk_to_numpy
from camera_funs import *
from settings import * 
from copy import deepcopy
import re 
# from PIL import Image

# Get the bounding box coordinates of a vtk geometry, used to focus camera
def getBoundingBoxCoords_actor(actor):
    bounds = actor.GetMapper().GetInput().GetBounds()
    center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2]
    radius = (((bounds[1]-center[0])**2) + ((bounds[3]-center[1])**2) + ((bounds[5]-center[2])**2))**(1/2)
    return bounds, center, radius

def isOfficialGeo(name: str):
    for x in runSettings['official geometry prefix']:
        if x == name[:len(x)]:
            return True
    return False

def splitAtNumber(s):
    match = re.search(r'\d', s)
    if match:
        index = match.start()
        return s[:index]
    return s

def get_list_of_paths( geometries: list ):
    if isinstance(geometries, str): # If you pass it a single geometry as a str, it'll still work. 
        geometries = [geometries]
    list_of_paths = []

    off_geo_path = runSettings['official geometry path']

    for geometry in geometries: 

        if isOfficialGeo(geometry):
            # If the part is in the official geometry folder, then we must make sure we read the right file: 
            files_in_folder = [f for f in os.listdir(off_geo_path) if os.path.isfile(os.path.join(off_geo_path, f))]
            file_no = next((i for i, j in enumerate(files_in_folder) if geometry.lower() == splitAtNumber(j.lower())), None)
            list_of_paths.append( os.path.join(off_geo_path, files_in_folder[file_no] ) )

        else:
            # if the part is from the submission folder, then just read all files in the particular folder: 
            sub_geo_path = os.path.join(runSettings['submission geometry path'], geometry)
            list_of_paths += [os.path.join(sub_geo_path, f) for f in os.listdir(sub_geo_path) if all([os.path.isfile(os.path.join(sub_geo_path, f)), f.lower().endswith(".stl")]) ]

    return list_of_paths

def read_stls(list_of_paths, offset6dir = False):
    appendFilter = vtk.vtkAppendPolyData()
    sourceList = []
    for path in list_of_paths:
        reader = vtk.vtkSTLReader()
        reader.SetFileName(path)
        reader.Update()
        # sourceList.append( deepcopy(reader) )
        appendvtk(appendFilter, reader, offset6dir)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection( appendFilter.GetOutputPort() )

    actor = vtk.vtkActor()
    actor.SetMapper( mapper )

    return actor

def appendvtk(appendFilter, reader, offset6dir):
    appendInput = vtk.vtkPolyData()
    if offset6dir:
        transforms = [ 
            [ 0.001, 0, 0],
            [-0.001, 0, 0],
            [0,  0.001, 0],
            [0, -0.001, 0],
            [0, 0,  0.001],
            [0, 0, -0.001] ]
        for t in transforms:
            transform = vtk.vtkTransform()
            transform.Translate(t[0], t[1], t[2])

            transformedPolyData = vtk.vtkTransformPolyDataFilter()
            transformedPolyData.SetTransform(transform)
            transformedPolyData.SetInputData( reader.GetOutput() )
            transformedPolyData.Update()

            appendFilter.AddInputData(transformedPolyData.GetOutput())
            appendFilter.Update()

    else:
        appendInput.ShallowCopy(reader.GetOutput())

        appendFilter.AddInputData(appendInput)
        appendFilter.Update()
    
    return

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

def views2cam(views):
    return {
        'all' : cameraAllAngles(),
        'below' : cameraBelow(),
        'above': cameraAbove(),
        'top': cameraAbove(), 
        'sides': cameraSides(),
        'left side': cameraLHS(),
        'front': cameraFront()}[views]

# def _test_():
    
#     geometries = ["RV-RW-PROFILES_v", "RV-RW-PYLON_v", "rw_endplate"]
#     # geometries = ["rw_endplate"]

#     list_of_paths = get_list_of_paths(geometries)
#     print(list_of_paths)
#     actor = read_stls(list_of_paths, offset6dir= True)
#     actor.GetProperty().SetOpacity(0.2)

#     bounds = actor.GetMapper().GetInput().GetBounds()
#     print(bounds)

#     geo2 = ["rw_endplate"]
#     list2 = get_list_of_paths(geo2)
#     actor2 = read_stls(list2, offset6dir= False)
#     actor2.GetProperty().SetColor(1.0, 0.0, 0.0)

#     ren = vtk.vtkRenderer()
#     ren.AddActor( actor )
#     ren.AddActor( actor2 )
#     renwin = vtk.vtkRenderWindow()
#     renwin.AddRenderer(ren)

#     interactor = vtk.vtkRenderWindowInteractor()
#     interactor.SetRenderWindow(renwin)

#     renwin.Render()
#     interactor.Initialize()
#     interactor.Start()


# if __name__ == "__main__":
#     _test_()