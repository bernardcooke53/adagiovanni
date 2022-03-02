# Copyright (c) 2022, Bernard Cooke
# All rights reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE.md file in the root directory of this source tree.

"""
setup.py

This is mainly present to support legacy build-system interfaces
such as direct build from source.
"""

import os

import setuptools
import toml

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
os.chdir(THIS_DIR)

with open("pyproject.toml", encoding="utf-8") as project_file, open(
    "README.md", encoding="utf-8"
) as readme, open("requirements.txt", encoding="utf-8") as reqfile:
    long_description = readme.read()
    requirements = reqfile.readlines()
    project_info = toml.load(project_file)
    project_metadata = project_info["tool"]["poetry"]
    project_urls = project_metadata["urls"]


if __name__ == "__main__":
    setuptools.setup(
        name=project_metadata["name"],
        version=project_metadata["version"],
        author=project_metadata["authors"],
        description=project_metadata["description"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        url=project_urls["Homepage"],
        project_urls=project_urls,
        classifiers=project_metadata["classifiers"],
        packages=setuptools.find_packages(where="src", include=["*"]),
        package_dir={
            "": "src",
        },
        include_package_data=True,
        python_requires=">=3.8",
        install_requires=requirements,
    )
