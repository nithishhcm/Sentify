from setuptools import setup, find_packages

setup(
    name="sentify",
    version="0.1.0",
    description="A CLI tool to analyze user sentiment for movies or books.",
    author="Antigravity",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "textblob",
        "transformers",
        "torch",
        "pandas",
        "rich",
        "customtkinter"
    ],
    entry_points={
        "console_scripts": [
            "sentify=sentify.cli:main",
        ],
    },
)
