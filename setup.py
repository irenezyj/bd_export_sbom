import setuptools
import platform

platform_system = platform.system()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bd_export_sbom",
    version="1.0",
    author="Irene Zhang",
    author_email="irenez@synosys.com",
    description="Export a SBOM report from a Black Duck project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/irenezyj/bd_export_sbom",
    packages=setuptools.find_packages(),
    install_requires=['blackduck>=1.0.0',
                      'lxml',
                      'aiohttp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache-2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    entry_points={
        'console_scripts': ['bd_export_sbom=export_sbom.main:run'],
    },
)
