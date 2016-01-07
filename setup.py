##
## Installtion of the USS
##

from setuptools import setup,find_packages

setup(
    name="uss",
    author="Vladimir Ulogov",
    author_email="vladimir.ulogov@zabbix.com",
    license="GNU GPLv2",
    description="uss",
    long_description="USS Framework",
    version="0.1",
    url="https://github.com/vulogov/uss",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    package_dir = {'':'lib'},
    packages=find_packages('lib'),
    scripts=[],
    data_files=[
    ],
    install_requires=[
        "daemonize >= 2.4.2",
        "numpy >= 1.4.1",
        "redis >= 2.0.0",
        "simplejson >= 2.0.9",
        "pyclips >= 1.0.7",
        "sysv_ipc >= 0.6.8"
    ]
    )