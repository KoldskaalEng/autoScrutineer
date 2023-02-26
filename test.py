import os 
import vtk 
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy

path = os.getcwd()

submission_subfolder = os.listdir(path+'/submission')
print(submission_subfolder)

subfolderpath = os.path.join(path, 'submission', submission_subfolder[0])

files = [f for f in os.listdir(subfolderpath) if os.path.isfile(os.path.join(subfolderpath, f))]
print(files)

### test writing vtk info directly to numpy array

reader = vtk.vtkSTLReader()
reader.SetFileName('referenceGeometry/RV-RW.stl')

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

testActor = vtk.vtkActor()
testActor.SetMapper(mapper)

ren = vtk.vtkRenderer()
ren.AddActor(testActor)



renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(800,600)

# vtk to image filter
vtk_win_im = vtk.vtkWindowToImageFilter()
vtk_win_im.SetInput(renWin)
vtk_win_im.Update()

vtk_image = vtk_win_im.GetOutput()

width, height, _ = vtk_image.GetDimensions()
vtk_array = vtk_image.GetPointData().GetScalars()
components = vtk_array.GetNumberOfComponents()

arr = vtk_to_numpy(vtk_array).reshape(height, width, components)


iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
iren.SetRenderWindow(renWin)
iren.Initialize()
renWin.Render()

iren.Start()

