import tkinter as tk
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui import ImageForensicsGUIApp


def main():
    """Launch the application."""
    root = tk.Tk()
    
    # Configure window
    root.minsize(1200, 800)
    
    # Create app
    app = ImageForensicsGUIApp(root)
    
    # Run
    root.mainloop()


if __name__ == '__main__':
    main()
