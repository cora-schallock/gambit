import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#from gambit import create_masks_for_pair

PANSTARRS_COLOR_DICT = {'g':'green',
                        'r':'red',
                        'i':'indigo',
                        'z':'blue',
                        'y':'orange'}

DEFAULT_POSITIVE_RGB_VECTOR = [60/255,179/255,113/255] #mediumseagreen
DEFAULT_NEGATIVE_RGB_VECTOR = [240/255,128/255,125/255] #lightcoral
DEFAULT_BAD_PIXEL_RGB_VECTOR = [169/255,169/255,169/255] #lightgrey

def create_color_map_class(pos,neg,valid_pixels):
    cmap_class = np.zeros((pos.shape[0],pos.shape[1],3))
    
    cmap_class[pos>=1.0] = DEFAULT_POSITIVE_RGB_VECTOR
    cmap_class[neg>=1.0] = DEFAULT_NEGATIVE_RGB_VECTOR
    cmap_class[valid_pixels<1.0] = DEFAULT_BAD_PIXEL_RGB_VECTOR
    
    return cmap_class

def make_cmap_class_for_bands(the_gal,valid_pixel_mask_dict,xs_keys):
    cmaps_class_for_bands = dict()
    
    for the_band in xs_keys: #used to be the_gal.bands
        first_band = the_band.strip().split("-")[1]
        base_band = the_band.strip().split("-")[1]
        ref_band = the_gal.get_ref_band(first_band,base_band)
        #ref_band = base_band
        
        
        cmap_class = create_color_map_class(the_gal[ref_band].pos_mask,the_gal[ref_band].neg_mask,valid_pixel_mask_dict[the_band])
        cmaps_class_for_bands[the_band] = cmap_class
    return cmaps_class_for_bands

def construct_diff_plot(xs,diff_dict,ax_diff=None):
    legend_colors = []
    legend_labels = []
    
    if isinstance(ax_diff,type(None)):
        fig, ax_combined = plt.subplots(figsize = (12,8))
    else:
        ax_combined = ax_diff
    
    #Step 1) Plot difference vs. percentil graph for each band
    for band in diff_dict:
        print(band)
        first_band = band.strip().split("-")[0]
        base_band = band.strip().split("-")[1]
        
        ax_combined.plot(xs,diff_dict[band], linestyle=(0, (5, 5)), 
                         color=PANSTARRS_COLOR_DICT[first_band])
        ax_combined.plot(xs,diff_dict[band], linestyle=(5, (5, 5)), 
                         color=PANSTARRS_COLOR_DICT[base_band])
        
        m1, = ax_combined.plot([], [], c=PANSTARRS_COLOR_DICT[first_band], 
                               marker='s', markersize=20, fillstyle='left', linestyle='none')
        m2, = ax_combined.plot([], [], color=PANSTARRS_COLOR_DICT[base_band], 
                               marker='s', markersize=20, fillstyle='right', linestyle='none')
        legend_colors.append((m1,m2))
        legend_labels.append(band)
        #using: https://stackoverflow.com/questions/31908982/python-matplotlib-multi-color-legend-entry
        #different implementation of mutliple color line: https://stackoverflow.com/questions/59130371/can-the-off-color-be-set-for-a-matplotlib-dashed-line
   
    #Step 2) If applicable, plot verticle line (indicating current percentile threshold)
    #if diff_line != -1:
    #    ax_combined.axvline(diff_line)
    
    #Step 3) Add labels and legend
    ax_combined.set_xlabel('percentile')
    ax_combined.set_ylabel('threshold diff.')
    ax_combined.legend(tuple(legend_colors), tuple(legend_labels), 
                       numpoints=1, labelspacing=2, loc="lower left") #, fontsize=16
    #https://stackoverflow.com/questions/31908982/python-matplotlib-multi-color-legend-entry
    if isinstance(ax_diff,type(None)):
        plt.show()
    
def visualize_gambit_sersic(the_gal,xs,diff_dict,dark_side='',save_path='',bisection_theta=0):
    gs_kw = dict(width_ratios=[1,1,1], height_ratios=[1, 1, 2])
    #(30,40)
    fig, axd = plt.subplot_mosaic([['color','g','r'],
                                   ['i','z','y'],
                                   ['diff','diff','diff']],
                                  gridspec_kw=gs_kw, figsize = (24,32),
                                  constrained_layout=True,num=1, clear=True) #num=1, clear=True #https://stackoverflow.com/a/65910539/13544635
    fig.patch.set_facecolor('white')
    
    #add color:
    color_image = mpimg.imread(the_gal.color_image_path)
    axd['color'].imshow(color_image)
    axd['color'].set_title("{}: dark side {}".format(the_gal.name,dark_side))
    
    for band in the_gal.bands:
        ref_band, el_mask, pos_mask, neg_mask, valid_pixels = create_masks_for_pair(the_gal,band,band,bisection_theta=bisection_theta)
        valid_mask = np.logical_and(el_mask,valid_pixels)
        pos_valid_mask = np.logical_and(pos_mask,valid_mask)
        neg_valid_mask = np.logical_and(neg_mask,valid_mask)
        cmap = create_color_map_class(pos_valid_mask, neg_valid_mask, valid_mask)
        
        data = the_gal[band].data
        m, s = np.mean(data), np.std(data)
        axd[band].imshow(data, interpolation='nearest', cmap='gray', vmin=m-3*s, vmax=m+3*s, origin='lower') #, cmap='gray'
        axd[band].imshow(cmap, origin= 'lower',alpha=0.4)
        
        band_title = "{}:({:.2f},{:.2f}) a={:.2f}, b={:.2f}, θ={:.2f}".format(band,the_gal[band].x,
                                                                          the_gal[band].y,the_gal[band].a,
                                                                          the_gal[band].b,np.degrees(the_gal[band].theta))
        axd[band].set_title(band_title, color=PANSTARRS_COLOR_DICT[band])
    
    construct_diff_plot(xs,diff_dict,axd['diff'])
    if save_path != "":
        fig.savefig(save_path, dpi = 300, bbox_inches='tight')
    else:
        plt.show()
    #fig.close()
    #plt.close('all') #possible memory leak
    #also possibly relevent: https://stackoverflow.com/a/7101477/13544635
