"""Modern GUI theme and styling definitions."""

# Modern Dark Theme Colors
COLORS = {
    # Primary
    'bg_primary': '#1e1e2e',      # Dark background
    'bg_secondary': '#2d2d44',    # Slightly lighter
    'bg_tertiary': '#3d3d5c',     # Even lighter for panels
    
    # Accent
    'accent_primary': '#00d9ff',  # Cyan
    'accent_secondary': '#ff006e', # Pink/Magenta
    'accent_tertiary': '#ffbe0b',  # Yellow
    
    # Text
    'text_primary': '#f0f0f0',    # Light gray
    'text_secondary': '#b0b0b0',  # Medium gray
    'text_muted': '#707070',      # Dark gray
    
    # Special
    'success': '#00ff41',         # Green
    'warning': '#ffbe0b',         # Yellow
    'error': '#ff006e',           # Red
    'info': '#00d9ff',            # Cyan
    
    # Borders and dividers
    'border': '#3d3d5c',
    'divider': '#454560',
}

# Font configurations
FONTS = {
    'title': ('Segoe UI', 16, 'bold'),
    'subtitle': ('Segoe UI', 12, 'bold'),
    'button': ('Segoe UI', 10),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9),
    'mono': ('Courier New', 9),
}

# Button styles
BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['accent_primary'],
        'fg': COLORS['bg_primary'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'padx': 15,
        'pady': 8,
        'cursor': 'hand2',
    },
    'secondary': {
        'bg': COLORS['bg_tertiary'],
        'fg': COLORS['text_primary'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'padx': 15,
        'pady': 8,
        'cursor': 'hand2',
        'activebackground': COLORS['divider'],
    },
    'danger': {
        'bg': COLORS['error'],
        'fg': COLORS['bg_primary'],
        'font': FONTS['button'],
        'relief': 'flat',
        'bd': 0,
        'padx': 15,
        'pady': 8,
        'cursor': 'hand2',
    },
}

# Label styles
LABEL_STYLES = {
    'title': {
        'bg': COLORS['bg_primary'],
        'fg': COLORS['accent_primary'],
        'font': FONTS['title'],
    },
    'subtitle': {
        'bg': COLORS['bg_secondary'],
        'fg': COLORS['text_primary'],
        'font': FONTS['subtitle'],
    },
    'body': {
        'bg': COLORS['bg_primary'],
        'fg': COLORS['text_primary'],
        'font': FONTS['body'],
    },
}

# Frame styles
FRAME_STYLES = {
    'primary': {
        'bg': COLORS['bg_primary'],
        'relief': 'flat',
        'bd': 0,
    },
    'secondary': {
        'bg': COLORS['bg_secondary'],
        'relief': 'flat',
        'bd': 0,
    },
    'panel': {
        'bg': COLORS['bg_tertiary'],
        'relief': 'solid',
        'bd': 1,
        'highlightbackground': COLORS['border'],
        'highlightthickness': 1,
    },
}
