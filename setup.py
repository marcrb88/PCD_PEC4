from setuptools import setup, find_packages

setup(
    name="PEC4_Roige_Benaiges_Marc",
    version="0.1.0",
    description="PEC4 - Anàlisi de Rendiment i Abandonament Acadèmic",
    author="Marc Roigé Benaiges",
    author_email="marcroige@uoc.edu",

    package_dir={"": "src"},
    packages=find_packages(where="src"),

    install_requires=[
        "pandas",
        "matplotlib",
        "openpyxl",
        "numpy"
    ],
    python_requires='>=3.8',
)
