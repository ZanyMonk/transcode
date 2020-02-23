from setuptools import setup

setup(
    name='transcode',
    version='1.0',
    packages=['transcode', 'transcode.commands'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        transcode=transcode.cli:cli
        t=transcode.cli:cli
    '''
)
