from setuptools import setup, find_packages

setup(
    name='adding_stats_to_mmcif',
    version='0.1',
    url='https://github.com/berrisfordjohn/adding_stats_to_mmcif',
    author='John Berrisford',
    test_suite='tests',
    zip_safe=True,
    packages=find_packages('adding_stats_to_mmcif'),
    # dependency_links=['https://github.com/project-gemmi/gemmi/tarball/master#egg=gemmi'],
    install_requires=['biopython>=1.72',
                      'requests',
                      'onedep_api>=0.15'
                      ],
)
