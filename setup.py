import os
import pathlib
import sys

sys.path.append(os.path.dirname(__file__))
from setuptools import find_packages, setup

import versioneer

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

install_requires = [
    "carvekit",
    "jsonschema",
    "numpy",
    "onnxruntime",
    "opencv-contrib-python-headless",
    "pillow",
    "pooch",
    "pymatting",
    "scikit-image",
    "scipy",
    "tqdm",
    "aiohttp",
    "asyncer",
    "click",
    "fastapi",
    "filetype",
    "gradio",
    "python-multipart",
    "uvicorn",
    "watchdog",
    "requests",
]

extras_require = {
    "dev": [
        "bandit",
        "black",
        "flake8",
        "imagehash",
        "isort",
        "mypy",
        "pytest",
        "setuptools",
        "twine",
        "wheel",
    ],
    "gpu": ["onnxruntime-gpu"],
    "cli": [
        "aiohttp",
        "asyncer",
        "click",
        "fastapi",
        "filetype",
        "gradio",
        "python-multipart",
        "uvicorn",
        "watchdog",
    ],
}

entry_points = {
    "console_scripts": [
        "removebg_infusiblecoder=removebg_infusiblecoder.cli:main",
    ],
}


setup(
    name="removebg_infusiblecoder",
    description="Remove image background",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syedusama5556/removebg_infusiblecoder",
    author="Syed Usama Ahmad",
    author_email="syedusama5556@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="remove, background, u2net",
    python_requires=">=3.9, <3.13",
    packages=find_packages(),
    install_requires=install_requires,
    entry_points=entry_points,
    extras_require=extras_require,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
