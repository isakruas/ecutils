# Installation

The `ecutils` package is a comprehensive toolkit for working with Elliptic Curve Cryptography (ECC) in Python. To get started with `ecutils`, follow the steps below for installation and initial setup.

## Pre-requisites

Make sure you have Python version 3.8 or newer installed on your system. You can download the latest version of Python from the [official Python website](https://www.python.org/downloads/).

## Installation from PyPI

`ecutils` can be easily installed from the Python Package Index (PyPI) using `pip`. Open your terminal or command prompt and execute the following command:

```bash
pip install ecutils
```

This command will download and install the `ecutils` package along with its required dependencies.

## Installation from GitHub Repository

For the latest version or for contributing to the development of `ecutils`, you may want to install directly from the GitHub repository. To do this, follow these steps:

1. Open your terminal or command prompt.
2. Use `git` to clone the repository onto your local machine:

```bash
git clone https://github.com/isakruas/ecutils.git
```

3. Navigate to the cloned repository directory:

```bash
cd ecutils
```

4. Install the package using pip:

```bash
pip install .
```

Alternatively, if you want to install the package in editable mode (which is useful for development), use the following command:

```bash
pip install -e .
```

## Verifying Installation

To verify that `ecutils` has been installed correctly, launch the Python interpreter and attempt to import the module:

```python
import ecutils
```

If there are no errors, the installation was successful.

## Using ECUtils

Once installed, you can start using the `ecutils` package in your Python scripts or projects. Here is an example of how to import a specific module and use it:

```python
from ecutils.algorithms import DigitalSignature

# Continue with the application code
```

For detailed usage instructions, please refer to the provided module documentation or the official documentation available on the `ecutils` [Homepage](https://ecutils.readthedocs.io/en/latest/).

Remember to keep your package updated by periodically running:

```bash
pip install --upgrade ecutils
```

## Support and Contribution

If you encounter any issues or would like to contribute to the `ecutils` project, you can check its [GitHub Repository](https://github.com/isakruas/ecutils) for the source code and contact the maintainers. For reporting bugs, please use the [Bug Tracker](https://github.com/isakruas/ecutils/issues).

Contributions to the project are welcome, and you can submit your changes via pull requests. To get started with contributing, please refer to the [CONTRIBUTING.md](https://github.com/isakruas/ecutils/blob/master/CONTRIBUTING.md) document in the repository.

Enjoy using `ecutils`, a powerful package for Elliptic Curve Cryptography in Python!