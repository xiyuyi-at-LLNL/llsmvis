"""
Haichao Miao @ LLNL, 2021.
"""
import vtk
import numpy as np
import os

def extract_surface(th, fpath, output_dir, morph_open=True, morph_close=True, kernel_size=3, save_mask=False, surface_smoothing_steps=0):
    #get reader to load tiff file
    reader = vtk.vtkTIFFReader()
    reader.SetFileName(fpath)
    reader.Update()

    tn = os.path.split(fpath)[-1]
    name = tn.split('.')[0]

    print('EXTRACT SURFACE ', name)

    print('input file is', fpath)
    
    print('create binary mask with threshold', th)

    thf = vtk.vtkImageThreshold()
    thf.SetInputConnection(reader.GetOutputPort())
    thf.ThresholdByLower(th)
    thf.ReplaceInOn()
    thf.SetInValue(0)  # values below th -> 0
    thf.ReplaceOutOn()
    thf.SetOutValue(1)  # values above th -> 0
    thf.Update()    

    if(morph_open or morph_close):
        print("kernel size for morphological operation is", kernel_size)
    
    if(morph_close):
        print('Apply closing operation')
        
        c = vtk.vtkImageOpenClose3D()
        c.SetInputConnection(thf.GetOutputPort())
        c.SetOpenValue(0)
        c.SetCloseValue(1)
        c.SetKernelSize(3,3,3)
        c.Update()

    if(morph_open):
        print('Apply opening operation')

        o = vtk.vtkImageOpenClose3D()
        o.SetInputConnection(c.GetOutputPort())
        o.SetOpenValue(1)
        o.SetCloseValue(0)
        o.SetKernelSize(3,3,3)
        o.Update()

    print('Apply marching cubes')
    mc = vtk.vtkDiscreteMarchingCubes()
    mc.SetInputConnection(o.GetOutputPort())
    mc.GenerateValues(1, 1, 1)
    mc.Update()

    if (save_mask):
        print('save binary mask to', output_dir)
        out_mask = os.path.join(output_dir,name+"_mask.tif")
        writer = vtk.vtkTIFFWriter()
        writer.SetInputConnection(o.GetOutputPort())
        writer.SetFileName(out_mask)
        writer.Write()

    print('Get the largest connected component')

    #We only want the largest connected component
    con = vtk.vtkPolyDataConnectivityFilter()
    con.SetInputData(mc.GetOutput())
    con.SetExtractionModeToLargestRegion()
    con.Update()

    surface = con.GetOutput()
    
    if(surface_smoothing_steps > 0):
        r = 0.1
        print('smooth surface with laplacian filter with {} steps and relaxation factor {}'.format(surface_smoothing_steps, r))
        smooth = vtk.vtkSmoothPolyDataFilter()

        smooth.SetNumberOfIterations(surface_smoothing_steps)
        smooth.SetInputData(surface)
        smooth.SetRelaxationFactor(r)
        smooth.Update()
        surface = smooth.GetOutput()

    print('save surface to', output_dir)

    writer = vtk.vtkSTLWriter()
    writer.SetInputData(surface)
    writer.SetFileTypeToBinary()
    out = name + "{}_{}.stl".format(th,surface_smoothing_steps)
    out_file = os.path.join(output_dir,out)
    writer.SetFileName(out_file)
    writer.Write()

    return out_file

def get_cone(output, center=(0,0,0), dir=(1,0,0), h=1.0, r=0.5, capping=True, resolution=64):
    """returns a cone.

    Parameters
    ----------
    center: center of middle axis

    dir : orientation of center axis of the cone.

    h : height

    r : radius of base circle 
    
    capping : cone has a base or not

    resolution : number of facets for cone sides

    """
    
    cone = vtk.vtkConeSource()
    cone.Update()

    cone.SetCapping(capping)
    cone.SetDirection(dir)
    cone.SetCenter(center)
    cone.SetHeight(h)
    cone.SetRadius(r)
    cone.SetResolution(resolution)
    cone.Update()
    
    
    # Write the stl file to disk
    stlWriter = vtk.vtkSTLWriter()
    stlWriter.SetFileName(output)
    stlWriter.SetInputData(cone.GetOutput())
    stlWriter.Write()
    
    return cone

def get_cell_cone_intersection(cell_surface_fpath, cone_fpath, intersection_surface_fpath):
    
    cell = vtk.vtkSTLReader()
    cell.SetFileName(cell_surface_fpath)
    cell.Update()
    
    cone = vtk.vtkSTLReader()
    cone.SetFileName(cone_fpath)
    cone.Update()
    
    intersect = vtk.vtkBooleanOperationPolyDataFilter()
    intersect.SetOperation(1)
    intersect.SetInputData(0,cell.GetOutput())
    intersect.SetInputData(1,cone.GetOutput())
    intersect.Update()
    
    # Write the stl file to disk
    stlWriter = vtk.vtkSTLWriter()
    stlWriter.SetFileName(intersection_surface_fpath)
    stlWriter.SetInputConnection(intersect.GetOutputPort())
    stlWriter.Write()

    
def get_volume_surface_area(fpath):
    
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fpath)
    reader.Update()
    
    properties = vtk.vtkMassProperties()
    properties.SetInputConnection(reader.GetOutputPort())
    volume = properties.GetVolume()
    surface_area = properties.GetSurfaceArea()
    
    return [volume, surface_area]

def get_cut(cell_surface_fpath, cone_fpath, cut_cell_fpath, cut_protrusion_fpath, cone_protrusion_fpath):
    
    cell = vtk.vtkSTLReader()
    cell.SetFileName(cell_surface_fpath)
    cell.Update()
    
    cone = vtk.vtkSTLReader()
    cone.SetFileName(cone_fpath)
    cone.Update()
    
    implicitCone = vtk.vtkImplicitPolyDataDistance()
    implicitCone.SetInput(cone.GetOutput())
    
    clipper_inside = vtk.vtkClipPolyData()
    clipper_inside.SetInputConnection(cell.GetOutputPort())
    clipper_inside.SetClipFunction(implicitCone)
    clipper_inside.InsideOutOn()
    clipper_inside.SetValue(0.0)
    clipper_inside.GenerateClippedOutputOn()
    clipper_inside.Update()
    
    clipper_outside = vtk.vtkClipPolyData()
    clipper_outside.SetInputConnection(cell.GetOutputPort())
    clipper_outside.SetClipFunction(implicitCone)
    clipper_outside.SetValue(0.0)
    clipper_outside.GenerateClippedOutputOn()
    clipper_outside.Update()
    
    con_cell = vtk.vtkPolyDataConnectivityFilter()
    con_cell.SetInputData(clipper_outside.GetOutput())
    con_cell.SetExtractionModeToLargestRegion()
    con_cell.Update()
    
    n = con_cell.GetNumberOfExtractedRegions()
    print("num of regions", n)
    con_cell.SetExtractionModeToSpecifiedRegions()
    con_cell.Update()

    cell_polydata_list = []

    largest_region_idx = 0
    largest_region_vol = 0
    for region in range(0, n):
        con_cell.InitializeSpecifiedRegionList()
        con_cell.AddSpecifiedRegion(region)
        con_cell.Update()

        p = vtk.vtkPolyData()
        p.DeepCopy(con_cell.GetOutput())

        properties = vtk.vtkMassProperties()
        properties.SetInputData(p)
        volume = properties.GetVolume()
        
        if(volume > largest_region_vol):
            largest_region_vol = volume
            largest_region_idx = region
        
        print('volume of component {} is {}'.format(region, volume))
        
        #output components as stl        
        if (False): 
            stlWriter = vtk.vtkSTLWriter()
            path = r'C:\Users\miao1\Data\h3pd\cone test 2\cut_cell_{}.stl'.format(region)
            stlWriter.SetFileName(path)
            stlWriter.SetInputData(p)
            stlWriter.Write()
        
        cell_polydata_list.append(p)

    append_protrusion_filter = vtk.vtkAppendPolyData()
    
    for region in range(0, n):
        if region == largest_region_idx:
            continue
        append_protrusion_filter.AddInputData(cell_polydata_list[region])
        append_protrusion_filter.Update()
    
    append_protrusion_filter.AddInputConnection(clipper_inside.GetOutputPort())
    append_protrusion_filter.Update()
    
    protrusion_stlWriter = vtk.vtkSTLWriter()
    protrusion_stlWriter.SetFileName(cut_protrusion_fpath)
    protrusion_stlWriter.SetInputConnection(append_protrusion_filter.GetOutputPort())
    protrusion_stlWriter.Write()

    cut_cell_stlWriter = vtk.vtkSTLWriter()
    cut_cell_stlWriter.SetFileName(cut_cell_fpath)
    cut_cell_stlWriter.SetInputData(cell_polydata_list[largest_region_idx])
    cut_cell_stlWriter.Write()
    
    #get the inner cone
    implicitCell = vtk.vtkImplicitPolyDataDistance()
    implicitCell.SetInput(cell.GetOutput())
    
    subdivision_filter = vtk.vtkLinearSubdivisionFilter()
    subdivision_filter.SetNumberOfSubdivisions(3)
    subdivision_filter.SetInputData(cone.GetOutput())
    subdivision_filter.Update()
        
    clipper_cone = vtk.vtkClipPolyData()
    clipper_cone.SetInputConnection(subdivision_filter.GetOutputPort())
    clipper_cone.SetClipFunction(implicitCell)
    clipper_cone.InsideOutOn()
    clipper_cone.SetValue(0.0)
    clipper_cone.GenerateClippedOutputOn()
    clipper_cone.Update()
    
    con_cone = vtk.vtkPolyDataConnectivityFilter()
    con_cone.SetInputData(clipper_cone.GetOutput())
    con_cone.SetExtractionModeToLargestRegion()
    con_cone.Update()
    
    n = con_cone.GetNumberOfExtractedRegions()
    print("num of regions", n)
    con_cone.SetExtractionModeToLargestRegion()
    con_cone.Update()
    
    append_all_filter = vtk.vtkAppendPolyData()
    
    append_all_filter.AddInputConnection(append_protrusion_filter.GetOutputPort())
    append_all_filter.AddInputConnection(con_cone.GetOutputPort())
    append_all_filter.Update()
    
    cone_protrusion_stlWriter = vtk.vtkSTLWriter()
    cone_protrusion_stlWriter.SetFileName(cone_protrusion_fpath)
    cone_protrusion_stlWriter.SetInputConnection(append_all_filter.GetOutputPort())
    cone_protrusion_stlWriter.Write()
    
def calc_morphometrics(fpath):
    
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fpath)
    reader.Update()
    
    properties = vtk.vtkMassProperties()
    properties.SetInputConnection(reader.GetOutputPort())
    surface_area = properties.GetSurfaceArea()
    volume = properties.GetVolume()
    
    print("surface area", surface_area)
    print("volume", volume)
    
    ratio = surface_area / volume
    print("ratio", ratio)
    
    # pca = vtk.vtkPCAAnalysisFilter()
    # pca.SetInputConnection(reader.GetOutputPort())
    # pca.Update()
    
    return [surface_area, volume]

