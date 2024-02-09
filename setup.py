from setuptools import setup

setup(
    # Whatever arguments you need/want
    # Needed to silence warnings (and to be a worthwhile package)
    name='parserian',
    author='Anatolii Yakushko',
    author_email='shaddyx@gmail.com',
    # Needed to actually package something
    packages=['parserian'],
    package_dir={'parserian':'src/parserian'},
    # Needed for dependencies
    install_requires=[
                      'pytest',
                      ],
    package_data={"": ["*.json"]},
    # *strongly* suggested for sharing
    version='0.05',
    # The license can be anything you like
    license='MIT',
    description='A bunch of tools to help developing parsers',
    include_package_data=True
)
