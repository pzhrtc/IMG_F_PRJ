# Project File Structure Reference

## 📁 Complete Directory Tree

```
proo/
│
├── main.py                          # Entry point (25 lines)
│   └── Imports gui.ImageForensicsGUIApp
│
├── requirements.txt                 # Python dependencies
│   └── Lists all required packages
│
├── README.md                        # Complete documentation
│   └── Features, usage, troubleshooting
│
├── QUICKSTART.md                    # Quick start guide
│   └── Installation and first use
│
├── UPGRADE_SUMMARY.md               # This upgrade summary
│   └── What changed and why
│
├── core/                            # Image Processing Engine
│   ├── __init__.py                  # Package exports
│   │   └── Exports: CustomImageProcessing
│   │
│   └── image_processor.py           # Main processing class (~800 lines)
│       ├── CustomImageProcessing class
│       ├── Preprocessing methods
│       │   ├── rgb_to_grayscale()
│       │   ├── resize_bilinear()
│       │   ├── histogram_equalization()
│       │   └── compute_gradient()
│       ├── Feature extraction methods
│       │   ├── compute_sift_keypoints()
│       │   ├── compute_glcm()
│       │   ├── compute_lbp()
│       │   ├── gaussian_blur()
│       │   └── Helper methods
│       └── Dimensionality reduction
│           └── pca_reduction()
│
├── gui/                             # User Interface (700+ lines)
│   ├── __init__.py                  # Package exports
│   │   └── Exports: ImageForensicsGUIApp
│   │
│   ├── main_window.py               # Main application (~500 lines)
│   │   ├── ImageForensicsGUIApp class
│   │   ├── create_ui()
│   │   ├── _create_header()
│   │   ├── _create_content_area()
│   │   ├── _create_processing_tab()
│   │   ├── _create_feature_tab()
│   │   ├── _create_analysis_tab()
│   │   ├── Image processing methods
│   │   │   ├── import_image()
│   │   │   ├── to_grayscale()
│   │   │   ├── resize_image()
│   │   │   ├── enhance_contrast()
│   │   │   ├── extract_features()
│   │   │   └── reduce_features()
│   │   ├── Threading methods
│   │   │   ├── _extract_features_thread()
│   │   │   └── _reduce_features_thread()
│   │   ├── Export methods
│   │   │   ├── save_feature_image()
│   │   │   └── save_reduced_image()
│   │   ├── UI utilities
│   │   │   ├── display_image()
│   │   │   ├── reset_app()
│   │   │   └── clear_* methods
│   │
│   ├── styles.py                    # Theme & Styling (~150 lines)
│   │   ├── COLORS dictionary
│   │   │   ├── Primary colors
│   │   │   ├── Accent colors
│   │   │   ├── Text colors
│   │   │   └── Status colors
│   │   ├── FONTS dictionary
│   │   │   ├── title, subtitle, body, small, mono
│   │   │
│   │   ├── BUTTON_STYLES dictionary
│   │   │   ├── primary, secondary, danger styles
│   │   │
│   │   ├── LABEL_STYLES dictionary
│   │   │   ├── title, subtitle, body styles
│   │   │
│   │   └── FRAME_STYLES dictionary
│   │       ├── primary, secondary, panel styles
│   │
│   ├── widgets.py                   # Custom Widgets (~200 lines)
│   │   ├── ModernButton class
│   │   │   ├── Custom styled button
│   │   │   ├── Hover effects
│   │   │   └── Style variants
│   │   │
│   │   ├── ModernLabel class
│   │   │   └── Styled label with themes
│   │   │
│   │   ├── ModernFrame class
│   │   │   └── Styled frame with themes
│   │   │
│   │   ├── ProgressBar class
│   │   │   ├── Custom canvas-based progress bar
│   │   │   ├── set_value()
│   │   │   └── draw()
│   │   │
│   │   └── StatusBar class
│   │       ├── Application status display
│   │       ├── set_status()
│   │       └── set_info()
│   │
│   └── __init__.py                  # Package exports
│       └── Exports: ImageForensicsGUIApp
│
└── utils/                           # Utility Functions (~150 lines)
    ├── __init__.py                  # Package exports
    │   └── Exports helpers and validators
    │
    ├── helpers.py                   # Utility Functions (~100 lines)
    │   ├── draw_keypoints()
    │   │   └── Draw SIFT keypoints on image
    │   │
    │   ├── create_feature_overlay()
    │   │   └── Overlay features on image
    │   │
    │   ├── gaussian_heatmap()
    │   │   └── Generate gaussian heatmap
    │   │
    │   ├── clip_value()
    │   │   └── Clip value to range
    │   │
    │   └── scale_image_to_fit()
    │       └── Scale image to fit bounds
    │
    ├── validators.py                # Input Validation (~60 lines)
    │   ├── validate_image()
    │   │   └── Validate image array
    │   │
    │   ├── validate_dimensions()
    │   │   └── Validate image dimensions
    │   │
    │   └── validate_components()
    │       └── Validate PCA components
    │
    └── __init__.py                  # Package exports


```

## 📊 File Statistics

| File | Lines | Purpose |
|------|-------|---------|
| main.py | 25 | Entry point |
| core/image_processor.py | 800 | All algorithms |
| gui/main_window.py | 500 | Main GUI |
| gui/widgets.py | 200 | Custom widgets |
| gui/styles.py | 150 | Themes |
| utils/helpers.py | 100 | Utilities |
| utils/validators.py | 60 | Validation |
| Various __init__.py | 20 | Package init |
| **Total** | **1,855** | **Complete app** |

## 🔄 Code Dependencies

```
main.py
  └── gui/
      ├── main_window.py
      │   ├── core/image_processor.py
      │   ├── utils/
      │   │   ├── validators.py
      │   │   └── helpers.py
      │   ├── gui/styles.py
      │   └── gui/widgets.py
      │       └── gui/styles.py
      │
      └── widgets.py
          └── styles.py
```

## 📝 Key Classes

### Core Package
- **CustomImageProcessing**: Static methods for all image processing
  - 25+ static methods
  - ~800 lines of code
  - No external dependencies (except numpy, PIL, scikit-image)

### GUI Package
- **ImageForensicsGUIApp**: Main application window
  - ~500 lines, 30+ methods
  - Handles all UI interactions
  - Threading for background operations

- **ModernButton**: Custom styled button
- **ModernLabel**: Styled text label
- **ModernFrame**: Styled container frame
- **ProgressBar**: Custom progress visualization
- **StatusBar**: Application status display

### Utils Package
- **Validators**: Input validation functions
- **Helpers**: Image processing utilities

## 🎯 Control Flow

### Application Launch
```
main.py (main())
  └── create root window
  └── ImageForensicsGUIApp(root)
      ├── create_ui()
      │   ├── _create_header()
      │   ├── _create_content_area()
      │   │   ├── _create_processing_tab()
      │   │   ├── _create_feature_tab()
      │   │   └── _create_analysis_tab()
      │   └── StatusBar()
      └── enter mainloop()
```

### Feature Extraction Flow
```
extract_features() (UI thread)
  └── threading.Thread(_extract_features_thread)
      ├── Preprocess image
      ├── Call processor.compute_*()
      ├── Update progress bar
      ├── Display results
      └── Update status bar
```

## 📦 Module Responsibilities

### core/
- Pure image processing algorithms
- No UI dependencies
- Reusable anywhere
- Well-documented methods

### gui/
- All UI code
- tkinter widgets
- Event handling
- User interactions
- Threading management

### utils/
- Shared utilities
- Input validation
- Helper functions
- Data visualization utilities

### main.py
- Application entry point
- Minimal dependencies
- Clean startup

## 🔧 Configuration

### No Config File Needed!
All configuration is:
- **Hardcoded defaults**: 256×256 resize, 50 PCA components
- **User-adjustable**: Via GUI text entries
- **Theme-based**: Defined in styles.py

### To Change Theme:
Edit `gui/styles.py`:
```python
COLORS = {
    'accent_primary': '#00d9ff',  # Change cyan color
    'bg_primary': '#1e1e2e',      # Change background
    # ... etc
}
```

## 🚀 Extending the Application

### Add New Feature Extraction Method
1. Add method to `core/image_processor.py`
2. Add UI in `gui/main_window.py` feature_tab
3. Add validator in `utils/validators.py` if needed

### Add New Processing Step
1. Add method to `core/image_processor.py`
2. Create new tab in `gui/main_window.py`
3. Call processor method from UI

### Change Theme
1. Edit colors in `gui/styles.py`
2. Update fonts if needed
3. Restart application

## 📚 Documentation Map

| Document | Purpose |
|----------|---------|
| README.md | Complete feature documentation |
| QUICKSTART.md | Getting started guide |
| UPGRADE_SUMMARY.md | What changed in this update |
| FILE_STRUCTURE.md | This file - code organization |
| Inline comments | Implementation details |
| Docstrings | Function documentation |

---

This structure makes the code:
- ✅ Easy to understand
- ✅ Easy to maintain
- ✅ Easy to extend
- ✅ Professional quality
- ✅ Scalable for future features
