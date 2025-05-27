from setuptools import setup, find_packages

setup(
    name="articles_project",
    version="0.1.0",
    packages=find_packages(where="lib"),
    package_dir={"": "lib"},
    install_requires=[
        # List dependencies here, e.g. 'requests', 'sqlalchemy', etc.
    ],
    entry_points={
        "console_scripts": [
            # Add CLI commands here if any, e.g. 'articles-cli=lib.cli:main'
        ],
    },
)
