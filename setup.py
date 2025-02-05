from setuptools import setup, find_packages

setup(
    name="proxmox_templater",
    version="1.0",
    packages=find_packages(),
    install_requires=open("requirements.txt").read().splitlines(),
    entry_points={
        "console_scripts": [
            "ptemplate=ptemplate.main:main",
        ],
    },
)

