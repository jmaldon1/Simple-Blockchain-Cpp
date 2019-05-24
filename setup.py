#!/usr/bin/env python

"""
setup.py file for simple c++ blockchain

HOW TO RUN:

first run: `swig -c++ -python blockchain.i`
second run: `python3 setup.py build_ext --inplace`

"""

from distutils.core import setup, Extension
import os

os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.14"

blockchain_module = Extension('_blockchain',
                              sources=['blockchain_wrap.cxx',
                                       'src/blockchain.cpp',
                                       'src/sha256.cpp'],
                              extra_compile_args=['-stdlib=libc++']
                              )

setup(name='blockchain',
      version='0.1',
      author="Joshua Maldonado",
      description="""Simple blockchain written in C++""",
      ext_modules=[blockchain_module],
      py_modules=["blockchain"]
      )
