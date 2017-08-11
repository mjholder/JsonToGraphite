from setuptools import setup

setup(
    name='JsonToGraphite',
    version='1.0',
    packages=['JsonToGraphite'],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'JsonToGraphite = JsonToGraphite.__main__:main'
        ]
    }
)
