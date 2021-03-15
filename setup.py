from setuptools import setup, find_packages

setup(
    name='adding_stats_to_mmcif',
    version='0.5',
    url='https://github.com/berrisfordjohn/adding_stats_to_mmcif',
    author='John Berrisford',
    test_suite='tests',
    zip_safe=True,
    packages=['adding_stats_to_mmcif'],
    install_requires=['biopython>=1.72',
                      'requests',
                      'gemmi'
                      ],
)
