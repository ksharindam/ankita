import os
from setuptools import setup
from distutils.cmd import Command
from ankita import __version__

class Build(Command):
    description = 'build c/c++ extensions'
    user_options = []     # The format is [long option, short option, description]
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system("make --directory=lib")

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='ankita',
    version=__version__,
    description = 'Well designed MS-Paint like paint program written in PyQt5',
    long_description = readme(),
    long_description_content_type = 'text/markdown',
    keywords = 'pyqt paint',
    url='http://github.com/ksharindam/ankita',
    author='Arindam Chaudhuri',
    author_email='ksharindam@gmail.com',
    license='GNU GPLv3',
    packages=['ankita'],
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Environment :: X11 Applications :: Qt',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.7',
    'Topic :: Multimedia :: Graphics',
    ],
    entry_points={
      'console_scripts': ['ankita=ankita.main:main'],
    },
    data_files=[
             ('share/applications', ['files/ankita.desktop']),
             ('share/icons', ['files/ankita.png'])
    ],
    cmdclass = {'compile' : Build},     # using {'build' : Build} gives error
    include_package_data=True,
    zip_safe=False,
    )
