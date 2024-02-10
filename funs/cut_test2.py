import vtk

def create_cut_actor(stl_reader, cutting_plane_normal, cutting_plane_origin):
    # Create a cut plane
    cut_plane = vtk.vtkPlane()
    cut_plane.SetNormal(cutting_plane_normal)
    cut_plane.SetOrigin(cutting_plane_origin)

    # Create a cutter
    cutter = vtk.vtkCutter()
    cutter.SetCutFunction(cut_plane)
    cutter.SetInputConnection(stl_reader.GetOutputPort())

    # Create a mapper for the cut actor
    cut_mapper = vtk.vtkPolyDataMapper()
    cut_mapper.SetInputConnection(cutter.GetOutputPort())

    # Create an actor for the cut section
    cut_actor = vtk.vtkActor()
    cut_actor.SetMapper(cut_mapper)
    cut_actor.GetProperty().SetRepresentationToWireframe()  # Show the cut section in a red outline
    cut_actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Set the color of the outline

    return cut_actor, cutter

def main():
    # Create a renderer
    renderer = vtk.vtkRenderer()

    # Create a render window
    render_window = vtk.vtkRenderWindow()
    render_window.SetWindowName("STL File Cut Section Outline")
    render_window.SetSize(800, 600)
    render_window.AddRenderer(renderer)

    # Create a render window interactor
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # Read STL file
    stl_reader = vtk.vtkSTLReader()
    stl_reader.SetFileName("team1_submission/body/body_sidepod.stl")

    # Create and add the cut actor to the renderer
    cutting_plane_normal = (1.0, 0.0, 0.0)  # Normal vector aligned with x-axis
    cutting_plane_origin = (2.0, 0.0, 0.0)  # Origin at (2.0, 0.0, 0.0)
    cut_actor, cutter = create_cut_actor(stl_reader, cutting_plane_normal, cutting_plane_origin)
    renderer.AddActor(cut_actor)

    # Set up the camera and render
    renderer.ResetCamera()
    render_window.Render()



    # Test image writing that suddenly doesn't work...
    w2if = vtk.vtkWindowToImageFilter() # w2if = window to image filter
    w2if.SetInput(render_window)
    w2if.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetInputConnection(w2if.GetOutputPort())

    writer.SetFileName("test.png")
    writer.Update()
    writer.Write()

    # Start the interactor
    render_window_interactor.Start()


if __name__ == "__main__":
    main()
