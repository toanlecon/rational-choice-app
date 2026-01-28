from setuptools import setup, find_packages

setup(
    name="rational_choice_app",
    version="1.0.0",
    description="A Game Theory visualization tool for Pearce's Lemma",
    packages=find_packages(),
    # THIS SECTION IS CRITICAL:
    install_requires=[
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0"
    ],
    entry_points={
        'console_scripts': [
            'rational-choice=rational_choice_app.main:main',
        ],
    },
)
