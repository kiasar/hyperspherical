from setuptools import setup, find_packages

setup(
    name="hyperspherical",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy",
    ],
    author="Peyman M. Kiasari",
    author_email="pmkiasari@gmail.com",
    description="A package for converting between Cartesian and hyper-spherical (n-sphere) coordinates",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kiasar/hyperspherical",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)