"""Custom tkinter widgets with modern styling."""
import tkinter as tk
from tkinter import ttk
from .styles import COLORS, FONTS, BUTTON_STYLES, LABEL_STYLES, FRAME_STYLES


class ModernButton(tk.Button):
    """Modern styled button with hover effects."""
    
    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        button_style = BUTTON_STYLES[style].copy()
        button_style.update(kwargs)
        
        super().__init__(parent, text=text, command=command, **button_style)
        
        self.style_type = style
        self.original_bg = button_style['bg']
        self.original_fg = button_style['fg']
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
    
    def _on_enter(self, event):
        """Hover effect."""
        if self.style_type == 'primary':
            self.config(bg=COLORS['accent_secondary'])
        else:
            self.config(bg=COLORS['divider'])
    
    def _on_leave(self, event):
        """Reset hover effect."""
        self.config(bg=self.original_bg)


class ModernLabel(tk.Label):
    """Modern styled label."""
    
    def __init__(self, parent, text, style='body', **kwargs):
        label_style = LABEL_STYLES[style].copy()
        label_style.update(kwargs)
        
        super().__init__(parent, text=text, **label_style)


class ModernFrame(tk.Frame):
    """Modern styled frame."""
    
    def __init__(self, parent, style='primary', **kwargs):
        frame_style = FRAME_STYLES[style].copy()
        frame_style.update(kwargs)
        
        super().__init__(parent, **frame_style)


class ProgressBar(tk.Canvas):
    """Custom progress bar with modern styling."""
    
    def __init__(self, parent, max_value=100, height=20, **kwargs):
        super().__init__(parent, height=height, bg=COLORS['bg_tertiary'], 
                         relief='flat', bd=0, highlightthickness=1,
                         highlightbackground=COLORS['border'], **kwargs)
        
        self.max_value = max_value
        self.current_value = 0
        self.height = height
        self.bind('<Configure>', self._on_configure)
    
    def set_value(self, value):
        """Set progress bar value."""
        self.current_value = min(value, self.max_value)
        self.draw()
    
    def draw(self):
        """Draw progress bar."""
        self.delete('all')
        
        width = self.winfo_width()
        if width <= 1:
            return
        
        fill_width = (self.current_value / self.max_value) * width if self.max_value > 0 else 0
        
        # Background
        self.create_rectangle(0, 0, width, self.height, fill=COLORS['bg_tertiary'], 
                            outline=COLORS['border'])
        
        # Progress fill
        self.create_rectangle(0, 0, fill_width, self.height, fill=COLORS['accent_primary'],
                            outline=COLORS['accent_primary'])
        
        # Text
        percentage = (self.current_value / self.max_value * 100) if self.max_value > 0 else 0
        self.create_text(width // 2, self.height // 2, 
                        text=f'{percentage:.0f}%',
                        font=FONTS['small'],
                        fill=COLORS['text_primary'],
                        anchor='center')
    
    def _on_configure(self, event):
        """Redraw on resize."""
        self.draw()


class StatusBar(tk.Frame):
    """Modern status bar for application status."""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg_secondary'], height=30, **kwargs)
        self.pack_propagate(False)
        
        self.status_label = ModernLabel(self, text='Ready', style='body')
        self.status_label.pack(side='left', padx=15, pady=5)
        
        self.info_label = ModernLabel(self, text='', style='body')
        self.info_label.pack(side='right', padx=15, pady=5)
    
    def set_status(self, text, color='info'):
        """Update status text."""
        self.status_label.config(text=text, fg=COLORS[color])
    
    def set_info(self, text):
        """Update info text."""
        self.info_label.config(text=text)
