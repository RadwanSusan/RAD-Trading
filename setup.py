# setup.py
from setuptools import setup, find_packages
setup(
    name='RAD-Trading',
    version='0.2.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'MetaTrader5',
        'pandas',
        'numpy',
        'plotly',
        'scikit-learn',
        'scipy',
    ],
    extras_require={
        'dev': [
            'pytest',
            'flake8',
        ],
    },
    author='Radwan Susan',
    author_email='radwansusan90@gmail.com',
    description='A comprehensive trading and backtesting framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/RadwanSusan/RAD-Trading',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
