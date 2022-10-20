from setuptools import setup

setup(
    # Your setup arguments
    python_requires='>=3.6',  # Your supported Python ranges
    name = "lightMol",
    version = "0.0.1",
    description = "",
    author = "Sergey Sosnin <serg.sosnin@gmail.com>",
    include_package_data=True,
    install_requires=[],
    packages=["lightMol"],
    package_data={},
    license = "MIT",
)

