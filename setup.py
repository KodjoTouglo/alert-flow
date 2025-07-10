from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages


setup(
    name="alert-flow",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*py")],
    include_package_data=True,
    zip_safe=False,
    install_requires=["fpdf", "typer", "aiofiles", "matplotlib", "pandas"],
)
