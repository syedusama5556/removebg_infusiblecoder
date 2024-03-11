@echo off
rmdir /s /q "dist"
pip uninstall removebg-infusiblecoder -y
python setup.py sdist bdist_wheel
cd dist
for %%f in (removebg_infusiblecoder-*.whl) do (
    pip install "%%f[cli]" -U
)
removebg_infusiblecoder s
pause
