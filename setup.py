"""
cd directory
py2app build script for MyApplication

Usage:
    python setup.py py2app
"""
from setuptools import setup
setup(
    app=["main.py"],
    options={'py2app': {'argv_emulation': True, 'packages': ['pygame']}},
    data_files=['cge.py', 'crazy_spin_pvc.py', 'crazy_spin_pvp.py', 'Assets'],
    setup_requires=["py2app"]
)
