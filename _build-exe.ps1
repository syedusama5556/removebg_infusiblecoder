# Install required packages
pip install pyinstaller
pip install -e ".[cli]"
pip uninstall typing
pip uninstall pathlib
# Create PyInstaller spec file with specified data collections
# pyi-makespec --collect-data=gradio_client --collect-data=gradio removebg_infusiblecoder.py

# Run PyInstaller with the generated spec file
pyinstaller removebg_infusiblecoder.spec