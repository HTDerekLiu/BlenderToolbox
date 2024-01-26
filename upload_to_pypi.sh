pip cache purge

rm -rf dist
rm -rf build

pip install wheel twine

python setup.py sdist
python setup.py bdist_wheel

twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl --verbose