import bpy
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("fast_vamp_utils.py")
)