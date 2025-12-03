from PyInstaller.utils.hooks import collect_dynamic_libs

# Collects all DLLs associated with PySide6
binaries = collect_dynamic_libs('PySide6')
hiddenimports = ['PySide6']
