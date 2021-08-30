from setuptools import setup, find_packages


setup(
    name="operate_drive",
    version="0.1.2",
    packages=find_packages(exclude=["tests.*", "tests"]),
    install_requires=["PyDrive2"],
)
