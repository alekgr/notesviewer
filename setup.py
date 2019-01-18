from setuptools import setup

setup(
    name='notesviewer',
    version='1.0.0-99',
    description='notesviewer',
    py_modules=["noteviewer"],
    package_dir={'': 'src'},
    license='GPL',
    author='alekgr',
    author_email='alek.grigorian@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/Alekgr/notesviewer.git'
)
