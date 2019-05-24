import os

from setuptools import setup, find_packages

try:
    here = os.path.abspath(os.path.dirname(__file__))
    README = open(os.path.join(here, "README.md"), encoding="utf-8").read()
    with open(os.path.join(here, "requirements/run.txt"), encoding="utf-8") as f:
        required = [l.strip('\n') for l in f if
                    l.strip('\n') and not l.startswith('#')]
except IOError:
    required = []
    README = ""

setup(
    name="log-analyzer",
    packages=find_packages(),
    version='0.0.2',
    license='GPLv3+',
    description="Log analyzer ",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Amine Ben Asker",
    author_email="ben.asker.amine@gmail.com",
    url="https://github.com/yurilaaziz/log-analyzer",
    download_url='https://github.com/yurilaaziz/log_anaylzer/releases/tag/0.1',
    keywords="Log Analyzer, W3 log, Log Parser",
    install_requires=required,
    entry_points={"console_scripts": ["log-analyzer = log_analyzer.__main__:main"]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
