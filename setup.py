import os
from setuptools import setup, find_packages

rootdir = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

with open(os.path.join(rootdir, "requirements.txt"), "r") as f:
    requirements = f.read().splitlines()


setup(
    name="premji_invest",
    include_package_data=True,
    version="1.0",
    packages=find_packages(),
    install_requires=requirements,
    author="Navnitan",
    setup_requires=["pytest-runner"],
    tests_requires=["pytest"],
    entry_points={
        "console_scripts":[
            "pipeline1 = main:pipeline1",
            "pipeline2 = main:pipeline2"
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)

