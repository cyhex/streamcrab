from setuptools import setup, find_packages

setup(
    name='smm',
    version='0.2',
    packages=['smm'],
    url='https://github.com/cyhex/streamcrab',
    license='GPLv3',
    author='Timor A.',
    author_email='timor@cyhex.com',
    description='Real-Time, multi-lingual Twitter sentiment analyzer engine',
    install_requires=[
        "requests",
        "requests_oauthlib",
        "mongoengine",
        "nltk",
        'numpy',
        'gevent',
        'gevent-socketio',
        'flask',
        'argcomplete'
    ],
)
