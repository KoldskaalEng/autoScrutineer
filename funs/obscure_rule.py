import vtk
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy
from util_funs import *

def ruleObscure(rule, settings): 
    # Creating actors for reference geometry and given geometry. 
    source_ref, actor_ref = ruleStr2vtk(rule['ref_geometry'])
    source_given, actor_given = ruleStr2vtk(rule['given_geometry'])

    # Creating renderer, window and adding actors. 
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.SetOffScreenRendering(1) # Rendering in "offscreen mode" so a vtk window will not pop up. 
    renWin.AddRenderer(ren)
    renWin.SetSize(1920,1080)

    actor_ref, actor_given, ren = colorActors(actor_ref, actor_given, ren)
    
    ren.AddActor(actor_ref)
    ren.AddActor(actor_given)


    # Adding mask if specified. 
    if not rule['mask'] == 'none':
        s3, actor_mask = ruleStr2vtk(rule['mask'])
        actor_mask.GetProperty().SetColor( 0.1, 0.1, 0.1 )
        actor_mask.GetProperty().LightingOff()
        ren.AddActor(actor_mask)

    # Getting list of camera angles from the rule 
    camPos, camViewUp, camBool = views2cam(rule['angles'])

    # Setting up camera and focusing on the correct part
    if rule['focus'] == 'reference':
        bbCords, center, radius = getBoundingBoxCoords(source_ref)
    else:
        bbCords, center, radius = getBoundingBoxCoords(source_given)

    camera = vtk.vtkCamera()
    camera = setCameraProj(camera, camBool)
    ren.SetActiveCamera(camera)

    # iterate through all camera positions. 
    for j in range(len(camPos)):
        ren.ResetCamera()

        # Reposition camera
        camera.SetFocalPoint(center)
        camera.SetViewUp(camViewUp[j,:])

        p = camPos[j,:]
        mag = ((p[0]**2) + (p[1]**2) + (p[2]**2))**(0.5)
        p1 = center + 4*radius*p/mag
        camera.SetClippingRange(0.01*radius,100*radius)
        camera.SetPosition(p1)

        # Render scene 
        renWin.Render()

        # Creating vtk array from a vtk-image from the hidden renderwindow, then converting said vtk_array into a numpy array to check for red pixels. 
        w2if = vtk.vtkWindowToImageFilter() # w2if = window to image filter
        w2if.SetInput(renWin)
        w2if.Update()

        vtk_img = w2if.GetOutput()

        width, height, _ = vtk_img.GetDimensions()
        vtk_array = vtk_img.GetPointData().GetScalars()
        components = vtk_array.GetNumberOfComponents()

        img = vtk_to_numpy(vtk_array).reshape(height, width, components)
        
        ## Checking the numpy array for red pixels 
        if np.max(img[:,:,0])>200: # Clearly visible red pixel should be ~229

            reportStr = 'Submission violates ' + rule['rule_section_name'] + '\n'

            # If a violation is found, then at least two images are saved: the image containing the violation, and a second image with transparent reference geometry.  
            # If the setting save all non compliance is TRUE then all angles will be tested. if the setting is FALSE, then the loop will break after the first violation is found. 

            # Write the image used for scrutineering. 
            writer = vtk.vtkPNGWriter()
            writer.SetInputConnection(w2if.GetOutputPort())

            w2if.Update()
            renderedImageScrt = settings['submission geometry path'] + 'renderedImages/Rule' + rule['rule_section_name'] + '_Image' + str(j) + '_scrt.png' 

            writer.SetFileName(renderedImageScrt)
            writer.Update()
            writer.Write()

            # Write an illustration image.
            illustrationColors(actor_ref, actor_given, ren, settings)
            renWin.Render()

            w2if2 = vtk.vtkWindowToImageFilter()
            w2if2.SetInput(renWin)
            w2if2.Update()
            
            renderedImageIll = settings['submission geometry path'] + 'renderedImages/Rule' + rule['rule_section_name'] + '_Image' + str(j) + '_ill.png' 
            writer2 = vtk.vtkPNGWriter()
            writer2.SetInputConnection(w2if2.GetOutputPort())
            writer2.SetFileName(renderedImageIll)
            writer2.Update()
            writer2.Write()

            # Undo illustration color settings 
            colorActors(actor_ref, actor_given, ren)

            #combinePNGsToGIF(renderedImageScrt, renderedImageIll, 'renderedImages/Rule' + rule['rule_section_name']  + '_Image' + str(j))

            del w2if, w2if2, writer, writer2

            if not settings['saved image settings']['Save all non-compliant images']:
                break

        else:
            reportStr = 'Submission complies with ' + rule['rule_section_name'] + '\n'

    return reportStr