# Quick Start Guide

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Application
```bash
python main.py
```

## First Time Use

### Step 1: Import an Image
- Click the **📁 Import** button in the header
- Select an image file (PNG, JPG, BMP, TIFF)
- The image appears in the original image panel

### Step 2: Preprocess (Optional but Recommended)
Go to the **Processing** tab:
- **Grayscale**: Convert to grayscale for texture analysis
- **Resize**: Enter width/height (e.g., 256x256) and click "Apply Resize"
- **Histogram Equalization**: Enhance contrast for better feature detection

### Step 3: Extract Features
Go to the **Features** tab:

1. **Select a technique**:
   - **SIFT**: Best for finding distinctive keypoints (detailed analysis)
   - **GLCM**: Best for texture properties (4 texture metrics)
   - **LBP**: Best for texture patterns (fast)
   - **Sobel**: Best for edge detection

2. Click **Extract Features**
3. View results in the table on the right

### Step 4: Reduce Dimensions (Optional)
Still in **Features** tab:

1. Enter number of PCA components (e.g., 50)
2. Click **Apply PCA Reduction**
3. View the reduced feature image in the **Analysis** tab

### Step 5: Export Results
Click **Save Feature Image** or **Save Reduced Image** to export

## Tips for Best Results

### For Face Detection
1. Import face image
2. Convert to grayscale
3. Use SIFT (will detect facial features)

### For Texture Analysis
1. Crop a texture region
2. Resize to 256×256
3. Use GLCM or LBP

### For Edge Detection
1. Preprocess the image
2. Use Sobel
3. Save the edge map

### For Quick Processing
1. Reduce image size first (256×256)
2. Use LBP instead of SIFT
3. Adjust PCA components as needed

## Understanding the Results

### SIFT Results
- **Keypoints Found**: Number of detected features
- Each keypoint has: position (x,y), scale, orientation

### GLCM Results
- **Contrast**: Measure of local variations
- **Dissimilarity**: Similar to contrast
- **Homogeneity**: Measures closeness of distribution
- **Energy**: Measure of uniformity
- **Correlation**: Measure of linear dependency

### LBP Results
- **Patterns Found**: Number of texture patterns detected

### Sobel Results
- **Edges Found**: Number of edge pixels detected
- Image shows edge magnitude (darker = stronger edge)

## Performance Settings

### For Speed (Large Images)
```
- Resize to 128×128 or 256×256
- Use LBP or Sobel
- Set PCA components to 10-20
```

### For Accuracy (Better Features)
```
- Keep original resolution
- Use SIFT or GLCM
- Set PCA components to 50+
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| App slow | Reduce image size |
| Out of memory | Use smaller images |
| Keypoints not found | Try GLCM or LBP instead |
| Blurry results | Check image quality |

## Keyboard Shortcuts

- Currently uses GUI buttons (no keyboard shortcuts in this version)

## File Menu Operations

- **Import**: Open an image file
- **Reset**: Clear all data and start over
- **Save**: Export processed images

## Next Steps

1. Experiment with different feature extraction methods
2. Try different image types (photos, documents, textures)
3. Compare results between techniques
4. Use for forensic analysis, image comparison, authentication

Enjoy exploring image forensics! 🔍
