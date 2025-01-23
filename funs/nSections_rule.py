import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from vtk_funs import *
from settings import *
from skimage.segmentation import flood_fill, flood
# 2do: 
# cut_test2.py works to create sections of a file. 
# fill outline test works for processing the rendered image. 

def semiRandomSamples(rule):
    upper = max(rule['sampling_interval'])
    lower = min(rule['sampling_interval'])
    max_dist = rule['max_unprobed_interval']
    n_init = int( (upper-lower)/max_dist ) 
    x = np.sort( (lower + np.random.rand(n_init))*(upper-lower) )
    x = np.concatenate( ([lower], x) )
    while 1:
        d = np.diff(x)
        too_big = d > max_dist
        if not np.any(too_big):
            break
        x = np.sort( np.concatenate( (x, x[np.where(too_big)] + 0.5 * d[np.where(too_big)]) ) )

    return x

def Read_and_cut_stl(path_to_file, cutting_plane_normal, cutting_plane_origin):
    # I hate how this works. 
    cwd = os.getcwd()
    reader = vtk.vtkSTLReader()
    reader.SetFileName( path_to_file )
    reader.Update()

    # Plane used for cutting: 
    cut_plane = vtk.vtkPlane()
    cut_plane.SetNormal(cutting_plane_normal)
    cut_plane.SetOrigin(cutting_plane_origin)

    # Create a cutter
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(cut_plane)
    cutter.SetInputConnection(reader.GetOutputPort())

    # Create a mapper for the cut actor
    cut_mapper = vtk.vtkPolyDataMapper()
    cut_mapper.SetInputConnection(cutter.GetOutputPort())

    cut_actor = vtk.vtkActor()
    cut_actor.SetMapper(cut_mapper)
    # cut_actor.GetProperty().SetRepresentationToWireframe()  # Show the cut section in a red outline
    cut_actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Set the color of the outline

    return cut_actor

def get_list_of_paths(geometries):
    list_of_paths = []
    if isinstance(geometries, str):
        geometries = [geometries]
    
    for geometry in geometries:
        # Check if it is an RV/RS
        if geometry[0:3] in ('RV-', 'RV_', 'RS-', 'RS_'):
            ref_geo_path = runSettings['reference geometry path']
            # This ugly list comprehension stuff is added, so that you dont need to specify the version number for the reference geometries in the rules. 
            ref_files = [f for f in os.listdir(ref_geo_path) if os.path.isfile(os.path.join(ref_geo_path, f))]
            file_no = next((i for i, j in enumerate(ref_files) if geometry.lower() in j.lower()), None)
            list_of_paths.append(ref_files[file_no])

        # Check if it is the mandatory parts
        if geometry == "MandParts":
            mand_geo_path = runSettings['mandatory geometry path']
            list_of_paths += [os.path.join(mand_geo_path, f) for f in os.listdir(mand_geo_path) if os.path.isfile(os.path.join(mand_geo_path, f))]

        # Otherwise read from the submission:
        else:
            sub_geo_path = os.path.join(runSettings['submission geometry path'], geometry)
            list_of_paths += [os.path.join(sub_geo_path, f) for f in os.listdir(sub_geo_path) if os.path.isfile(os.path.join(sub_geo_path, f))]

    return list_of_paths

def countSections(img: np.ndarray, corner: tuple = (0,0)):
    """ Counts the number of sections in the image by "flood-filling" the surrounding air, and then iteratively counting and filling the remaining parts of the image.
    Assumes that img is a B/W boolean array. 
    where 0 = False = air, and 1 = section outlines
    corner, tuple, must be one of:
        ( 0,  0)
        ( 0, -1)
        (-1,  0)
        (-1, -1) """
    
    img = flood( img, corner )
    sz = np.size(img)

    n_sections = 0
    while 1:

        # plt.figure(figsize=(6, 6))
        # # plt.imshow(bw_img, cmap = "gray")
        # plt.imshow(img, cmap='gray')
        # plt.title("Boolean Array Visualization")
        # plt.axis('off')  # Turn off axis labels
        # plt.show()
        
        non_zero = np.nonzero(img < 0.5)

        if len(non_zero[0]):
            # print( "Next to fill {}, {}".format(non_zero[0][0], non_zero[1][0] ) )
            img = flood_fill( img, (non_zero[0][0], non_zero[1][0]), True )
            n_sections += 1
        else:
            break

    return n_sections

def ruleNSections(rule, settings):

    condition, value = rule["number_of_sections"].split(" ")

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

    # Setting up camera and focusing on the part being cut
    combined_stls, _ = ruleStr2vtk(rule['given_geometry'])
    bbCords, center, radius = getBoundingBoxCoords(combined_stls)

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

    geometries_2_cut = get_list_of_paths(rule["given_geometry"])

    # Iterate through all sections:
    for i in range(len(section_locs)):

        violation = False
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

        # Convert to B/W images based on the red channel only, and count sections: 
        n_sections = countSections( img[:, :, 0] > 100 )

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
            writer2.SetFileName(renderedImageIll)
            writer2.Update()
            writer2.Write()

            if not settings['saved image settings']['Save all non-compliant images']:
                break
    if violation:
        reportStr = "Violates " + rule["rule_section_name"] + ", illegal number of sections in plane through point: ({:.4f},{:.4f},{:.4f})\n".format(cutting_plane_origin[0], cutting_plane_origin[1], cutting_plane_origin[2],)
        reportStr += "    Number of sections must be {}, but {} sections found. \n".format(rule['number_of_sections'], ns)
    else:
        reportStr = 'Complies with ' + rule['rule_section_name'] + '\n'
    return reportStr

if __name__ == "__main__":
    # For testing
    from testRules2025 import allRules
    from settings import runSettings
    # runSettings["submission geometry path"] = 'test_submission_2\\'
    # rule = allRules[4]
    # a = semiRandomSamples(rule)
    # print(a)
    # ruleNSections(rule, 0)

