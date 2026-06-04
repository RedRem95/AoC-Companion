import setuptools
import os

with open(os.path.join(os.path.dirname(__file__), "AoC_Companion", "version.txt"), "r") as fv:
    __version__ = fv.read().strip()

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = ["requests", "nose"]

setuptools.setup(
    name="AoC_Companion",
    version=__version__,
    author="RedRem",
    description="Companion for AoC_Companion development in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE',),
    url="https://github.com/RedRem95/AoC-Companion",
    project_urls={
        "Bug Tracker": "https://github.com/RedRem95/AoC-Companion/issues",
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache 2.0",
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'AoC_run = AoC_Companion.AoC.__main__:main',
        ],
    },
    packages=setuptools.find_packages(include=['AoC_Companion', 'AoC_Companion.*']),
    python_requires=">=3.11",
    install_requires=requirements,
    requires=requirements,
    include_package_data=True,
)
