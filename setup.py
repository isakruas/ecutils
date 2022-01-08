from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ecc',
    version='0.0.1.dev6',
    description='Elliptic Curve Cryptography',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/isakruas/ecc',
    author='Isak Paulo de Andrade Ruas',
    license='MIT',
    author_email='isakruas@gmail.com',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='ecc, elliptic curve, cryptography, elliptic curve cryptography',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=[],
    project_urls={
        'Bug Reports': 'https://github.com/isakruas/ecc/issues',
        'Source': 'https://github.com/isakruas/ecc/',
    },
)
