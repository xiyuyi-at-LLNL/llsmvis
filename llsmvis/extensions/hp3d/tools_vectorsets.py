import numpy as np

# define a set of tools
def sample_points_equal_spaced_logi_lati(longitude_n, latitude_n, output_angles=False):
    """
    create vectors sampled with equally spaced longitudes and latitudes.
    """
    logi = np.linspace(0, 360, longitude_n)*np.pi/180
    lati = np.linspace(0, 180, latitude_n)*np.pi/180
    pola = np.asarray(np.meshgrid(logi, lati))
    phis = pola[0]
    thes = pola[1]
    x = np.sin(thes) * np.cos(phis)
    y = np.sin(thes) * np.sin(phis)
    z = np.cos(thes)
    coordinates = np.asarray([x.ravel(), y.ravel(), z.ravel()])
    if output_angles is False:
        output = coordinates
    
    else: 
        output= [coordinates, pola[0], pola[1]]

    return output

def sample_points_semi_equal_space(t, output_angles=False):
    """
    generate an array of semi-equally spaced points on a 3D sphere
    t is the separation angle of 2 points  (degree)
    """
    # caldulate how many latitude circles should we have:
    N=np.int(180/t)
    # get the absolute theta for each latitude circle
    thetas=np.arange(0,N+1)*t
    # get the radius for each latitude circles
    Rs=np.sin(thetas/180*np.pi)
    # circumference of each latitude circle
    dr=np.sin(t/180*np.pi)
    # number of points along each latitude circle
    Np=np.round(Rs*2*np.pi/dr)
    Np[0]=1
    Np[-1]=1
    # loop over each circumferent, generate the location coordinates
    # for cn in np.arange(Np.size):
    xlist=[]
    ylist=[]
    zlist=[]
    thetalist=[]
    philist=[]
    for cn in np.arange(len(Np)):
        np2=Np[cn]
        dphi=360/np2
        phis=np.arange(0,np2)*dphi
        theta=thetas[cn]
        xs=np.sin(theta/180*np.pi)*np.cos(phis/180*np.pi)
        ys=np.sin(theta/180*np.pi)*np.sin(phis/180*np.pi)
        zs=np.cos(theta/180*np.pi)*np.ones(phis.size)
        xlist=xlist+list(xs)
        ylist=ylist+list(ys)
        zlist=zlist+list(zs)
        thetalist+=[theta]*len(phis)
        philist+=list(phis)
        
    x=np.asarray(xlist)
    y=np.asarray(ylist)
    z=np.asarray(zlist)
    if output_angles is False:
        return x, y, z
    else:
        return x, y, z, thetalist, philist