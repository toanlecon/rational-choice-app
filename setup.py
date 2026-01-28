from setuptools import setup, find_packages

setup(
    name="rational_choice_app",
    version="1.0.0",
    description="A Game Theory visualization tool for Pearce's Lemma",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib"
    ],
    entry_points={
        'console_scripts': [
            'rational-choice=rational_choice_app.main:main',
        ],
    },
)
