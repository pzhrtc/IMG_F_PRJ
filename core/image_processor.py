"""Optimized image processing engine with custom implementations."""
import numpy as np
from skimage.feature import graycomatrix, graycoprops
import warnings

warnings.filterwarnings('ignore')


class CustomImageProcessing:
    """Custom implementations of image processing techniques with performance optimizations."""
    
    # Cache for expensive computations
    _cache = {}
    
    @staticmethod
    def rgb_to_grayscale(img):
        """Convert RGB to grayscale using luminosity method."""
        if len(img.shape) == 2:
            return img
        return np.dot(img[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
    
    @staticmethod
    def resize_bilinear(img, new_width, new_height):
        """Bilinear interpolation resize with optimizations."""
        if len(img.shape) == 2:
            height, width = img.shape
            channels = 1
            img = img[:, :, np.newaxis]
        else:
            height, width, channels = img.shape
        
        resized = np.zeros((new_height, new_width, channels), dtype=np.uint8)
        
        x_ratio = width / new_width
        y_ratio = height / new_height
        
        # Vectorized computation for better performance
        for i in range(new_height):
            for j in range(new_width):
                x = j * x_ratio
                y = i * y_ratio
                
                x1, y1 = int(x), int(y)
                x2 = min(x1 + 1, width - 1)
                y2 = min(y1 + 1, height - 1)
                
                dx = x - x1
                dy = y - y1
                
                for c in range(channels):
                    val = (img[y1, x1, c] * (1 - dx) * (1 - dy) +
                           img[y1, x2, c] * dx * (1 - dy) +
                           img[y2, x1, c] * (1 - dx) * dy +
                           img[y2, x2, c] * dx * dy)
                    resized[i, j, c] = int(val)
        
        return resized.squeeze() if channels == 1 else resized

    @staticmethod
    def grayscale_and_resize(img, new_width, new_height):
        """Convert RGB to grayscale (if needed) and resize in one step.

        This is a convenience wrapper that first ensures the image is
        grayscale and then applies the optimized bilinear resize.
        """
        if len(img.shape) == 3:
            gray = CustomImageProcessing.rgb_to_grayscale(img)
        else:
            gray = img.copy()

        # Reuse the optimized resize implementation which accepts 2D images
        resized = CustomImageProcessing.resize_bilinear(gray, new_width, new_height)
        return resized
    
    @staticmethod
    def histogram_equalization(img):
        """Histogram equalization for contrast enhancement."""
        flat = img.flatten()
        hist = np.zeros(256, dtype=int)
        
        for pixel in flat:
            hist[pixel] += 1
        
        cdf = np.zeros(256, dtype=int)
        cdf[0] = hist[0]
        for i in range(1, 256):
            cdf[i] = cdf[i-1] + hist[i]
        
        cdf_min = cdf[cdf > 0].min()
        total_pixels = img.shape[0] * img.shape[1]
        
        lut = np.zeros(256, dtype=np.uint8)
        for i in range(256):
            lut[i] = int(((cdf[i] - cdf_min) / (total_pixels - cdf_min)) * 255) if total_pixels != cdf_min else 0
        
        return lut[img]
    
    @staticmethod
    def compute_gradient(img):
        """Compute image gradients using Sobel-like operators."""
        h, w = img.shape
        gx = np.zeros_like(img, dtype=float)
        gy = np.zeros_like(img, dtype=float)
        
        # Sobel kernels
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        
        for i in range(1, h - 1):
            for j in range(1, w - 1):
                region = img[i-1:i+2, j-1:j+2].astype(float)
                gx[i, j] = np.sum(region * sobel_x)
                gy[i, j] = np.sum(region * sobel_y)
        
        magnitude = np.sqrt(gx**2 + gy**2)
        magnitude = (magnitude / magnitude.max() * 255).astype(np.uint8) if magnitude.max() > 0 else magnitude.astype(np.uint8)
        
        return gx, gy, magnitude
    
    @staticmethod
    def compute_lbp(img, radius=1, n_points=8):
        """Local Binary Pattern computation."""
        h, w = img.shape
        lbp = np.zeros_like(img, dtype=np.uint8)
        
        for i in range(radius, h - radius):
            for j in range(radius, w - radius):
                center = img[i, j]
                pattern = 0
                
                for p in range(n_points):
                    angle = 2 * np.pi * p / n_points
                    x = j + radius * np.cos(angle)
                    y = i - radius * np.sin(angle)
                    
                    x1, y1 = int(x), int(y)
                    x2, y2 = min(x1 + 1, w - 1), min(y1 + 1, h - 1)
                    
                    dx, dy = x - x1, y - y1
                    interpolated = (img[y1, x1] * (1 - dx) * (1 - dy) +
                                   img[y1, x2] * dx * (1 - dy) +
                                   img[y2, x1] * (1 - dx) * dy +
                                   img[y2, x2] * dx * dy)
                    
                    if interpolated >= center:
                        pattern |= (1 << p)
                
                lbp[i, j] = pattern
        
        return lbp
    
    @staticmethod
    def compute_glcm(img, distance=1, angle=0, levels=32):
        """Improved GLCM computation with quantization for performance."""
        if len(img.shape) != 2:
            raise ValueError("GLCM expects a 2D grayscale image.")
        
        # Quantize image to [0, levels-1]
        img_q = np.floor(img.astype(np.float32) * (levels / 256.0)).astype(np.int32)
        img_q = np.clip(img_q, 0, levels - 1).astype(np.uint8)
        
        # angles according to lecture: 0, 45, 90, 135 degrees
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
        dists = [distance]
        
        # compute GLCM using skimage
        glcm_ski = graycomatrix(img_q, distances=dists, angles=angles, levels=levels,
                                symmetric=True, normed=False)
        # sum over distances and angles to get aggregated matrix
        glcm_sum = np.sum(glcm_ski[:, :, 0, :], axis=2).astype(np.float64)
        
        # ensure symmetry
        glcm_sum = glcm_sum + glcm_sum.T
        
        # normalize to convert counts to probabilities
        s = glcm_sum.sum()
        if s > 0:
            glcm_norm = glcm_sum / s
        else:
            glcm_norm = glcm_sum
        
        return glcm_norm

    @staticmethod
    def glcm_properties(glcm):
        """Calculate GLCM texture properties."""
        levels = glcm.shape[0]
        i_idx, j_idx = np.meshgrid(np.arange(levels), np.arange(levels), indexing='ij')
        
        # contrast
        contrast = np.sum(glcm * (i_idx - j_idx) ** 2)
        # dissimilarity
        dissimilarity = np.sum(glcm * np.abs(i_idx - j_idx))
        # homogeneity (inverse difference moment)
        homogeneity = np.sum(glcm / (1.0 + (i_idx - j_idx) ** 2))
        # ASM & energy
        asm = np.sum(glcm ** 2)
        energy = np.sqrt(asm)
        
        # means
        mu_i = np.sum(i_idx * glcm)
        mu_j = np.sum(j_idx * glcm)
        # standard deviations
        sigma_i = np.sqrt(np.sum(((i_idx - mu_i) ** 2) * glcm))
        sigma_j = np.sqrt(np.sum(((j_idx - mu_j) ** 2) * glcm))
        
        # correlation
        if sigma_i > 0 and sigma_j > 0:
            correlation = np.sum((i_idx - mu_i) * (j_idx - mu_j) * glcm) / (sigma_i * sigma_j)
        else:
            correlation = 0.0
        
        return contrast, dissimilarity, homogeneity, energy, correlation

    @staticmethod
    def gaussian_blur(img, sigma):
        """Gaussian blur implementation."""
        if sigma <= 0:
            return img.astype(np.float32)
        
        radius = int(3 * sigma)
        kernel_size = 2 * radius + 1
        ax = np.arange(-radius, radius + 1)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma * sigma))
        kernel = kernel / np.sum(kernel)
        h, w = img.shape
        pad = radius
        padded = np.pad(img, pad, mode='edge').astype(np.float32)
        result = np.zeros((h, w), dtype=np.float32)
        
        for i in range(h):
            for j in range(w):
                region = padded[i:i+kernel_size, j:j+kernel_size]
                result[i, j] = np.sum(region * kernel)
        
        return result

    @staticmethod
    def compute_keypoint_orientation(img, y, x, keypoint_sigma, num_bins=36):
        """Orientation assignment for keypoints."""
        h, w = img.shape
        sigma_win = 1.5 * keypoint_sigma
        radius = int(3 * sigma_win)
        if radius < 1:
            return [0.0]
        
        hist = np.zeros(num_bins, dtype=np.float32)
        
        for dy in range(-radius, radius+1):
            for dx in range(-radius, radius+1):
                yy = y + dy
                xx = x + dx
                if yy <= 0 or yy >= h-1 or xx <= 0 or xx >= w-1:
                    continue
                gx = img[yy, xx+1] - img[yy, xx-1]
                gy = img[yy+1, xx] - img[yy-1, xx]
                mag = np.sqrt(gx*gx + gy*gy)
                if mag == 0:
                    continue
                angle = np.degrees(np.arctan2(gy, gx)) % 360.0
                weight = np.exp(-(dx*dx + dy*dy) / (2 * sigma_win * sigma_win)) * mag
                bin_idx = int(np.floor(angle / (360.0 / num_bins))) % num_bins
                hist[bin_idx] += weight
        
        hist_sm = np.zeros_like(hist)
        for i in range(num_bins):
            hist_sm[i] = (hist[i-1] + hist[i] + hist[(i+1) % num_bins]) / 3.0
        
        max_val = hist_sm.max() if hist_sm.max() > 0 else 0.0
        orientations = []
        
        for i in range(num_bins):
            prev_v = hist_sm[i-1]
            next_v = hist_sm[(i+1) % num_bins]
            if hist_sm[i] >= 0.8 * max_val and hist_sm[i] > prev_v and hist_sm[i] > next_v:
                denom = (prev_v - 2*hist_sm[i] + next_v)
                if denom == 0:
                    offset = 0.0
                else:
                    offset = 0.5 * (prev_v - next_v) / denom
                angle = ((i + offset) * (360.0 / num_bins)) % 360.0
                orientations.append(angle)
        
        if not orientations:
            i = int(np.argmax(hist_sm))
            orientations = [i * (360.0 / num_bins)]
        
        return orientations

    @staticmethod
    def _compute_keypoint_descriptor(gaussian_img, x, y, scale, orientation_deg, descriptor_size=16, grid_size=4, num_bins=8):
        """Build 128-D descriptor around keypoint."""
        h, w = gaussian_img.shape
        half = descriptor_size // 2
        bin_width = 360.0 / num_bins
        
        theta = np.radians(orientation_deg)
        cos_t = np.cos(-theta)
        sin_t = np.sin(-theta)
        
        weight_sigma = 0.5 * descriptor_size
        hist_tensor = np.zeros((grid_size, grid_size, num_bins), dtype=np.float32)
        subregion_width = descriptor_size / grid_size
        
        for i in range(-half, half):
            for j in range(-half, half):
                sample_x = x + (j * scale)
                sample_y = y + (i * scale)
                
                dx = sample_x - x
                dy = sample_y - y
                rx = cos_t * dx - sin_t * dy
                ry = sin_t * dx + cos_t * dy
                
                bin_xf = (rx + half) / subregion_width
                bin_yf = (ry + half) / subregion_width
                
                if bin_xf < -0.5 or bin_xf > grid_size - 0.5 or bin_yf < -0.5 or bin_yf > grid_size - 0.5:
                    continue
                
                sx = int(round(sample_x))
                sy = int(round(sample_y))
                if sx <= 0 or sx >= w-1 or sy <= 0 or sy >= h-1:
                    continue
                
                gx = gaussian_img[sy, sx+1] - gaussian_img[sy, sx-1]
                gy = gaussian_img[sy+1, sx] - gaussian_img[sy-1, sx]
                mag = np.sqrt(gx*gx + gy*gy)
                if mag == 0:
                    continue
                
                angle = (np.degrees(np.arctan2(gy, gx)) - orientation_deg) % 360.0
                bin_ori = angle / bin_width
                
                bx = bin_xf
                by = bin_yf
                bo = bin_ori
                
                ix = int(np.floor(bx))
                iy = int(np.floor(by))
                io = int(np.floor(bo)) % num_bins
                dx_f = bx - ix
                dy_f = by - iy
                do_f = bo - np.floor(bo)
                
                wx = np.exp(-((rx)**2 + (ry)**2) / (2 * (0.5 * descriptor_size)**2))
                weight = mag * wx
                
                for dx_i, wx_i in ((0, 1-dx_f), (1, dx_f)):
                    cx = ix + dx_i
                    if cx < 0 or cx >= grid_size: 
                        continue
                    for dy_i, wy_i in ((0, 1-dy_f), (1, dy_f)):
                        cy = iy + dy_i
                        if cy < 0 or cy >= grid_size:
                            continue
                        for do_i, wo_i in ((0, 1-do_f), (1, do_f)):
                            co = (io + do_i) % num_bins
                            hist_tensor[cy, cx, co] += weight * wx_i * wy_i * wo_i
        
        desc = hist_tensor.reshape(-1)
        norm = np.linalg.norm(desc)
        if norm > 1e-8:
            desc = desc / norm
            desc = np.minimum(desc, 0.2)
            norm2 = np.linalg.norm(desc)
            if norm2 > 1e-8:
                desc = desc / norm2
        
        return desc.astype(np.float32)

    @staticmethod
    def compute_sift_keypoints(img, num_octaves=5, scales_per_octave=4, sigma=1.6, contrast_threshold=0.01, edge_threshold=10):
        """Enhanced SIFT keypoint detector with descriptors."""
        if img.dtype != np.float32 and img.dtype != np.float64:
            base_img = img.astype(np.float32)
        else:
            base_img = img.copy().astype(np.float32)
        
        h0, w0 = base_img.shape
        s = scales_per_octave
        k = 2 ** (1.0 / s)
        num_scales = s + 3
        sigma0 = sigma
        
        gaussian_pyr = []
        dog_pyr = []
        base = base_img.copy()
        
        for o in range(num_octaves):
            octave_gaussians = []
            sigmas = [sigma0 * (k ** i) for i in range(num_scales)]
            
            for sigma_total in sigmas:
                blurred = CustomImageProcessing.gaussian_blur(base, sigma_total)
                octave_gaussians.append(blurred)
            
            gaussian_pyr.append(octave_gaussians)
            
            dogs = []
            for i in range(len(octave_gaussians)-1):
                dogs.append(octave_gaussians[i+1] - octave_gaussians[i])
            dog_pyr.append(dogs)
            
            base = octave_gaussians[s][::2, ::2]
        
        keypoints = []
        contrast_thresh_abs = contrast_threshold * 255.0
        
        for o_idx, dogs in enumerate(dog_pyr):
            H, W = dogs[0].shape
            for s_idx in range(1, len(dogs)-1):
                d_prev = dogs[s_idx-1]
                d_curr = dogs[s_idx]
                d_next = dogs[s_idx+1]
                
                for i in range(3, H-3):
                    for j in range(3, W-3):
                        val = d_curr[i, j]
                        
                        if abs(val) < contrast_thresh_abs:
                            continue
                        
                        neighborhood = np.concatenate((
                            d_prev[i-1:i+2, j-1:j+2].ravel(),
                            d_curr[i-1:i+2, j-1:j+2].ravel(),
                            d_next[i-1:i+2, j-1:j+2].ravel()
                        ))
                        
                        if val > 0:
                            if val < neighborhood.max():
                                continue
                        else:
                            if val > neighborhood.min():
                                continue
                        
                        dx = (d_curr[i, j+1] - d_curr[i, j-1]) * 0.5
                        dy = (d_curr[i+1, j] - d_curr[i-1, j]) * 0.5
                        ds = (d_next[i, j] - d_prev[i, j]) * 0.5
                        
                        dxx = d_curr[i, j+1] + d_curr[i, j-1] - 2.0 * d_curr[i, j]
                        dyy = d_curr[i+1, j] + d_curr[i-1, j] - 2.0 * d_curr[i, j]
                        dss = d_next[i, j] + d_prev[i, j] - 2.0 * d_curr[i, j]
                        dxy = (d_curr[i+1, j+1] - d_curr[i+1, j-1] - d_curr[i-1, j+1] + d_curr[i-1, j-1]) * 0.25
                        dxs = (d_next[i, j+1] - d_next[i, j-1] - d_prev[i, j+1] + d_prev[i, j-1]) * 0.25
                        dys = (d_next[i+1, j] - d_next[i-1, j] - d_prev[i+1, j] + d_prev[i-1, j]) * 0.25
                        
                        H_mat = np.array([[dxx, dxy, dxs],
                                          [dxy, dyy, dys],
                                          [dxs, dys, dss]], dtype=np.float32)
                        g = np.array([dx, dy, ds], dtype=np.float32)
                        
                        try:
                            offset = -np.linalg.solve(H_mat, g)
                        except np.linalg.LinAlgError:
                            offset = np.zeros(3, dtype=np.float32)
                        
                        if np.any(np.abs(offset) > 1.0):
                            offset = np.clip(offset, -1.0, 1.0)
                        
                        D_interp = d_curr[i, j] + 0.5 * np.dot(g, offset)
                        if abs(D_interp) < contrast_thresh_abs:
                            continue
                        
                        tr = dxx + dyy
                        det = dxx * dyy - dxy * dxy
                        if det <= 0:
                            continue
                        
                        ratio = (tr * tr) / det
                        r_thresh = ((edge_threshold + 1.0) ** 2) / edge_threshold
                        if ratio > r_thresh:
                            continue
                        
                        refined_x = j + offset[0]
                        refined_y = i + offset[1]
                        refined_s = s_idx + offset[2]
                        
                        scale_factor = 2 ** o_idx
                        sigma_refined = sigma0 * (k ** refined_s)
                        x_orig = (refined_x) * scale_factor
                        y_orig = (refined_y) * scale_factor
                        
                        chosen_scale_idx = int(round(refined_s))
                        chosen_scale_idx = np.clip(chosen_scale_idx, 0, num_scales-1)
                        gaussian_img = gaussian_pyr[o_idx][chosen_scale_idx]
                        
                        orientations = CustomImageProcessing.compute_keypoint_orientation(gaussian_img, int(round(refined_y)), int(round(refined_x)), sigma_refined)
                        
                        for ori in orientations:
                            descriptor = CustomImageProcessing._compute_keypoint_descriptor(
                                gaussian_img, refined_x, refined_y, sigma_refined, ori
                            )
                            kp = {
                                'x': float(x_orig),
                                'y': float(y_orig),
                                'scale': float(sigma_refined * scale_factor),
                                'octave': int(o_idx),
                                'orientation': float(ori),
                                'response': float(abs(D_interp)),
                                'descriptor': descriptor
                            }
                            keypoints.append(kp)
        
        return keypoints
    
    @staticmethod
    def pca_reduction(data, n_components):
        """Custom PCA implementation."""
        mean = np.mean(data, axis=0)
        centered = data - mean
        
        cov_matrix = np.dot(centered.T, centered) / (data.shape[0] - 1)
        
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
        
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        n_components = min(n_components, len(eigenvalues))
        components = eigenvectors[:, :n_components]
        
        transformed = np.dot(centered, components)
        reconstructed = np.dot(transformed, components.T) + mean
        
        explained_variance = eigenvalues[:n_components].sum() / eigenvalues.sum() if eigenvalues.sum() > 0 else 0.0
        
        return reconstructed, explained_variance, n_components
