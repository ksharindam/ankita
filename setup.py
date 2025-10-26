from setuptools import setup
from setuptools.command.bdist_wheel import bdist_wheel
from subprocess import check_call


# allows to run commands before building wheel
class BdistWheel(bdist_wheel):
    def finalize_options(self):
        bdist_wheel.finalize_options(self)
        check_call("pyrcc5 -o ./ankita/resources_rc.py ./data/resources.qrc".split())
        check_call("pyuic5 -o ./ankita/ui_mainwindow.py ./data/mainwindow.ui".split())
        check_call("make --directory=lib".split())


setup(
    name='ankita',
    #version=__version__,
    packages=['ankita'],
    entry_points={
        'gui_scripts': ['ankita=ankita.main:main'],
    },
    data_files=[
             ('share/applications', ['data/ankita.desktop']),
             ('share/icons/hicolor/scalable/apps', ['data/ankita.png'])
    ],
    cmdclass = {'bdist_wheel': BdistWheel},
    include_package_data=True,
    zip_safe=False,
    )
