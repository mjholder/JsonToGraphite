from setuptools import setup

setup(
    name='JsonToCarbon',
    version='1.0',
    packages=['JsonToCarbon'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'JsonToCarbon = JsonToCarbon.__main__:main'
        ]
    }
)
