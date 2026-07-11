from setuptools import setup, find_packages

setup(
    name="kryon",
    version="0.0.1",
    description="A modern systems programming language focused on safety and concurrency.",
    author="Kryon Team",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        'console_scripts': [
            'kryon=kryon.cli:main',
        ],
    },
)
