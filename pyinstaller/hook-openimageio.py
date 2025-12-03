from PyInstaller.utils.hooks import collect_dynamic_libs

# Collecte toutes les DLL associées à OpenImageIO
binaries = collect_dynamic_libs('OpenImageIO')
hiddenimports = ['OpenImageIO']
