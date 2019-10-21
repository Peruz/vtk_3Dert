from vtk import (vtkUnstructuredGridReader, vtkDataSetMapper, vtkActor,
                 vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor)
import vtk
import os

"""

reader(datafile) -> mapper(reader.GetOutputPort(), LookupTable) -> actor(mapper) -> render(actor1, ...) -> window(render)

"""

def read_vtk(fileName, scalarName):
    reader = vtkUnstructuredGridReader()
    reader.SetFileName(fileName)
    reader.SetScalarsName(scalarName)
    reader.Update()  # Needed because of GetScalarRange
    return(reader)
    
def lookup_table(output):
    scalar_range = output.GetScalarRange()
    lut = vtk.vtkLookupTable()
    #lut.SetTableRange(scalar_range)
    lut.SetTableRange(30, 500)
    lut.SetNumberOfColors(50)
    lut.SetHueRange(0.667, 0.0)
    lut.SetNumberOfColors(256)
    lut.Build()
    return(lut)
    
def data_actor(output_port, lut):
    data_mapper = vtkDataSetMapper()
    data_mapper.SetInputConnection(output_port)
    data_mapper.SetLookupTable(lut)
    data_mapper.SetUseLookupTableScalarRange(True)
    data_actor = vtkActor()
    data_actor.SetMapper(data_mapper)
    return(data_actor)

def axes2D_actor(output_port, renderer):
    fontsize=100
    cubeAxes_actor = vtk.vtkCubeAxesActor2D()
    cubeAxes_actor.SetInputConnection(output_port)
    cubeAxes_actor.SetCamera(renderer.GetActiveCamera())
    cubeAxes_actor.SetLabelFormat("%1.2g")
    cubeAxes_actor.GetAxisLabelTextProperty().SetColor(0,0,0)
    cubeAxes_actor.GetAxisLabelTextProperty().BoldOn()
    cubeAxes_actor.GetAxisLabelTextProperty().SetFontSize(fontsize)
    cubeAxes_actor.GetAxisTitleTextProperty().SetFontSize(fontsize)
    cubeAxes_actor.GetAxisTitleTextProperty().SetColor(0, 0, 0)
    cubeAxes_actor.GetProperty().SetColor(0, 0, 0)
    cubeAxes_actor.GetAxisLabelTextProperty().SetUseTightBoundingBox(1)
    cubeAxes_actor.SetFlyModeToOuterEdges()
    cubeAxes_actor.SetVisibility(1)
    cubeAxes_actor.SetZAxisVisibility(0)
    cubeAxes_actor.SetYAxisVisibility(1)
    cubeAxes_actor.SetXAxisVisibility(1)
    cubeAxes_actor.SetFontFactor(1.5)
    return(cubeAxes_actor)

def axes_actor(output_port, renderer, reader):
    axis1Color = [0, 0, 0]
    axis2Color = [0, 0, 0]
    axis3Color = [0, 0, 0]
    fontsize = 50
    cubeAxesActor = vtk.vtkCubeAxesActor()
    cubeAxesActor.SetUseTextActor3D(1)
    cubeAxesActor.SetBounds(reader.GetOutput().GetBounds())
    cubeAxesActor.SetCamera(renderer.GetActiveCamera())
    cubeAxesActor.DrawXGridlinesOn()
    cubeAxesActor.DrawYGridlinesOn()
    cubeAxesActor.DrawZGridlinesOn()
    cubeAxesActor.XAxisMinorTickVisibilityOff()
    cubeAxesActor.YAxisMinorTickVisibilityOff()
    cubeAxesActor.ZAxisMinorTickVisibilityOff()
    cubeAxesActor.SetGridLineLocation(cubeAxesActor.VTK_GRID_LINES_FURTHEST)
    cubeAxesActor.SetGridLineLocation(10)
    #cubeAxesActor.SetFlyModeToStaticEdges()
    cubeAxesActor.GetTitleTextProperty(0).SetFontSize(16)
    cubeAxesActor.GetLabelTextProperty(0).SetFontSize(16)
    cubeAxesActor.GetTitleTextProperty(0).SetColor(axis1Color)
    cubeAxesActor.GetLabelTextProperty(0).SetColor(axis1Color)
    cubeAxesActor.GetLabelTextProperty(1).SetFontSize(fontsize)
    cubeAxesActor.GetTitleTextProperty(1).SetFontSize(fontsize)
    cubeAxesActor.GetTitleTextProperty(1).SetColor(axis2Color)
    cubeAxesActor.GetLabelTextProperty(1).SetColor(axis2Color)
    cubeAxesActor.GetLabelTextProperty(2).SetFontSize(fontsize)
    cubeAxesActor.GetTitleTextProperty(2).SetFontSize(fontsize)
    
    cubeAxesActor.GetTitleTextProperty(2).SetColor(axis3Color)
    cubeAxesActor.GetLabelTextProperty(2).SetColor(axis3Color)
    cubeAxesActor.SetLabelOffset(20)  # default 20
    cubeAxesActor.SetTitleOffset(20)  # default 20
    cubeAxesActor.SetXUnits('m')
    cubeAxesActor.SetYUnits('m')
    cubeAxesActor.SetZUnits('m')
    cubeAxesActor.SetXTitle('x')
    cubeAxesActor.SetYTitle('y')
    cubeAxesActor.SetZTitle('z')
    cubeAxesActor.SetXLabelFormat("%2.2g")
    cubeAxesActor.SetYLabelFormat("%2.2g")
    cubeAxesActor.SetZLabelFormat("%2.2g")
    cubeAxesActor.SetYAxisTickVisibility(0)
    cubeAxesActor.SetTitleScaling(7, 3,3,3)
    #cubeAxesActor.SetScale(1,1,0.1)
    # cubeAxesActor.SetPosition(10, 0, 0)
    return(cubeAxesActor)

def colorbar_actor(lut):
    colorbar = vtk.vtkScalarBarActor()
    colorbar.SetLookupTable(lut)
    colorbar.SetWidth(0.12)
    colorbar.SetBarRatio(0.5)
    colorbar.SetHeight(0.7)
    colorbar.SetPosition(0.8, 0.1)
    colorbar.SetLabelFormat("%.3g")
    colorbar.PickableOff()
    #colorbar.VisibilityOn()
    colorbar.SetTitle("Rho \n [Ohm m]\n\n")
    colorbar.SetNumberOfLabels(10)
    colorbar.GetLabelTextProperty().SetColor(0,0,0)
    colorbar.GetLabelTextProperty().SetFontSize(10)
    colorbar.GetTitleTextProperty().SetColor(0,0,0)
    colorbar.GetTitleTextProperty().SetFontSize(10)
    #colorbar.GetTitleTextProperty().SetOrientation(0)
    #colorbar.GetTitleTextProperty().SetLineOffset(0.1)
    #colorbar.GetTitleTextProperty().SetLineSpacing(0.1)
    #colorbar.GetTitleTextProperty().SetUseTightBoundingBox(1)
    return(colorbar)

def renderer_options(renderer):
    renderer.SetBackground(0.9, 0.9, 0.9) # Set background to white
    renderer.GetActiveCamera().Azimuth(0)
    renderer.GetActiveCamera().Elevation(20)
    renderer.GetActiveCamera().Zoom(0.9)
    # renderer.GetActiveCamera().SetViewUp(0,0,0.5)
    # renderer.GetActiveCamera().Yaw(-20)
    # renderer.GetActiveCamera().Roll(-90)
    # renderer.GetActiveCamera().SetPosition(0, 1, 0.2)
    renderer.ResetCamera()
    return(renderer)
    
def renderer_window(renderer):
    renderer_window = vtkRenderWindow()
    renderer_window.AddRenderer(renderer)
    renderer_window.SetSize(1300, 1000)
    return(renderer_window)

def save_png(renderer_window, nameout):
    """ renderer_window -> WindowToImageFilter -> Writer -> png """ 
    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renderer_window)
    w2if.Update()
    
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(nameout)
    writer.SetInputData(w2if.GetOutput())
    writer.Write()
    
def interactor(renderer_window):
    """ Create the RendererWindowInteractor and display the vtk_file """
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderer_window)
    interactor.Initialize()
    interactor.Start()


files = [f for f in os.listdir() if (f.endswith('.vtk') and '2018' in f)]
for f in files:
    print(f)
    reader = read_vtk(f, 'res')
    output = reader.GetOutput()
    output_port = reader.GetOutputPort()

    rr = vtkRenderer()

    lut = lookup_table(output)
    data_act = data_actor(output_port, lut)
    #axes_act = axes2D_actor(output_port, rr)
    axes_act = axes_actor(output_port, rr, reader)
    colorbar_act = colorbar_actor(lut)
    
    rr.AddActor(data_act)
    rr.AddActor(colorbar_act)
    rr.AddActor(axes_act)
    
    rr = renderer_options(rr)
    rw = renderer_window(rr)
    
    nameout = f.replace('.vtk', '_ResVTK.png')
    save_png(rw, nameout)
    interactor(rw)
