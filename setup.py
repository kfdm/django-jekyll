from setuptools import find_packages, setup

setup(
    name='django-jekyll',
    description='Experimental static-ish site',
    author='Paul Traylor',
    packages=find_packages(),
    install_requires=[
        'Django',
        ],
    entry_points={
        'console_scripts': [
            'dekyll = dekyll.manage:main',
        ],
    },
)
