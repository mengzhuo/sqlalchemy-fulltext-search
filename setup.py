"""
SQLAlchemy FullText Search
"""

from setuptools import setup, Command


setup(
        name='SQLAlchemy-FullText-Search',
        version='0.2.1',
        url='https://github.com/mengzhuo/sqlalchemy-fulltext-search',
        license='BSD',
        author='Meng Zhuo, Alejandro Mesa',
        author_email='mengzhuo1203@gmail.com, alejom99@gmail.com',
        description=('Provide FullText for MYSQL & SQLAlchemy model'),
        long_description = __doc__,
        packages=['sqlalchemy_fulltext'],
        zip_safe=False,
        include_package_data=True,
        platforms='any',
        install_requires=['SQLAlchemy>=0.8',],
            classifiers=[
                        'Environment :: Web Environment',
                        'Intended Audience :: Developers',
                        'License :: OSI Approved :: BSD License',
                        'Operating System :: OS Independent',
                        'Programming Language :: Python',
                        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                        'Topic :: Software Development :: Libraries :: Python Modules'            ]
)
