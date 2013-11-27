from distutils.core import setup

setup(
    name='smm',
    version='0.2',
    packages=['smm'],
    url='https://github.com/cyhex/smm',
    license='GPLv3',
    author='Timor A.',
    author_email='timor@cyhex.com',
    description='Real-Time, multi-lingual Twitter sentiment analyzer engine',
    install_requires=[
        "tweetstream"
    ],
)
