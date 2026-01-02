"""Main GUI window with modern dark theme and improved UX."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk
import threading
import os
from pathlib import Path

from core import CustomImageProcessing
from utils.validators import validate_image, validate_dimensions
from utils.helpers import draw_keypoints, create_feature_overlay
from .styles import COLORS, FONTS
from .widgets import ModernButton, ModernLabel, ModernFrame, ProgressBar, StatusBar


class ImageForensicsGUIApp:
    """Main Application Window with modern dark theme."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Image Forensics Project")
        
        # Set dark theme
        self.root.configure(bg=COLORS['bg_primary'])
        
        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width-100}x{screen_height-100}")
        
        # Initialize processor
        self.processor = CustomImageProcessing()
        
        # State variables
        self.original_image = None
        self.preprocessed_image = None
        self.feature_extracted_image = None
        self.reduced_image = None
        self.image_path = None
        self.keypoints = None
        self.processing = False
        
        # Create UI
        self.create_ui()
    
    def create_ui(self):
        """Create the user interface."""
        # Main container with scrollable content
        main_container = ModernFrame(self.root, style='primary')
        main_container.pack(fill='both', expand=True)
        
        # Header
        self._create_header(main_container)
        
        # Content area with tabs
        self._create_content_area(main_container)
        
        # Status bar
        self.status_bar = StatusBar(main_container)
        self.status_bar.pack(side='bottom', fill='x')
    
    def _create_header(self, parent):
        """Create header with title and quick actions."""
        header = ModernFrame(parent, style='secondary')
        header.pack(fill='x', padx=0, pady=0)
        
        # Title
        title = ModernLabel(header, text='🔍 Image Forensics Project', style='title')
        title.pack(side='left', padx=20, pady=15)
        
        # Quick action buttons
        button_frame = ModernFrame(header, style='secondary')
        button_frame.pack(side='right', padx=20, pady=15)
        
        ModernButton(button_frame, '📁 Import', command=self.import_image, 
                    style='primary').pack(side='left', padx=5)
        ModernButton(button_frame, '🔄 Reset', command=self.reset_app, 
                    style='secondary').pack(side='left', padx=5)
    
    def _create_content_area(self, parent):
        """Create tabbed content area."""
        # Create notebook (tabs)
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Style notebook
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=COLORS['bg_primary'], 
                       borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', COLORS['accent_primary'])],
                 foreground=[('selected', COLORS['bg_primary'])])
        
        # Tab 1: Processing
        processing_frame = ModernFrame(notebook, style='primary')
        notebook.add(processing_frame, text='  Processing  ')
        self._create_processing_tab(processing_frame)
        
        # Tab 2: Feature Extraction
        feature_frame = ModernFrame(notebook, style='primary')
        notebook.add(feature_frame, text='  Features  ')
        self._create_feature_tab(feature_frame)
        
        # Tab 3: Analysis
        analysis_frame = ModernFrame(notebook, style='primary')
        notebook.add(analysis_frame, text='  Analysis  ')
        self._create_analysis_tab(analysis_frame)
    
    def _create_processing_tab(self, parent):
        """Create image preprocessing tab."""
        # Left panel - Controls
        control_panel = ModernFrame(parent, style='secondary')
        control_panel.pack(side='left', fill='y', padx=10, pady=10)
        
        ModernLabel(control_panel, text='Preprocessing Tools', style='subtitle').pack(
            fill='x', padx=10, pady=10)
        
        # Grayscale
        frame = ModernFrame(control_panel, style='panel')
        frame.pack(fill='x', padx=10, pady=5)
        ModernLabel(frame, text='Grayscale Conversion', style='body').pack(anchor='w', padx=5, pady=5)
        ModernButton(frame, 'Convert to Grayscale', command=self.to_grayscale, 
                    style='primary').pack(fill='x', padx=5, pady=5)
        
        # Resize
        frame = ModernFrame(control_panel, style='panel')
        frame.pack(fill='x', padx=10, pady=5)
        ModernLabel(frame, text='Resize Image', style='body').pack(anchor='w', padx=5, pady=5)
        
        dim_frame = ModernFrame(frame, style='panel')
        dim_frame.pack(fill='x', padx=5, pady=3)
        ModernLabel(dim_frame, text='Width:', style='body').pack(side='left')
        self.resize_width = tk.Entry(dim_frame, width=10, bg=COLORS['bg_tertiary'],
                                     fg=COLORS['text_primary'], font=FONTS['body'],
                                     relief='flat', bd=1, insertbackground=COLORS['accent_primary'])
        self.resize_width.insert(0, '256')
        self.resize_width.pack(side='left', padx=5)
        
        ModernLabel(dim_frame, text='Height:', style='body').pack(side='left')
        self.resize_height = tk.Entry(dim_frame, width=10, bg=COLORS['bg_tertiary'],
                                      fg=COLORS['text_primary'], font=FONTS['body'],
                                      relief='flat', bd=1, insertbackground=COLORS['accent_primary'])
        self.resize_height.insert(0, '256')
        self.resize_height.pack(side='left', padx=5)
        
        ModernButton(frame, 'Apply Resize', command=self.resize_image, 
                    style='primary').pack(fill='x', padx=5, pady=5)
        # Combined Grayscale + Resize
        ModernButton(frame, 'Grayscale + Resize', command=self.grayscale_and_resize_action,
                style='primary').pack(fill='x', padx=5, pady=5)
        
        # Histogram Equalization
        frame = ModernFrame(control_panel, style='panel')
        frame.pack(fill='x', padx=10, pady=5)
        ModernLabel(frame, text='Histogram Equalization', style='body').pack(anchor='w', padx=5, pady=5)
        ModernButton(frame, 'Enhance Contrast', command=self.enhance_contrast, 
                    style='primary').pack(fill='x', padx=5, pady=5)
        
        # Right panel - Image displays
        image_panel = ModernFrame(parent, style='primary')
        image_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        # Original
        ModernLabel(image_panel, text='Original Image', style='subtitle').pack(fill='x')
        self.original_label = tk.Label(image_panel, bg=COLORS['bg_tertiary'], 
                                       width=300, height=300, relief='solid', bd=1)
        self.original_label.pack(padx=5, pady=5)
        
        # Preprocessed
        ModernLabel(image_panel, text='Preprocessed Image', style='subtitle').pack(fill='x')
        self.preprocessed_label = tk.Label(image_panel, bg=COLORS['bg_tertiary'],
                                           width=300, height=300, relief='solid', bd=1)
        self.preprocessed_label.pack(padx=5, pady=5)
    
    def _create_feature_tab(self, parent):
        """Create feature extraction tab."""
        # Left panel - Controls
        control_panel = ModernFrame(parent, style='secondary')
        control_panel.pack(side='left', fill='y', padx=10, pady=10)
        
        ModernLabel(control_panel, text='Feature Extraction', style='subtitle').pack(
            fill='x', padx=10, pady=10)
        
        # Feature selection
        frame = ModernFrame(control_panel, style='panel')
        frame.pack(fill='x', padx=10, pady=5)
        ModernLabel(frame, text='Select Technique:', style='body').pack(anchor='w', padx=5, pady=3)
        
        self.feature_var = tk.StringVar(value='SIFT')
        feature_options = ['SIFT', 'GLCM', 'LBP', 'Sobel']
        self.feature_menu = ttk.Combobox(frame, textvariable=self.feature_var,
                                        values=feature_options, state='readonly',
                                        width=20, font=FONTS['body'])
        self.feature_menu.pack(fill='x', padx=5, pady=3)
        
        ModernButton(frame, 'Extract Features', command=self.extract_features,
                    style='primary').pack(fill='x', padx=5, pady=5)
        
        # PCA Reduction
        frame = ModernFrame(control_panel, style='panel')
        frame.pack(fill='x', padx=10, pady=5)
        ModernLabel(frame, text='Dimensionality Reduction', style='body').pack(anchor='w', padx=5, pady=3)
        
        comp_frame = ModernFrame(frame, style='panel')
        comp_frame.pack(fill='x', padx=5, pady=3)
        ModernLabel(comp_frame, text='PCA Components:', style='body').pack(side='left')
        self.pca_components = tk.Entry(comp_frame, width=10, bg=COLORS['bg_tertiary'],
                                       fg=COLORS['text_primary'], font=FONTS['body'],
                                       relief='flat', bd=1, insertbackground=COLORS['accent_primary'])
        self.pca_components.insert(0, '50')
        self.pca_components.pack(side='left', padx=5)
        
        ModernButton(frame, 'Apply PCA Reduction', command=self.reduce_features,
                    style='primary').pack(fill='x', padx=5, pady=5)
        
        # Export
        frame = ModernFrame(control_panel, style='panel')
        frame.pack(fill='x', padx=10, pady=5)
        ModernLabel(frame, text='Export Results', style='body').pack(anchor='w', padx=5, pady=3)
        ModernButton(frame, 'Save Feature Image', command=self.save_feature_image,
                    style='primary').pack(fill='x', padx=5, pady=5)
        ModernButton(frame, 'Save Reduced Image', command=self.save_reduced_image,
                    style='secondary').pack(fill='x', padx=5, pady=5)
        
        # Progress
        frame = ModernFrame(control_panel, style='panel')
        frame.pack(fill='x', padx=10, pady=5)
        ModernLabel(frame, text='Processing:', style='body').pack(anchor='w', padx=5, pady=3)
        self.progress_bar = ProgressBar(frame, max_value=100)
        self.progress_bar.pack(fill='x', padx=5, pady=5)
        
        # Right panel - Results
        result_panel = ModernFrame(parent, style='primary')
        result_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        ModernLabel(result_panel, text='Extracted Features', style='subtitle').pack(fill='x')
        
        # Treeview for features
        self.features_table = ttk.Treeview(result_panel, columns=('Feature', 'Value'),
                                          show='headings', height=15)
        self.features_table.heading('Feature', text='Feature')
        self.features_table.heading('Value', text='Value')
        self.features_table.column('Feature', width=150)
        self.features_table.column('Value', width=150)
        
        # Style treeview
        style = ttk.Style()
        style.configure('Treeview', background=COLORS['bg_tertiary'],
                       foreground=COLORS['text_primary'], fieldbackground=COLORS['bg_tertiary'],
                       font=FONTS['small'])
        style.map('Treeview', background=[('selected', COLORS['accent_primary'])],
                 foreground=[('selected', COLORS['bg_primary'])])
        
        self.features_table.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Processed image preview
        ModernLabel(result_panel, text='Processed Preview', style='subtitle').pack(fill='x')
        self.feature_preview_label = tk.Label(result_panel, bg=COLORS['bg_tertiary'],
                              width=300, height=300, relief='solid', bd=1)
        self.feature_preview_label.pack(padx=5, pady=5)
    def _create_analysis_tab(self, parent):
        """Create analysis visualization tab."""
        # Create a frame to hold image displays
        left_panel = ModernFrame(parent, style='primary')
        left_panel.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        ModernLabel(left_panel, text='Feature Extraction', style='subtitle').pack(fill='x')
        self.feature_extracted_label = tk.Label(left_panel, bg=COLORS['bg_tertiary'],
                                               width=400, height=300, relief='solid', bd=1)
        self.feature_extracted_label.pack(padx=5, pady=5, fill='both', expand=True)
        
        right_panel = ModernFrame(parent, style='primary')
        right_panel.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        ModernLabel(right_panel, text='Dimensionality Reduction', style='subtitle').pack(fill='x')
        self.reduced_label = tk.Label(right_panel, bg=COLORS['bg_tertiary'],
                                     width=400, height=300, relief='solid', bd=1)
        self.reduced_label.pack(padx=5, pady=5, fill='both', expand=True)
    
    def import_image(self):
        """Import an image file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                      ("All files", "*.*")])
        
        if not file_path:
            return
        
        try:
            self.status_bar.set_status('Loading image...', 'info')
            self.root.update()
            
            img_pil = Image.open(file_path).convert('RGB')
            self.original_image = np.array(img_pil)
            self.preprocessed_image = None
            self.feature_extracted_image = None
            self.reduced_image = None
            self.image_path = file_path
            
            # Display original
            self.display_image(self.original_image, self.original_label)
            self.clear_preprocessing_displays()
            self.clear_features_table()
            
            self.status_bar.set_status(f'✓ Loaded: {Path(file_path).name}', 'success')
            
        except Exception as e:
            messagebox.showerror('Error', f'Failed to load image: {str(e)}')
            self.status_bar.set_status('Error loading image', 'error')
    
    def to_grayscale(self):
        """Convert to grayscale."""
        if self.original_image is None:
            messagebox.showwarning('Warning', 'Please import an image first')
            return
        
        try:
            self.status_bar.set_status('Converting to grayscale...', 'info')
            self.root.update()
            
            if len(self.original_image.shape) == 3:
                gray = self.processor.rgb_to_grayscale(self.original_image)
            else:
                gray = self.original_image.copy()
            
            self.preprocessed_image = gray
            self.display_image(gray, self.preprocessed_label, is_gray=True)
            if hasattr(self, 'feature_preview_label'):
                self.display_image(gray, self.feature_preview_label, is_gray=True)
            
            self.status_bar.set_status('✓ Grayscale conversion complete', 'success')
            
        except Exception as e:
            messagebox.showerror('Error', f'Conversion failed: {str(e)}')
            self.status_bar.set_status('Error during conversion', 'error')
    
    def resize_image(self):
        """Resize image."""
        if self.original_image is None:
            messagebox.showwarning('Warning', 'Please import an image first')
            return
        
        try:
            width = int(self.resize_width.get())
            height = int(self.resize_height.get())
            
            if width <= 0 or height <= 0:
                messagebox.showerror('Error', 'Dimensions must be positive')
                return
            
            self.status_bar.set_status(f'Resizing to {width}x{height}...', 'info')
            self.root.update()
            
            img = self.original_image
            resized = self.processor.resize_bilinear(img, width, height)
            
            self.preprocessed_image = resized
            is_gray = len(resized.shape) == 2
            self.display_image(resized, self.preprocessed_label, is_gray=is_gray)
            if hasattr(self, 'feature_preview_label'):
                self.display_image(resized, self.feature_preview_label, is_gray=is_gray)
            
            self.status_bar.set_status(f'✓ Resized to {width}x{height}', 'success')
            
        except ValueError:
            messagebox.showerror('Error', 'Please enter valid numbers')
            self.status_bar.set_status('Invalid input', 'error')
        except Exception as e:
            messagebox.showerror('Error', f'Resize failed: {str(e)}')
            self.status_bar.set_status('Error during resize', 'error')

    def grayscale_and_resize_action(self):
        """Convert to grayscale and resize in one operation."""
        if self.original_image is None:
            messagebox.showwarning('Warning', 'Please import an image first')
            return

        try:
            width = int(self.resize_width.get())
            height = int(self.resize_height.get())

            if width <= 0 or height <= 0:
                messagebox.showerror('Error', 'Dimensions must be positive')
                return

            self.status_bar.set_status(f'Converting to grayscale and resizing to {width}x{height}...', 'info')
            self.root.update()

            img = self.original_image
            processed = self.processor.grayscale_and_resize(img, width, height)

            self.preprocessed_image = processed
            # Result will be grayscale (2D)
            self.display_image(processed, self.preprocessed_label, is_gray=True)
            if hasattr(self, 'feature_preview_label'):
                self.display_image(processed, self.feature_preview_label, is_gray=True)

            self.status_bar.set_status(f'✓ Grayscale + Resize complete ({width}x{height})', 'success')

        except ValueError:
            messagebox.showerror('Error', 'Please enter valid numbers')
            self.status_bar.set_status('Invalid input', 'error')
        except Exception as e:
            messagebox.showerror('Error', f'Operation failed: {str(e)}')
            self.status_bar.set_status('Error during operation', 'error')
    
    def enhance_contrast(self):
        """Apply histogram equalization."""
        if self.preprocessed_image is None and self.original_image is None:
            messagebox.showwarning('Warning', 'Please import an image first')
            return
        
        try:
            self.status_bar.set_status('Enhancing contrast...', 'info')
            self.root.update()
            
            img = self.preprocessed_image if self.preprocessed_image is not None else self.original_image
            
            if len(img.shape) == 3:
                gray = self.processor.rgb_to_grayscale(img)
            else:
                gray = img.copy()
            
            enhanced = self.processor.histogram_equalization(gray)
            self.preprocessed_image = enhanced
            self.display_image(enhanced, self.preprocessed_label, is_gray=True)
            if hasattr(self, 'feature_preview_label'):
                self.display_image(enhanced, self.feature_preview_label, is_gray=True)
            
            self.status_bar.set_status('✓ Contrast enhancement complete', 'success')
            
        except Exception as e:
            messagebox.showerror('Error', f'Enhancement failed: {str(e)}')
            self.status_bar.set_status('Error during enhancement', 'error')
    
    def extract_features(self):
        """Extract features using threading."""
        if self.preprocessed_image is None:
            messagebox.showwarning('Warning', 'Please preprocess image first')
            return
        
        technique = self.feature_var.get()
        
        # Run in background thread
        thread = threading.Thread(target=self._extract_features_thread, args=(technique,))
        thread.daemon = True
        thread.start()
    
    def _extract_features_thread(self, technique):
        """Background thread for feature extraction."""
        try:
            self.processing = True
            self.status_bar.set_status(f'Extracting {technique} features...', 'info')
            self.progress_bar.set_value(0)
            self.root.update()
            
            img = self.preprocessed_image.copy()
            
            if len(img.shape) == 3:
                img_gray = self.processor.rgb_to_grayscale(img)
            else:
                img_gray = img.copy()
            
            img_gray = self.processor.histogram_equalization(img_gray)
            self.progress_bar.set_value(20)
            self.root.update()
            
            if technique == 'SIFT':
                keypoints = self.processor.compute_sift_keypoints(img_gray)
                self.keypoints = keypoints
                
                feature_img = np.stack([img_gray, img_gray, img_gray], axis=-1)
                feature_img = draw_keypoints(feature_img, keypoints)
                
                self.feature_extracted_image = feature_img
                self.clear_features_table()
                self.features_table.insert('', 'end', values=('Technique', 'SIFT'))
                self.features_table.insert('', 'end', values=('Keypoints Found', len(keypoints)))
                
            elif technique == 'GLCM':
                glcm = self.processor.compute_glcm(img_gray)
                contrast, dissimilarity, homogeneity, energy, correlation = self.processor.glcm_properties(glcm)
                
                feature_img = np.stack([img_gray, img_gray, img_gray], axis=-1)
                self.feature_extracted_image = feature_img
                
                self.clear_features_table()
                self.features_table.insert('', 'end', values=('Technique', 'GLCM'))
                self.features_table.insert('', 'end', values=('Contrast', f'{contrast:.4f}'))
                self.features_table.insert('', 'end', values=('Dissimilarity', f'{dissimilarity:.4f}'))
                self.features_table.insert('', 'end', values=('Homogeneity', f'{homogeneity:.4f}'))
                self.features_table.insert('', 'end', values=('Energy', f'{energy:.4f}'))
                self.features_table.insert('', 'end', values=('Correlation', f'{correlation:.4f}'))
                
            elif technique == 'LBP':
                lbp_img = self.processor.compute_lbp(img_gray)
                feature_img = (lbp_img / lbp_img.max() * 255).astype(np.uint8) if lbp_img.max() > 0 else lbp_img
                self.feature_extracted_image = feature_img
                
                self.clear_features_table()
                self.features_table.insert('', 'end', values=('Technique', 'LBP'))
                self.features_table.insert('', 'end', values=('Patterns Found', np.sum(feature_img > 0)))
                
            elif technique == 'Sobel':
                gx, gy, magnitude = self.processor.compute_gradient(img_gray)
                self.feature_extracted_image = magnitude
                
                self.clear_features_table()
                self.features_table.insert('', 'end', values=('Technique', 'Sobel'))
                self.features_table.insert('', 'end', values=('Edges Found', np.sum(magnitude > 0)))
            
            self.progress_bar.set_value(100)
            self.display_image(self.feature_extracted_image, self.feature_extracted_label, 
                             is_gray=(len(self.feature_extracted_image.shape) == 2))
            self.root.update()
            
            self.status_bar.set_status(f'✓ {technique} extraction complete', 'success')
            
        except Exception as e:
            messagebox.showerror('Error', f'Feature extraction failed: {str(e)}')
            self.status_bar.set_status('Error during extraction', 'error')
        finally:
            self.processing = False
            self.progress_bar.set_value(0)
    
    def reduce_features(self):
        """Apply PCA reduction using threading."""
        if self.feature_extracted_image is None:
            messagebox.showwarning('Warning', 'Please extract features first')
            return
        
        try:
            n_components = int(self.pca_components.get())
            if n_components <= 0:
                messagebox.showerror('Error', 'Components must be positive')
                return
        except ValueError:
            messagebox.showerror('Error', 'Please enter a valid number')
            return
        
        # Run in background thread
        thread = threading.Thread(target=self._reduce_features_thread, args=(n_components,))
        thread.daemon = True
        thread.start()
    
    def _reduce_features_thread(self, n_components):
        """Background thread for PCA reduction."""
        try:
            self.processing = True
            self.status_bar.set_status('Applying PCA reduction...', 'info')
            self.progress_bar.set_value(50)
            self.root.update()
            
            img = self.feature_extracted_image.copy()
            
            if len(img.shape) == 3:
                img = self.processor.rgb_to_grayscale(img)
            
            img_normalized = img.astype(float) / 255.0
            h, w = img.shape
            pixels = img_normalized.reshape(h, w)
            
            max_components = min(n_components, h, w)
            reconstructed, explained_variance, actual_components = self.processor.pca_reduction(
                pixels.T, max_components)
            
            reduced_img = reconstructed.T
            reduced_img = np.uint8(np.clip(reduced_img * 255, 0, 255))
            
            self.reduced_image = reduced_img
            self.progress_bar.set_value(100)
            
            self.clear_features_table()
            self.features_table.insert('', 'end', values=('Operation', 'PCA Reduction'))
            self.features_table.insert('', 'end', values=('Components', actual_components))
            self.features_table.insert('', 'end', values=('Variance Explained', f'{explained_variance:.4f}'))
            
            self.display_image(reduced_img, self.reduced_label, is_gray=True)
            self.root.update()
            
            self.status_bar.set_status(f'✓ PCA reduction to {actual_components} components', 'success')
            
        except Exception as e:
            messagebox.showerror('Error', f'PCA reduction failed: {str(e)}')
            self.status_bar.set_status('Error during reduction', 'error')
        finally:
            self.processing = False
            self.progress_bar.set_value(0)
    
    def save_feature_image(self):
        """Save feature extracted image."""
        if self.feature_extracted_image is None:
            messagebox.showwarning('Warning', 'No feature image to save')
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension='.png',
                filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg'), ('All', '*.*')])
            
            if file_path:
                img = self.feature_extracted_image
                if len(img.shape) == 2:
                    img_pil = Image.fromarray(img, mode='L')
                else:
                    img_pil = Image.fromarray(img, mode='RGB')
                
                img_pil.save(file_path)
                messagebox.showinfo('Success', f'Saved to {Path(file_path).name}')
                self.status_bar.set_status(f'✓ Saved feature image', 'success')
                
        except Exception as e:
            messagebox.showerror('Error', f'Save failed: {str(e)}')
    
    def save_reduced_image(self):
        """Save reduced image."""
        if self.reduced_image is None:
            messagebox.showwarning('Warning', 'No reduced image to save')
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension='.png',
                filetypes=[('PNG', '*.png'), ('JPEG', '*.jpg'), ('All', '*.*')])
            
            if file_path:
                img_pil = Image.fromarray(self.reduced_image, mode='L')
                img_pil.save(file_path)
                messagebox.showinfo('Success', f'Saved to {Path(file_path).name}')
                self.status_bar.set_status(f'✓ Saved reduced image', 'success')
                
        except Exception as e:
            messagebox.showerror('Error', f'Save failed: {str(e)}')
    
    def reset_app(self):
        """Reset the application."""
        self.original_image = None
        self.preprocessed_image = None
        self.feature_extracted_image = None
        self.reduced_image = None
        self.image_path = None
        self.keypoints = None
        
        self.clear_all_displays()
        self.clear_features_table()
        self.status_bar.set_status('✓ Application reset', 'success')
    
    def display_image(self, img, label, is_gray=False):
        """Display image on label with proper scaling."""
        try:
            if len(img.shape) == 2:
                img_display = np.stack([img, img, img], axis=-1)
            else:
                img_display = img.copy()
            
            # Scale to fit label
            max_size = 300
            h, w = img_display.shape[:2]
            scale = min(max_size / h, max_size / w, 1.0)
            
            new_h = int(h * scale)
            new_w = int(w * scale)
            
            if new_h > 0 and new_w > 0:
                img_resized = self.processor.resize_bilinear(img_display, new_w, new_h)
                
                img_pil = Image.fromarray(img_resized.astype(np.uint8))
                img_tk = ImageTk.PhotoImage(img_pil)
                
                label.config(image=img_tk)
                label.image = img_tk
                
        except Exception as e:
            print(f'Error displaying image: {e}')
    
    def clear_preprocessing_displays(self):
        """Clear preprocessing display labels."""
        self.preprocessed_label.config(image='')
        self.preprocessed_label.image = None
        if hasattr(self, 'feature_preview_label'):
            self.feature_preview_label.config(image='')
            self.feature_preview_label.image = None
    
    def clear_all_displays(self):
        """Clear all image displays."""
        for label in [self.original_label, self.preprocessed_label, 
                     self.feature_extracted_label, self.reduced_label]:
            label.config(image='')
            label.image = None
        if hasattr(self, 'feature_preview_label'):
            self.feature_preview_label.config(image='')
            self.feature_preview_label.image = None
    
    def clear_features_table(self):
        """Clear features table."""
        for item in self.features_table.get_children():
            self.features_table.delete(item)
