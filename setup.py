#!/usr/bin/env python

from setuptools import setup

setup(
      name='ankita',
      version='3.1',
      description='Well designed MS-Paint like paint program written in PyQt4',
      long_description='''To run it you need PyQt4 module and PIL module.  
Install python-qt4 (for PyQt4 module) and python-pil(for Python Imaging Library) in debian based distros''',
      keywords='pyqt pyqt4 paint',
      url='http://github.com/ksharindam/ankita',
      author='Arindam Chaudhuri',
      author_email='ksharindam@gmail.com',
      license='GNU GPLv3',
      packages=['ankita'],
#      install_requires=['PyQt4',      ],
      classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Environment :: X11 Applications :: Qt',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 2.7',
      ],
      entry_points={
          'console_scripts': ['ankita=ankita.main:main'],
      },
#      include_package_data=True,
      zip_safe=False)
