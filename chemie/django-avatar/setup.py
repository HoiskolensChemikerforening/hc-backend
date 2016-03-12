import codecs
import re
from os import path
from setuptools import setup, find_packages


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='django-avatar',
    version=find_version("avatar", "__init__.py"),
    description="A Django app for handling user avatars",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='avatar, django',
    author='Eric Florenzano',
    author_email='floguy@gmail.com',
    maintainer='Grant McConnaughey',
    maintainer_email='grantmcconnaughey@gmail.com',
    url='http://github.com/grantmcconnaughey/django-avatar/',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    package_data={
        'avatar': [
            'templates/notification/*/*.*',
            'templates/avatar/*.html',
            'locale/*/LC_MESSAGES/*',
            'media/avatar/img/default.jpg',
        ],
    },
    install_requires=[
        'Pillow>=2.0',
        'django-appconf>=0.6',
    ],
    zip_safe=False,
)
