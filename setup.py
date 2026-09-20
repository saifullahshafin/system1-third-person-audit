from setuptools import setup, find_packages

setup(
    name="system1-third-person-audit",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "tpa=system1.cli:main",
            "system1=system1.cli:main",
        ],
    },
)
