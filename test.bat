
pip uninstall removebg-infusiblecoder -y
python setup.py sdist bdist_wheel
cd dist
pip install removebg_infusiblecoder-0.0.5-py3-none-any.whl
removebg_infusiblecoder s