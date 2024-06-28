from setuptools import setup, find_packages

import simple_catalog


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="simple-catalog",
    version=simple_catalog.__version__,
    author="hgyoon",
    author_email="hgyoon@wellbia.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Simple way to add file catalog with python",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["simple-catalog-cli=simple_catalog.__main__:main"]
    },
    install_requires=["pymysql"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
