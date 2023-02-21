import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

#fits: i/o:
def write_fits(path,data):
    """write fits file to path"""
    hdul = fits.PrimaryHDU(data)
    hdul.writeto(path)

def read_fits(path):
    """reads fits file specified by path"""
    hdul = fits.open(path)
    data = hdul[0].data
    return data

def view_fits(data,mask=None,std_range=None,cmap=None):
    """view fits files

    Args:
        data: the fits
        mask: a boolean mask where True means pixels is considered
        std_range: how many stds to visualize when viewing
        cmap: an additional color map to view ontop of fits
    """
    
    fig, ax = plt.subplots() #https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D
    vmin = None
    vmax = None

    if not isinstance(std_range,type(None)):
        if isinstance(mask,np.ndarray):
            m, s = np.mean(data[mask]), np.std(data[mask])
        else:
            m, s = np.mean(data), np.std(data)
        vmin = m-std_range*s
        vmax = m+std_range*s

    im = ax.imshow(data, interpolation='nearest', cmap='gray', vmin=vmin, vmax=vmax, origin='lower')
    if not isinstance(cmap,type(None)):
        ax.imshow(cmap, origin= 'lower',alpha=0.25)
    plt.show()
    
def view_fits_with_sep_objects(data,sep_objects,f=6):
    """view fits files with sep objects ontop"""
    
    fig, ax = plt.subplots() #https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D
    m, s = np.mean(data), np.std(data)
    im = ax.imshow(data, interpolation='nearest', cmap='gray',
                   vmin=m-s, vmax=m+s, origin='lower')
    
    NUM_COLORS = len(sep_objects)

    cm = plt.get_cmap('gist_rainbow')
    

    # plot an ellipse for each object
    for i in range(len(sep_objects)):
        x = sep_objects[i]['x']
        y = sep_objects[i]['y']
        a = sep_objects[i]['a']
        b = sep_objects[i]['b']
        theta = sep_objects[i]['theta']

        color = cm(1.*i/NUM_COLORS)
        e = Ellipse(xy=(x, y), width=f*a, height=f*b, angle=theta * 180. / np.pi)
        e.set_facecolor('none')
        e.set_edgecolor(color)
        ax.add_artist(e)
        
        
        xt = 0.5*f*a*np.cos(theta)
        yt = 0.5*f*a*np.sin(theta)
        plt.plot([x-xt,x+xt],[y-yt,y+yt],color=color,linestyle="--")
        

        xt = 0.5*f*b*np.cos(theta+np.pi/2)
        yt = 0.5*f*b*np.sin(theta+np.pi/2)
        plt.plot([x-xt,x+xt],[y-yt,y+yt],color=color,linestyle="--")
        
        plt.plot(sep_objects[i]['xcpeak'], sep_objects[i]['ycpeak'], marker='o', color=color)
        
    plt.xlim([0, data.shape[0]])
    plt.ylim([0, data.shape[0]])
    plt.show()
