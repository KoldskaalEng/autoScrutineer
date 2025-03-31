import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from vtk_funs import *
from settings import *
from skimage.segmentation import flood_fill, flood
from nSections_rule import semiRandomSamples, Read_and_cut_stl

def countVerticalIntersections(img):
    # bucket fill to ensure no overlaps are counted. 
    corner = (0,0)
    img = flood(img, corner) # Air = 1, geometry = 0
    sz = np.shape(img)

    max_intersections = 0
    for i in range(sz[1]): # Look every column of pixels one at a time
        column = img[:,i]
        intersections = 0
        if min(column) == 0: # Check if there are any intersections at all. 
            
            while 1:
                border = np.argmin(column) # find the index of the first 0 in the column. 

                if not border == 0: # if border = 0, then there are no more 
                    intersections += 1
                    column = np.logical_not( column[border:] ) # invert values (so you only ever look for 0's) and remove region before the border. 
                else:
                    break

        max_intersections = max( (max_intersections, intersections) )            

    return max_intersections

def ruleTopBottomVisibility(rule, settings):

    condition, value = rule["number_of_intersections"].split(" ")
    verbose = runSettings['Verbose scrutineering']

    # Find the list of locations to section the geometry:
    try:
        if rule['sampling_method'] == 'semi_random':
            section_locs = semiRandomSamples( rule )
        else:
            section_locs = rule['probing_locations']
    except KeyError:
        print("Cannot find section locations")
    

    camPos, camViewUp, camBool = views2cam(rule['angle'])

    # Creating renderer and window. 
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.SetOffScreenRendering(1) # Rendering in "offscreen mode" so a vtk window will not pop up. 
    renWin.AddRenderer(ren)
    renWin.SetSize(1920,1080)
    # renWin.SetSize(1280,720)

    # Setting up camera and focusing on the part being cut
    geometries_2_cut = get_list_of_paths(rule["given_geometry"])
    combined_stls = read_stls(geometries_2_cut, offset6dir= False)

    bbCords, center, radius = getBoundingBoxCoords_actor(combined_stls)

    camera = vtk.vtkCamera()
    camera = setCameraProj(camera, camBool)
    ren.SetActiveCamera(camera)
    camera.SetFocalPoint(center)
    camera.SetViewUp(camViewUp[0,:])
    p = camPos[0,:]
    mag = (p[0]**2 + p[1]**2 + p[2]**2)**0.5
    p1 = center + 4*radius*p/mag
    camera.SetClippingRange(0.01*radius,100*radius)
    camera.SetPosition(p1)

    # Prepare math: 
    normal_vec = np.array(rule["cutting_plane_normal"])
    cutting_plane_normal = tuple( normal_vec )
    violation = False
    # Iterate through all sections:
    for i in range(len(section_locs)):

        
        ren.RemoveAllViewProps()
        cutting_plane_origin = tuple( section_locs[i] * normal_vec )
        # print("    Checking section: {}".format(cutting_plane_origin)) # Uncomment to see if it actually does something. 

        for geo in geometries_2_cut:
            section_actor = Read_and_cut_stl( geo, cutting_plane_normal, cutting_plane_origin )

            # Add the actor to the renderer: 
            ren.AddActor(section_actor)
        
        # Update renderwindow 
        ren.ResetCamera()
        renWin.Render()

        # Create numpy array from rendered image: 
        w2if = vtk.vtkWindowToImageFilter() # w2if = window to image filter
        w2if.SetInput(renWin)
        w2if.Update()

        vtk_img = w2if.GetOutput()
        width, height, _ = vtk_img.GetDimensions()
        vtk_array = vtk_img.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()
        img = vtk_to_numpy(vtk_array).reshape(height, width, components)

        # Convert to B/W images based on the red channel only, and count vertical intersections: 
        if verbose:
            print("section = {}, no {} of {}".format(section_locs[i], i, len(section_locs)))
        n_sections = countVerticalIntersections( img[:, :, 0] > 100 )
        if verbose:
            print("Number of intersections: {}".format(n_sections))

        # Determine legality
        if condition == "=" and not( n_sections == int(value) ):
            violation = True
        elif condition == "<=" and n_sections > int(value):
            violation = True

        if violation:
            ns = n_sections
            writer2 = vtk.vtkPNGWriter()
            writer2.SetInputConnection(w2if.GetOutputPort())
            renderedImageIll = settings['submission geometry path'] + 'renderedImages/Rule_' + rule['rule_section_name'] + '_Image' + str(i) + '.png' 
            # Skriv sektion coordinater til filnavnet
            writer2.SetFileName(renderedImageIll)
            writer2.Update()
            writer2.Write()

            if not settings['saved image settings']['Save all non-compliant images']:
                break
    if violation:
        reportStr = "Violates " + rule["rule_section_name"] + ", top/bottom visibility is not satisfied in plane through point: ({:.4f},{:.4f},{:.4f})\n".format(cutting_plane_origin[0], cutting_plane_origin[1], cutting_plane_origin[2],)
    else:
        reportStr = 'Complies with ' + rule['rule_section_name'] + '\n'
    return reportStr

if __name__ == "__main__":

    testrule = {    
        'rule_section_name': 'testRule',           
        'rule_type': 'top bottom visibility',                      
        'angle': 'left side',
        'number_of_intersections': "<= 2", # 2 intersections means top and bottom visible. more than 2 means something is overhanging.                              
        'given_geometry': 'floor',                                     
        'cutting_plane_normal' : [0, 1, 0],
        'sampling_method': 'specific',
        'sampling_method': 'semi_random',
        'sampling_interval': (0.0, 0.25),
        'max_unprobed_interval': 25e-3,
        'probing_locations': np.array([ 0.175 ]),
    }

    a = ruleTopBottomVisibility(testrule, runSettings)
    print(a)