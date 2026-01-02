"""Helper functions for image processing and visualization."""
import numpy as np


def draw_keypoints(img, keypoints):
    """
    Draw keypoints on image.
    
    Args:
        img: numpy array (RGB or grayscale)
        keypoints: list of keypoint dicts with 'x', 'y', 'scale', 'orientation'
        
    Returns:
        numpy array: image with keypoints drawn
    """
    result = img.copy()
    if len(result.shape) == 2:
        result = np.stack([result, result, result], axis=-1)
    
    for kp in keypoints:
        x = int(round(kp['x']))
        y = int(round(kp['y']))
        scale = kp['scale']
        orientation = kp['orientation']
        
        if 0 <= y < result.shape[0] and 0 <= x < result.shape[1]:
            # Draw circle
            radius = max(2, int(scale * 0.5))
            for i in range(-radius, radius+1):
                for j in range(-radius, radius+1):
                    if i*i + j*j <= radius*radius:
                        ny, nx = y+i, x+j
                        if 0 <= ny < result.shape[0] and 0 <= nx < result.shape[1]:
                            result[ny, nx] = [0, 255, 0]  # Green
            
            # Draw orientation line
            angle_rad = np.radians(orientation)
            line_length = max(3, int(scale * 1.5))
            end_x = int(x + line_length * np.cos(angle_rad))
            end_y = int(y + line_length * np.sin(angle_rad))
            
            # Bresenham's line
            dx = abs(end_x - x)
            dy = abs(end_y - y)
            sx = 1 if x < end_x else -1
            sy = 1 if y < end_y else -1
            err = dx - dy
            
            cx, cy = x, y
            while True:
                if 0 <= cy < result.shape[0] and 0 <= cx < result.shape[1]:
                    result[cy, cx] = [255, 0, 0]  # Red
                
                if cx == end_x and cy == end_y:
                    break
                
                e2 = 2 * err
                if e2 > -dy:
                    err -= dy
                    cx += sx
                if e2 < dx:
                    err += dx
                    cy += sy
    
    return result


def create_feature_overlay(img, feature_map, alpha=0.5):
    """
    Create overlay of feature map on image.
    
    Args:
        img: numpy array (grayscale)
        feature_map: numpy array (grayscale) with features highlighted
        alpha: float, transparency
        
    Returns:
        numpy array: overlayed image
    """
    # Normalize feature map
    if feature_map.max() > 0:
        feature_norm = (feature_map / feature_map.max() * 255).astype(np.uint8)
    else:
        feature_norm = feature_map.astype(np.uint8)
    
    # Create heatmap (red channel for features)
    heatmap = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    heatmap[:, :, 0] = feature_norm  # Red channel
    
    # Blend
    result = img.astype(float)
    result = np.stack([result, result, result], axis=-1)
    result = (result * (1 - alpha) + heatmap * alpha).astype(np.uint8)
    
    return result


def gaussian_heatmap(shape, center, sigma=20):
    """
    Create gaussian heatmap.
    
    Args:
        shape: tuple (height, width)
        center: tuple (y, x)
        sigma: float, standard deviation
        
    Returns:
        numpy array: heatmap
    """
    h, w = shape
    cy, cx = center
    
    y, x = np.ogrid[:h, :w]
    heatmap = np.exp(-((x - cx)**2 + (y - cy)**2) / (2 * sigma**2))
    
    return heatmap


def clip_value(value, min_val, max_val):
    """Clip value between min and max."""
    return max(min_val, min(value, max_val))


def scale_image_to_fit(img, max_width, max_height):
    """
    Scale image to fit within bounds while maintaining aspect ratio.
    
    Args:
        img: numpy array
        max_width: int
        max_height: int
        
    Returns:
        tuple: (scaled_image, scale_factor)
    """
    h, w = img.shape[:2]
    scale_w = max_width / w
    scale_h = max_height / h
    scale = min(scale_w, scale_h, 1.0)
    
    new_h = int(h * scale)
    new_w = int(w * scale)
    
    return img, scale
