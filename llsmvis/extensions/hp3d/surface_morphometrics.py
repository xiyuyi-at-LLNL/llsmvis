import sys
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