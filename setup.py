import sys
from cx_Freeze import setup, Executable

# Run python setup.py build to create the exe

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name = "ahCalculator",
      version = "0.02",
      description = "Diablo 3 auction house calculator",
      executables = [Executable("ahCalculator.pyw", base=base)])

