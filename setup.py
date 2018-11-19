from setuptools import setup

setup(
    name='efs-cli',
    version='0.1',
    py_modules=['app'],
    install_requires=[
        'Click',
        'arcgis',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        efs-cli=app:cli
    ''',
)