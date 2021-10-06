import setuptools

setuptools.setup(
    entry_points={
        'console_scripts': [
            "pe2loaddata=pe2loaddata.__main__:main",
        ],
    },
    extras_require={
        "test":  [
            "pytest>=5.4.3"
        ]
    },
    install_requires=[
        "click>=7.1.2",
        "PyYAML>=5.3.1"
    ],
    name="pe2loaddata",
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    python_requires='>=3.8',
    version="0.1.2"
)
