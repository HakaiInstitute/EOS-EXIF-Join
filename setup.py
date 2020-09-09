from setuptools import setup
import os

setup(
    name='join_eos_exif',
    version=os.environ['VERSION'],
    packages=['join_eos_exif'],
    install_requires=['numpy', 'pandas'],
    url='https://github.com/HakaiInstitute/join-eos-exif',
    license='MIT',
    author='Taylor Denouden',
    author_email='taylor.denouden@hakai.org',
    description='Join EOS files to images using EXIF data'
)
