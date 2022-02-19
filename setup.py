"""setup.py."""

import json
import os
import re

import setuptools

VERSION_SPECIFIER_RE = re.compile(
    r"""
    [a-zA-Z]*
    (?P<major>\d+)
    \.?
    (?P<minor>(?<=\.)\d+)?
    \.?
    (?P<patch>(?<=\.)\d+)?
    """,
    flags=re.VERBOSE,
)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(THIS_DIR)

with open("package.json", encoding="utf-8") as vfile, open(
    "requirements.txt", encoding="utf-8"
) as reqfile, open("README.md", encoding="utf-8") as readme:
    requirements = reqfile.read()
    long_description = readme.read()
    vfilecontents = json.load(vfile)
    version_str = vfilecontents["version"]
    valid_version = VERSION_SPECIFIER_RE.match(version_str)
    name = vfilecontents["name"]

if not valid_version:
    raise TypeError(f"Invalid version: {version_str}")
version = ".".join(filter(None, valid_version.groups()))


if __name__ == "__main__":
    setuptools.setup(
        name=name,
        version=version,
        author="Bernard Cooke",
        description="<Add short description>",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="<Add project url>",
        project_urls={},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        packages=setuptools.find_packages(where="src", include=["*"]),
        package_dir={
            "": "src",
        },
        include_package_data=True,
        python_requires=">=3.8",
        install_requires=requirements,
    )
