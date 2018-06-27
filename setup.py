from setuptools import setup, find_packages

setup(
    name='adding_stats_to_mmcif',
    version='0.1',
    url='https://github.com/berrisfordjohn/adding_stats_to_mmcif',
    author='John Berrisford',
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False,
    packages=find_packages('src'),
    #install_requires=['unittest', 'logging', 'xml', 'os'], 
)