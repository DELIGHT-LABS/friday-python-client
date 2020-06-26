from os import path

from setuptools import setup


def read(file_name: str) -> str:
    """Helper to read README."""
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, file_name), encoding="utf-8") as f:
        return f.read()


setup(
    name="hdacpy",
    version="0.5.2",  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT
    author="psy2848048",
    author_email="psy2848048@users.noreply.github.com",
    description="Tools for Hdac wallet management and offline transaction signing",
    url="https://github.com/psy2848048/hdacpy",
    project_urls={"Changelog": "https://github.com/psy2848048/hdacpy/blob/master/CHANGELOG.md"},
    packages=["hdacpy"],
    package_data={"hadcpy": ["py.typed"]},
    zip_safe=False,  # For mypy to be able to find the installed package
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=[
        "ecdsa>=0.14.0,<0.15.0",
        "bech32>=1.1.0,<2.0.0",
        "typing-extensions>=3.7.4,<4.0.0; python_version<'3.8'",
    ],
    python_requires=">=3.6",
    keywords="hdac blockchain cryptocurrency python sdk",
    classifiers=[
        "Typing :: Typed",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
