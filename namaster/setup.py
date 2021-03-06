#!/usr/bin/env python
import sys
from setuptools import setup, Extension

# Get numpy include directory (works across versions)
import numpy
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

if '--enable-fftw-pthreads' in sys.argv:
    sys.argv.pop(sys.argv.index('--enable-fftw-pthreads'))
    FFTW_LIBS = ['fftw3', 'fftw3_threads', 'pthread']
else:
    FFTW_LIBS = ['fftw3', 'fftw3_omp']

if '--disable-openmp' in sys.argv:
    sys.argv.pop(sys.argv.index('--disable-openmp'))
    USE_OPENMP = False
else:
    USE_OPENMP = True

libs = [
    'nmt', 'sharp', 'fftpack', 'c_utils', 'chealpix', 'cfitsio', 'gsl',
    'gslcblas', 'm'] + FFTW_LIBS

use_icc = False  # Set to True if you compiled libsharp with icc
if use_icc:
    extra = []
    if USE_OPENMP:
        libs += ['gomp', 'iomp5']
        extra += ['-openmp']
else:
    extra = ['-O4']
    if USE_OPENMP:
        libs += ['gomp']
        extra += ['-fopenmp']

_nmtlib = Extension("_nmtlib",
                    ["pymaster/namaster_wrap.c"],
                    library_dirs=["/opt/ohpc/pub/libs/gnu8/gsl/2.5/lib", "/opt/ohpc/pub/apps/libsharp-gnu8-mvapich/lib", "/usr/lib64", "/opt/ohpc/pub/libs/gnu8/mvapich2/fftw/3.3.8/lib", "/opt/ohpc/pub/apps/NaMaster-gnu8-mvapich2/lib"],
                    libraries=libs,
                    include_dirs=[numpy_include, "../src/", "/opt/ohpc/pub/apps/libsharp-gnu8-mvapich/include/", "/opt/ohpc/pub/libs/gnu8/gsl/2.5/include", "/opt/ohpc/pub/libs/gnu8/mvapich2/fftw/3.3.8/include/", "/opt/ohpc/pub/apps/libsharp-gnu8-mvapich/include/"],
                    extra_compile_args=extra,
                    )

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="pymaster",
      version="1.0",
      author="David Alonso",
      author_email="david.alonso@physics.ox.ac.uk",
      description="Library for pseudo-Cl computation",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/LSSTDESC/NaMaster",
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Operating System :: Unix',
          'Operating System :: MacOS'],
      packages=['pymaster'],
      ext_modules=[_nmtlib],
      )
