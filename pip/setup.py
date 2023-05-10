from setuptools import find_packages, setup

setup(
    name="PhageOrder",
    version="0.0.2",
    description="Python package used to reorder and annotate phage genomes.",
    url="https://github.com/JoshuaIszatt",
    author="Joshua Iszatt",
    author_email="joshiszatt@gmail.com",
    license="AGPL-3.0",
    install_requires=[""],
    python_requires=">3",
    packages=find_packages(),
    data_files=[("", ["LICENSE.md", "README.md"])],
    entry_points={
        'console_scripts': [
            'phage-order.py = PhageOrder.main:main',
        ],
    },
)