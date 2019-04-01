"""
cd directory
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup
setup(
    app=["games_collection.py"],
    options={'py2app': {'argv_emulation': True, 'packages': ['pygame', 'numpy']}},
    data_files=['assets'],
    setup_requires=["py2app"]
)
