import setuptools


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setuptools.setup(
    name="fractional_cascading",
    version="1.0",
    author="Nariaki Tateiwa",
    author_email="nariaki3551@gmail.com",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
