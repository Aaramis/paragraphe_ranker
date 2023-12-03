from setuptools import setup, find_packages


def parse_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if not line.startswith("#")]


setup(
    name='prg',
    version='0.1',
    description = "Package to perform all the transformation to generate paragraphes",
    url='https://github.com/Aaramis/paragraphe_ranker',
    author='Aramis',
    author_email='auguste.gardette@hotmail.fr',
    license='MIT',
    packages=find_packages(include=['prg']),
    install_requires=parse_requirements('requirements.txt'),
    zip_safe=False,
)

