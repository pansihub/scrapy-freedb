from setuptools import setup, find_packages

setup(
    version='0.1.0',
    name='scrapy-freedb',
    description='scrapy freedb plugin',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'scrapy.plugin': [
            'scrapy-freedb = scrapy_freedb.plugin:Plugin',
        ],
    },
    install_requires=[
        'requests',
    ],
)
