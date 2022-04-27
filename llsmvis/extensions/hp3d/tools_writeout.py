import numpy as np
def polarity_vr_writeout(f, pc,pstd,pdv,nc,nstd,ndv,vol,polarity_vector,\
                         maximavalues, maximatags, maximainds, maximathes, maximaphis, \
                         minimavalues, minimatags, minimainds, minimathes, minimaphis ):

    try:
        del f['polarity based on volume - positive center']
    except:
        pass
    f.create_dataset("polarity based on volume - positive center", data=pc, dtype='float')
    
    try:
        del f['polarity based on volume - positive volume std']
    except:
        pass
    f.create_dataset("polarity based on volume - positive volume std", data=pstd, dtype='float')
    
    try:
        del f['polarity based on volume - positive delta volumes']
    except:
        pass
    f.create_dataset("polarity based on volume - positive delta volumes", data=pdv, dtype='float')
    
    try:
        del f['polarity based on volume - sum of positive delta volumes']
    except:
        pass
    f.create_dataset("polarity based on volume - sum of positive delta volumes", data=np.sum(pdv), dtype='float')
    
    try:
        del f['polarity based on volume - negative center']
    except:
        pass
    f.create_dataset("polarity based on volume - negative center", data=nc, dtype='float')
    
    try:
        del f['polarity based on volume - negative volume std']
    except:
        pass
    f.create_dataset("polarity based on volume - negative volume std", data=nstd, dtype='float')
    
    try:
        del f['polarity based on volume - negative delta volumes']
    except:
        pass
    f.create_dataset("polarity based on volume - negative delta volumes", data=ndv, dtype='float')
    
    try:
        del f['polarity based on volume - sum of negative delta volumes']
    except:
        pass
    f.create_dataset("polarity based on volume - sum of negative delta volumes", data=np.sum(ndv), dtype='float')
    
    try:
        del f['polarity based on volume - total volumes of all cones']
    except:
        pass
    f.create_dataset("polarity based on volume - total volumes of all cones", data=np.sum(vol), dtype='float')
    
    try:
        del f['polarity based on volume - polarity vector']
    except:
        pass
    f.create_dataset("polarity based on volume - polarity vector", data=polarity_vector, dtype='float')
    
    try:
        del f['polarity based on roughness - maxima values']
    except:
        pass
    f.create_dataset("polarity based on roughness - maxima values", data=maximavalues, dtype='float')
    
    try:
        del f['polarity based on roughness - maxima tags']
    except:
        pass
    f.create_dataset("polarity based on roughness - maxima tags", data=maximatags, dtype='float')
    
    try:
        del f['polarity based on roughness - maxima inds']
    except:
        pass
    f.create_dataset("polarity based on roughness - maxima inds", data=maximainds, dtype='float')

    try:
        del f['polarity based on roughness - maxima thetas']
    except:
        pass
    f.create_dataset("polarity based on roughness - maxima thetas", data=maximathes, dtype='float')
    
    try:
        del f['polarity based on roughness - maxima phis']
    except:
        pass
    f.create_dataset("polarity based on roughness - maxima phis", data=maximaphis, dtype='float')
    
    try:
        del f['polarity based on roughness - minima values']
    except:
        pass
    f.create_dataset("polarity based on roughness - minima values", data=minimavalues, dtype='float')
    
    try:
        del f['polarity based on roughness - minima tags']
    except:
        pass
    f.create_dataset("polarity based on roughness - minima tags", data=minimatags, dtype='float')
    
    try:
        del f['polarity based on roughness - minima inds']
    except:
        pass
    f.create_dataset("polarity based on roughness - minima inds", data=minimainds, dtype='float')

    try:
        del f['polarity based on roughness - minima thetas']
    except:
        pass
    f.create_dataset("polarity based on roughness - minima thetas", data=minimathes, dtype='float')
    
    try:
        del f['polarity based on roughness - minima phis']
    except:
        pass
    f.create_dataset("polarity based on roughness - minima phis", data=minimaphis, dtype='float')
    
