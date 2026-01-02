# Image Forensics Analysis Tool

A modern, high-performance Python-based application for image forensics analysis with advanced feature extraction capabilities. Features a completely redesigned dark theme GUI with professional UI/UX.

## 🎨 What's New

### Complete GUI Redesign
- **Modern Dark Theme**: Professional cyan/magenta color scheme with smooth gradients
- **Tabbed Interface**: Organized processing, features, and analysis workflows
- **Real-time Feedback**: Progress indicators, status bar, and live updates
- **Enhanced UX**: Intuitive controls with hover effects and better visual hierarchy
- **Threading**: Background processing to keep UI responsive

### New Project Structure
```
proo/
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── core/                   # Image processing engine
│   ├── __init__.py
│   └── image_processor.py # All processing algorithms
├── gui/                    # User interface
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── styles.py          # Theme and styling definitions
│   └── widgets.py         # Custom styled widgets
└── utils/                  # Helper utilities
    ├── __init__.py
    ├── helpers.py         # Visualization and utility functions
    └── validators.py      # Input validation
```

### Performance Improvements
- **Vectorized Operations**: Optimized numpy usage for faster processing
- **Lazy Loading**: Images loaded on demand
- **Caching**: Expensive computations cached where possible
- **Threading**: Non-blocking UI with background processing threads
- **Efficient Memory**: Reduced memory footprint through smart array handling

## 🚀 Features

### Image Processing
- **Grayscale Conversion**: RGB to grayscale using luminosity method
- **Image Resizing**: Bilinear interpolation for smooth scaling
- **Histogram Equalization**: Contrast enhancement for better visualization
- **Gradient Computation**: Sobel operator for edge detection

### Feature Extraction
- **SIFT (Scale-Invariant Feature Transform)**
  - Keypoint detection with scale and orientation
  - 128-D descriptor generation
  - Visualization with circles and orientation lines

- **GLCM (Gray-Level Co-occurrence Matrix)**
  - Texture analysis with multiple properties
  - Contrast, dissimilarity, homogeneity, energy, correlation
  - Optimized quantization for performance

- **LBP (Local Binary Pattern)**
  - Texture pattern extraction
  - Efficient circular neighborhood sampling

- **Sobel Edge Detection**
  - Gradient-based edge detection
  - Real-time visualization

### Dimensionality Reduction
- **PCA (Principal Component Analysis)**
  - Configurable component count
  - Variance explained calculation
  - Feature space reduction with reconstruction

### Visualization
- **Real-time Image Display**: Side-by-side comparison
- **Feature Overlay**: Visual representation of detected features
- **Results Table**: Detailed analysis results in organized table format
- **Progress Indicators**: Visual feedback during processing

## 📋 Requirements

- **Python**: 3.8+
- **OS**: Windows, macOS, Linux

## 🔧 Installation

1. Clone or download the project

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 📦 Dependencies

- **numpy**: Numerical computations
- **PIL/Pillow**: Image I/O and manipulation
- **scikit-image**: Advanced image processing (GLCM, etc.)
- **scikit-learn**: Machine learning utilities
- **opencv-python**: Computer vision algorithms
- **scipy**: Scientific computing

## 🎯 Usage

### Basic Workflow

1. **Import Image**
   - Click "📁 Import" to load an image
   - Supported formats: PNG, JPG, JPEG, BMP, TIFF

2. **Preprocess** (Processing Tab)
   - Convert to grayscale
   - Resize to desired dimensions
   - Enhance contrast with histogram equalization

3. **Extract Features** (Features Tab)
   - Select a feature extraction technique
   - Choose from SIFT, GLCM, LBP, or Sobel
   - View results in the analysis panel

4. **Reduce Dimensions** (Features Tab)
   - Set desired PCA components
   - Apply reduction to extracted features
   - View variance explained

5. **Export Results**
   - Save feature images in PNG/JPEG format
   - Save reduced images for further analysis

## 🔍 Feature Details

### SIFT (Scale-Invariant Feature Transform)
- Multi-scale keypoint detection
- Gaussian pyramid with 5 octaves
- 4 scales per octave
- Taylor interpolation for subpixel localization
- 128-D descriptor per keypoint
- Orientation assignment with 36-bin histogram

### GLCM (Gray-Level Co-occurrence Matrix)
- Texture analysis across multiple directions
- 4-directional computation (0°, 45°, 90°, 135°)
- Quantization to 32 levels for efficiency
- Normalized probability matrix

### LBP (Local Binary Pattern)
- Circular neighborhood sampling
- 8-point pattern with radius 1
- Fast texture feature extraction

### Sobel
- 3×3 kernel-based gradient computation
- Magnitude and direction calculation
- Real-time edge visualization

## ⚡ Performance Tips

1. **Large Images**: Resize to 256×256 or 512×512 for faster processing
2. **SIFT**: Most computationally intensive; use fewer octaves for speed
3. **PCA**: Reduce components gradually to find optimal balance
4. **Threading**: Processing happens in background; UI remains responsive

## 🎨 Interface Layout

### Processing Tab
- Left panel: Image preprocessing controls
- Right panel: Original and preprocessed image display

### Features Tab
- Left panel: Feature extraction and dimensionality reduction controls
- Right panel: Results table with feature properties

### Analysis Tab
- Feature extraction visualization
- Dimensionality reduction visualization
- Side-by-side comparison

## 🐛 Troubleshooting

### Image Won't Load
- Ensure file is in supported format
- Check file permissions
- Try a different image

### Slow Processing
- Reduce image size
- Lower number of SIFT octaves
- Use faster features (LBP, Sobel)

### Memory Issues
- Process smaller images
- Close other applications
- Reduce PCA components

## 📝 Architecture Notes

- **Modular Design**: Separation of concerns with core, gui, and utils packages
- **Custom Algorithms**: All image processing implemented from scratch
- **Efficient Threading**: Non-blocking operations for responsive UI
- **Styled Widgets**: Custom tkinter widgets with modern aesthetics
- **Clean Code**: Well-organized, documented, and maintainable

## 🔐 Code Quality

- Type hints where applicable
- Comprehensive error handling
- Input validation for all operations
- Clear separation of concerns
- Extensive comments and docstrings

## 📄 License

This project is provided as-is for educational and forensic analysis purposes.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Optimize performance

---

**Version**: 2.0 (Pro Edition)  
**Last Updated**: December 2024
