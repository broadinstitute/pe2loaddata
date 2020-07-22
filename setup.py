import os.path
import setuptools

setuptools.setup(
    entry_points={
        'console_scripts': [
            "pe2loaddata=pe2loaddata.__main__:main",
        ],
    },
    install_requires=[
        "PyYAML>=5.3.1"
    ],
    name="pe2loaddata",
    package_data={
        "pe2loaddata": [
            os.path.join("data", "*.json")
        ]
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    version="0.1.0"
)