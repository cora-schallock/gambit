import numpy as np
from scipy import stats

def clean_data(data):
    data[np.isinf(data)] = 0
    data[np.isnan(data)] = 0
    return data

def percentile_array(data,mask=None):
    if not isinstance(mask,np.ndarray):
        mask = np.ones(data.shape)
    per = np.zeros(data.shape)
    per[mask] = stats.rankdata(data[mask], "average") / len(data[mask])
    
    return per

def create_diff_per_image(first_band_data,base_band_data,base_band_mask):
    first_per = percentile_array(first_band_data,base_band_mask)
    base_per = percentile_array(base_band_data,base_band_mask)
    return first_per-base_per

def normalize_array(data,to_norm_mask):
    """data - fits file (after read fits)
    to_norm_mask - a single boolean mask"""
    normalized = np.zeros(data.shape)
    the_min = np.min(data[to_norm_mask]); the_max = np.max(data[to_norm_mask])
    normalized[to_norm_mask] = (data[to_norm_mask]- the_min)/(the_max-the_min)
    return normalized

def create_diff_image(first_band_data,base_band_data,base_band_mask):
    first_norm = normalize_array(first_band_data,base_band_mask)
    base_norm = normalize_array(base_band_data,base_band_mask)
    return first_norm-base_norm
