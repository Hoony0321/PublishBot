from setuptools import setup, find_packages

setup(
    name='notion2velog',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'undetected-chromedriver',
        'notion2md',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'notion2velog=notion2velog.main:main'
        ]
    }
)
