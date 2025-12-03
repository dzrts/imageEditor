from PyInstaller.utils.hooks import collect_dynamic_libs

# Collects all DLLs associated with OpenImageIO
binaries = collect_dynamic_libs('OpenImageIO')
hiddenimports = ['OpenImageIO']
