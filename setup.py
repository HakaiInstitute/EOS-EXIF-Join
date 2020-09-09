from setuptools import setup
import os

setup(
    name='joinEOStoEXIF',
    version=os.environ['VERSION'],
    packages=['core'],
    install_requires=['numpy', 'pandas'],
    url='https://github.com/HakaiInstitute/joinEOStoEXIF',
    license='MIT',
    author='Taylor Denouden',
    author_email='taylor.denouden@hakai.org',
    description='Join EOS files to images using EXIF data'
)
