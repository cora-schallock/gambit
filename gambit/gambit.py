import numpy as np

def normalize_array(data,to_norm_mask):
    normalized = np.zeros(data.shape)
    the_min = np.min(data[to_norm_mask]); the_max = np.max(data[to_norm_mask])
    normalized[to_norm_mask] = (data[to_norm_mask]- the_min)/(the_max-the_min)
    return normalized

def create_diff_image(first_band_data,base_band_data,base_band_mask):
    first_norm = normalize_array(first_band_data,base_band_mask)
    base_norm = normalize_array(base_band_data,base_band_mask)
    return first_norm-base_norm
