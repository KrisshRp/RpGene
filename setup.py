import os
import glob

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

import numpy as np

ext_files = glob.glob("Lib/codon/codonk/src/*.c")
ext_files.extend(glob.glob("Lib/codon/codonk/*.pyx"))

codonklib = Extension(
    "Lib.codon.codonk",
    ext_files,
    include_dirs=["Lib/codon/codonk/include/", np.get_include()],
)

this_directory = os.path.abspath(os.path.dirname(__file__))

version = '1.5.0.post1'
# For travis/pypi-test
if os.environ.get('TRAVIS') == 'true' and os.environ.get('TRAVIS_TAG') == '':
      version = ".".join(version.split('.')[:3])
      N, M = os.environ['TRAVIS_JOB_NUMBER'].split('.')
      version = "{v}-a{N}.dev{M}".format(v=version, N=N, M=M)

setup(
    name='codonk',
    version=version,
    license='GPLv2',
    packages=[
        'Lib.codon',
    ],
    setup_requires=[
        'cython',
    ],
    install_requires=[
        'numpy',
        'pandas'
    ],
    tests_require = [
        'pytest',
        'biopython',
    ],
    test_suite="pytest",
    ext_modules=cythonize([codonklib], language_level="3")
)
