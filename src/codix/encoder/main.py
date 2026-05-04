"""
Main application module
"""
from codix.encoder.encoder import Application, __version__

def main():
    app = Application()
    app.title(\
    f'Codix - The Swiss knife for coding behaviors - version: {__version__}')
    app.mainloop()

if __name__ == "__main__":
    main()
