"""Validation utilities for inputs."""
import numpy as np


def validate_image(img):
    """
    Validate image array.
    
    Args:
        img: numpy array
        
    Returns:
        bool: True if valid
    """
    if not isinstance(img, np.ndarray):
        return False
    
    if len(img.shape) not in [2, 3]:
        return False
    
    if img.dtype not in [np.uint8, np.uint16, np.float32, np.float64]:
        return False
    
    return True


def validate_dimensions(width, height, min_size=1, max_size=10000):
    """
    Validate image dimensions.
    
    Args:
        width: int
        height: int
        min_size: int
        max_size: int
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        w = int(width)
        h = int(height)
    except (ValueError, TypeError):
        return False, 'Dimensions must be numbers'
    
    if w < min_size or h < min_size:
        return False, f'Dimensions must be >= {min_size}'
    
    if w > max_size or h > max_size:
        return False, f'Dimensions must be <= {max_size}'
    
    return True, 'Valid'


def validate_components(n_components, max_components):
    """
    Validate PCA components.
    
    Args:
        n_components: int
        max_components: int
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        n = int(n_components)
    except (ValueError, TypeError):
        return False, 'Components must be a number'
    
    if n <= 0:
        return False, 'Components must be positive'
    
    if n > max_components:
        return False, f'Components cannot exceed {max_components}'
    
    return True, 'Valid'
