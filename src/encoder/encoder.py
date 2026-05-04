"""
Main application module
"""
from truecodix import Application, __version__

app = Application()
app.title(\
f'Codix - The Swiss knife for coding behaviors - version: {__version__}')
app.mainloop()
