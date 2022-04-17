from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='ecutils',
    version='0.0.1.dev0',
    description='Elliptic Curve Utils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/isakruas/ecutils',
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
    keywords='ecutils, ec, ecdh, eck, ecdsa, ecmo',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.8',
    install_requires=[],
    project_urls={
        'Bug Reports': 'https://github.com/isakruas/ecutils/issues',
        'Source': 'https://github.com/isakruas/ecutils/',
    },
)
