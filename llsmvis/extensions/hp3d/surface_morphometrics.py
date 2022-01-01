"""
Haichao Miao @ LLNL, 2021.
"""
import vtk
import numpy as np
import os

def extract_surface(th, fpath, output_dir,
                    morph_open=True, morph_close=True,
                    kernel_size=3, save_mask=False,
                    surface_smoothing_steps=0,
                    verbose=True):
    # get reader to load tiff file
    reader = vtk.vtkTIFFReader()
    reader.SetFileName(fpath)
    reader.Update()

    tn = os.path.split(fpath)[-1]
    name = tn.split('.')[0]

    if verbose:
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
        if verbose:
            print("kernel size for morphological operation is", kernel_size)
    
    if(morph_close):
        if verbose:
            print('Apply closing operation')
        c = vtk.vtkImageOpenClose3D()
        c.SetInputConnection(thf.GetOutputPort())
        c.SetOpenValue(0)
        c.SetCloseValue(1)
        c.SetKernelSize(3,3,3)
        c.Update()

    if(morph_open):
        if verbose:
            print('Apply opening operation')
        o = vtk.vtkImageOpenClose3D()
        o.SetInputConnection(c.GetOutputPort())
        o.SetOpenValue(1)
        o.SetCloseValue(0)
        o.SetKernelSize(3,3,3)
        o.Update()

    if verbose:
        print('Apply marching cubes')
    mc = vtk.vtkDiscreteMarchingCubes()
    mc.SetInputConnection(o.GetOutputPort())
    mc.GenerateValues(1, 1, 1)
    mc.Update()

    if save_mask:
        if verbose:
            print('save binary mask to', output_dir)
        out_mask = os.path.join(output_dir,name+"_mask.tif")
        writer = vtk.vtkTIFFWriter()
        writer.SetInputConnection(o.GetOutputPort())
        writer.SetFileName(out_mask)
        writer.Write()

    if verbose:
        print('Get the largest connected component')

    # We only want the largest connected component
    con = vtk.vtkPolyDataConnectivityFilter()
    con.SetInputData(mc.GetOutput())
    con.SetExtractionModeToLargestRegion()
    con.Update()
    surface = con.GetOutput()
    if surface_smoothing_steps > 0:
        r = 0.1
        if verbose:
            print('smooth surface with laplacian filter with {} steps and relaxation factor {}'.format(surface_smoothing_steps, r))
        smooth = vtk.vtkSmoothPolyDataFilter()
        smooth.SetNumberOfIterations(surface_smoothing_steps)
        smooth.SetInputData(surface)
        smooth.SetRelaxationFactor(r)
        smooth.Update()
        surface = smooth.GetOutput()
    if verbose:
        print('save surface to', output_dir)

    writer = vtk.vtkSTLWriter()
    writer.SetInputData(surface)
    writer.SetFileTypeToBinary()
    out = name + "{}_{}.stl".format(th,surface_smoothing_steps)
    out_file = os.path.join(output_dir,out)
    writer.SetFileName(out_file)
    writer.Write()

    return out_file


def get_cone(output,
             center=(0, 0, 0),
             dir=(1, 0, 0),
             h=1.0,
             r=0.5,
             capping=True,
             resolution=64,
             return_polydata=False):
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

    if return_polydata:
        result=cone.GetOutput()
    else:
        result=cone

    return result


def get_cell_cone_intersection(cell_surface_fpath=None,
                               cone_fpath=None,
                               intersection_surface_fpath=None,
                               use_stl_filepaths=True,
                               cell_polydata=None,
                               cone_polydata=None,
                               write_output_as_stl=True):

    if use_stl_filepaths:
        # load the cell stl, and get its polydata
        cell = vtk.vtkSTLReader()
        cell.SetFileName(cell_surface_fpath)
        cell.Update()
        cell_polydata=cell.GetOutput()

        # load the cone  stl, and get its polydata
        cone = vtk.vtkSTLReader()
        cone.SetFileName(cone_fpath)
        cone.Update()
        cone_polydata=cone.GetOutput()

    # calculate intersect of the two cell_polydata and cone_polydata
    intersect = vtk.vtkBooleanOperationPolyDataFilter()
    intersect.SetOperation(1)
    intersect.SetInputData(0, cell_polydata)
    intersect.SetInputData(1, cone_polydata)
    intersect.Update()

    if write_output_as_stl is True:
        # Write the stl file to disk
        stlWriter = vtk.vtkSTLWriter()
        stlWriter.SetFileName(intersection_surface_fpath)
        stlWriter.SetInputConnection(intersect.GetOutputPort())
        stlWriter.Write()

    return intersect.GetOutput()


def get_volume_surface_area(fpath=None, polydata=None, usestl=True, returnfmt='list', verbose=False):
    if usestl:
        reader = vtk.vtkSTLReader()
        reader.SetFileName(fpath)
        reader.Update()
        polydata=reader.GetOutput()

    properties = vtk.vtkMassProperties()
    properties.SetInputData(polydata)
    volume = properties.GetVolume()
    surface_area = properties.GetSurfaceArea()
    if returnfmt == 'list':
        if verbose:
            print('return format is list')
        result = [volume, surface_area]

    if returnfmt == 'dict':
        if verbose:
            print('return format is dict')
        result = {}
        result.update({'surface area': surface_area})
        result.update({'volume': volume})

    return result


def get_cut(cell_surface_fpath=None,
            cone_fpath=None,
            cut_cell_fpath=None,
            cut_protrusion_fpath=None,
            cone_protrusion_fpath=None,
            use_stl_filepaths=True,
            cell_polydata=None,
            cone_polydata=None,
            write_output_cone_protrusion_as_stl=True,
            write_output_protrusion_as_stl=True,
            write_output_cell_cut_as_stl=False,
            verbose=False):

    if use_stl_filepaths is True:
        cell = vtk.vtkSTLReader()
        cell.SetFileName(cell_surface_fpath)
        cell.Update()
        cell_polydata = cell.GetOutput()
    
        cone = vtk.vtkSTLReader()
        cone.SetFileName(cone_fpath)
        cone.Update()
        cone_polydata=cone.GetOutput()
    
    implicitCone = vtk.vtkImplicitPolyDataDistance()
    implicitCone.SetInput(cone_polydata)
    
    clipper_inside = vtk.vtkClipPolyData()
    clipper_inside.SetInputData(cell_polydata)
    clipper_inside.SetClipFunction(implicitCone)
    clipper_inside.InsideOutOn()
    clipper_inside.SetValue(0.0)
    clipper_inside.GenerateClippedOutputOn()
    clipper_inside.Update()
    
    clipper_outside = vtk.vtkClipPolyData()
    clipper_outside.SetInputData(cell_polydata)
    clipper_outside.SetClipFunction(implicitCone)
    clipper_outside.SetValue(0.0)
    clipper_outside.GenerateClippedOutputOn()
    clipper_outside.Update()
    
    con_cell = vtk.vtkPolyDataConnectivityFilter()
    con_cell.SetInputData(clipper_outside.GetOutput())
    con_cell.SetExtractionModeToLargestRegion()
    con_cell.Update()
    
    n = con_cell.GetNumberOfExtractedRegions()
    if verbose:
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

        if verbose:
            print('volume of component {} is {}'.format(region, volume))
        
        # output components as stl
        if (False): 
            stlWriter = vtk.vtkSTLWriter()
            path = r'C:\Users\miao1\Data\h3pd\cone test 2\cut_cell_{}.stl'.format(region)
            stlWriter.SetFileName(path)
            stlWriter.SetInputData(p)
            stlWriter.Write()
        
        cell_polydata_list.append(p)

    append_protrusion_filter = vtk.vtkAppendPolyData()
    cut_cell_polydata=cell_polydata_list[largest_region_idx]

    for region in range(0, n):
        if region == largest_region_idx:
            continue
        append_protrusion_filter.AddInputData(cell_polydata_list[region])
        append_protrusion_filter.Update()
    
    append_protrusion_filter.AddInputConnection(clipper_inside.GetOutputPort())
    append_protrusion_filter.Update()
    protrusion_polydata=append_protrusion_filter.GetOutput()

    if write_output_protrusion_as_stl is True:
        protrusion_stlWriter = vtk.vtkSTLWriter()
        protrusion_stlWriter.SetFileName(cut_protrusion_fpath)
        protrusion_stlWriter.SetInputConnection(append_protrusion_filter.GetOutputPort())
        protrusion_stlWriter.Write()

    if write_output_cell_cut_as_stl is True:
        cut_cell_stlWriter = vtk.vtkSTLWriter()
        cut_cell_stlWriter.SetFileName(cut_cell_fpath)
        cut_cell_stlWriter.SetInputData(cell_polydata_list[largest_region_idx])
        cut_cell_stlWriter.Write()
    
    #get the inner cone
    implicitCell = vtk.vtkImplicitPolyDataDistance()
    implicitCell.SetInput(cell_polydata)
    
    subdivision_filter = vtk.vtkLinearSubdivisionFilter()
    subdivision_filter.SetNumberOfSubdivisions(3)
    subdivision_filter.SetInputData(cone_polydata)
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
    if verbose:
        print("num of regions", n)
    con_cone.SetExtractionModeToLargestRegion()
    con_cone.Update()
    
    append_all_filter = vtk.vtkAppendPolyData()
    append_all_filter.AddInputConnection(append_protrusion_filter.GetOutputPort())
    append_all_filter.AddInputConnection(con_cone.GetOutputPort())
    append_all_filter.Update()
    cone_protrusion_polydata=append_all_filter.GetOutput()

    if write_output_cone_protrusion_as_stl is True:
        cone_protrusion_stlWriter = vtk.vtkSTLWriter()
        cone_protrusion_stlWriter.SetFileName(cone_protrusion_fpath)
        cone_protrusion_stlWriter.SetInputConnection(append_all_filter.GetOutputPort())
        cone_protrusion_stlWriter.Write()

    # make return values
    results={}
    results.update({'protrusion polydata':protrusion_polydata})
    results.update({'cut cell polydata':cut_cell_polydata})
    results.update({'cone protrusion polydata':cone_protrusion_polydata})
    return results


def calc_morphometrics(fpath, verbose=True, returnfmt='list'):
    reader = vtk.vtkSTLReader()
    reader.SetFileName(fpath)
    reader.Update()

    properties = vtk.vtkMassProperties()
    properties.SetInputConnection(reader.GetOutputPort())
    surface_area = properties.GetSurfaceArea()
    volume = properties.GetVolume()
    if verbose:
        print("surface area", surface_area)
        print("volume", volume)

    ratio = surface_area / volume
    if verbose:
        print("ratio", ratio)

    # pca = vtk.vtkPCAAnalysisFilter()
    # pca.SetInputConnection(reader.GetOutputPort())
    # pca.Update()
    if returnfmt == 'list':
        if verbose:
            print('return format is list')
        result = [surface_area, volume]

    if returnfmt == 'dict':
        if verbose:
            print('return format is dict')
        result = {}
        result.update({'surface area': surface_area})
        result.update({'volume': volume})

    return result


def get_center_of_mass(polydata, verbose=True):
    """
    calculate the center of mass of the polydata
    """
    centerOfMass = vtk.vtkCenterOfMass()
    centerOfMass.SetInputData(polydata)
    centerOfMass.SetUseScalarsAsWeights(False)
    centerOfMass.Update()
    cm = centerOfMass.GetCenter()
    if verbose:
        print('center of mass is ' + str(cm))
    return cm


def get_shifted_cell(cellpath, output='.', savestl=False):
    """
    shift the mass center of the cell to the origin of the coordinate system
    return shifted_cell as a polydata
    """
    # load the cell stl
    cell = vtk.vtkSTLReader()
    cell.SetFileName(cellpath)
    cell.Update()

    # get the center of mass of the cell
    cm = get_center_of_mass(cell.GetOutput(), verbose=False)

    # define a translation transform
    tl = vtk.vtkTransform()
    shift = tuple(-np.asarray(list(cm)))  # shift the mass center to the origin
    tl.Translate(shift)

    # perfrom the translation on the polydata
    tf = vtk.vtkTransformFilter()
    tf.SetInputConnection(cell.GetOutputPort())
    tf.SetTransform(tl)
    tf.Update()

    shifted_cell = tf.GetOutput()

    if savestl:
        # Write the stl file to disk
        stlWriter = vtk.vtkSTLWriter()
        stlWriter.SetFileName(output)
        stlWriter.SetInputData(shifted_cell)
        stlWriter.Write()

    return shifted_cell


def stl2polydata(stlpath):
    stl = vtk.vtkSTLReader()
    stl.SetFileName(stlpath)
    stl.Update()
    polydata = stl.GetOutput()
    return polydata


def polydata2stl(polydata, stlpath):
    stlWriter = vtk.vtkSTLWriter()
    stlWriter.SetFileName(stlpath)
    stlWriter.SetInputData(polydata)
    stlWriter.Write()
    return 0


def getsv(polydata, getv=True, gets=True):
    """
    get surface area and volume of polydata

    """
    properties = vtk.vtkMassProperties()
    properties.SetInputData(polydata)
    result = {}
    if getv:
        volume = properties.GetVolume()
        result.update({'volume': volume})
    if gets:
        surface_area = properties.GetSurfaceArea()
        result.update({'surface area': surface_area})

    return result


def getroughness(s, v, f_norm=1):
    s=np.asarray(s)
    v=np.asarray(v)
    rv=(3*v/4/np.pi)**(1/3)
    rs=(s/4/np.pi)**(1/2)
    roughness=rv/rs*f_norm
    return roughness

def get_f_norm(apex):
    """
    get the normalization factor for roughness given an apex angle (unit=degree)

    :param a:  apex angle of a cone (unit=degree)
    :return: f_norm, the normalization factor
    """
    a=apex/180*np.pi
    # should include the derivation of this normalization factor to SI of the paper.
    f_norm=(4/(2-np.cos(a/2)**3))**(1/3) * ((2)/(np.sin(a/2)))**(-1/2)
    return f_norm

def get_pos_neg_vcenters(v, cone_vectors, normalize_v=False):
    """
    Perform noise filtering on a image stack along the time axis for each 
    pixel independently.

    Parameters
    ----------
    v : list
        a list of volumes for each cone cut volumes
    cone_vectors : list
        a list of volumes for each cone vectors
    normalize_v : bool
        whether to normalize the v or not

    Returns
    -------
    posc:  [type]
        description
    posstd:  [type]
        description 
    dvpos:  [type]
        description 
    negc:  [type]
        description 
    negstd:  [type]
        description 
    dvneg:  [type]
        description 
    polarity_vector:  [type]
        description
    """

    xs=cone_vectors[0]
    ys=cone_vectors[1]
    zs=cone_vectors[2]
    dv = v-np.average(v.ravel())
    if normalize_v is True:
        dv=dv/np.average(v.ravel())

    dvpos=np.zeros(dv.shape)
    dvpos[dv>0]=dv[dv>0]
    dvneg=np.zeros(dv.shape)
    dvneg[dv<0]=-dv[dv<0]
    
    
    posc=np.asarray([np.mean(dvpos*xs), np.mean(dvpos*ys), np.mean(dvpos*zs)]) # volume center of positive delta volumes

    negc=np.asarray([np.mean(dvneg*xs), np.mean(dvneg*ys), np.mean(dvneg*zs)]) # volume center of negative delta volumes
    
    posstd=np.asarray([np.std(dvpos[dvpos>0]*xs[dvpos>0]),
                     np.std(dvpos[dvpos>0]*ys[dvpos>0]),
                     np.std(dvpos[dvpos>0]*zs[dvpos>0])])

    negstd=np.asarray([np.std(dvneg[dvneg>0]*xs[dvneg>0]),
                     np.std(dvneg[dvneg>0]*ys[dvneg>0]),
                     np.std(dvneg[dvneg>0]*zs[dvneg>0])])

    polarity_vector=posc-negc
    return [posc, posstd, dvpos, negc, negstd, dvneg, polarity_vector]

def mark_local_extrema(roughnesses=[], cone_vectors=[],neighbour_n=8):
    maximatags = []
    minimatags = []
    for vind  in np.arange(len(cone_vectors.T)): # cone vector index
        dis = np.linalg.norm(cone_vectors.T - cone_vectors.T[vind],axis = 1)
        nearest_inds = np.argsort(dis)[1:neighbour_n+1]
        nearest_roughnesses = roughnesses[nearest_inds]
        rself = roughnesses[vind]
        maxima = 1 # 1 means maxima, 0 means minima
        minima = 1 # 1 means maxima, 0 means minima
        for r in nearest_roughnesses:
            if rself < r:
                maxima = 0
            if rself > r:
                minima = 0
        maximatags.append(maxima)
        minimatags.append(minima)
        
    return maximatags, minimatags

def mark_local_extrema_on_maps(cone_vectors, thetalist, philist, roughnesses=[], roumap=[], neighbour_n=8):  
    maximatags, minimatags = mark_local_extrema(roughnesses=roughnesses, 
                                                cone_vectors=cone_vectors, 
                                                neighbour_n=neighbour_n)
    maximainds=np.argsort(maximatags)[-np.sum(maximatags):]
    minimainds=np.argsort(minimatags)[-np.sum(minimatags):]
    from matplotlib import pyplot as plt
    maximathes = np.asarray(thetalist)[maximainds]
    maximaphis = np.asarray(philist)[maximainds]
    plt.figure(figsize=(10,10))
    plt.imshow(roumap)
    for i in np.arange(len(maximathes)):
        plt.plot(maximaphis[i],maximathes[i],'ro')
    
    
    minimathes = np.asarray(thetalist)[minimainds]
    minimaphis = np.asarray(philist)[minimainds]
    for i in np.arange(len(minimathes)):
        plt.plot(minimaphis[i],minimathes[i],'ro',markerfacecolor='w')

    maximavalues = np.asarray(roughnesses)[maximainds]
    minimavalues = np.asarray(roughnesses)[minimainds]
    plt.xlim(0,360)
    plt.ylim(0,180)

    return maximavalues, maximatags, maximainds, maximathes, maximaphis, minimavalues, minimatags, minimainds, minimathes, minimaphis
    
    
