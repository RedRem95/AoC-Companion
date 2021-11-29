import setuptools
from src.AoC_Companion import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AoC-Companion-RedRem",
    version=__version__,
    author="RedRem",
    description="Companion for AoC_Companion development in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedRem95/AoC-Companion",
    project_urls={
        "Bug Tracker": "https://github.com/RedRem95/AoC-Companion/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'requests'
    ]
)
