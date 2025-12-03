from PyInstaller.utils.hooks import collect_dynamic_libs

# Collects all DLLs associated with opencv-python
binaries = collect_dynamic_libs('opencv-python')
hiddenimports = ['opencv-python']
