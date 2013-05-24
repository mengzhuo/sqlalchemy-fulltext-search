SQLAlchemy-FullText-Search
==========================

Fulltext search support with MySQL & SQLAlchemy

Quick example:

.. code:: python

    from sqlalchemy_fulltext import FullText, FullTextSearch
    class Foo(FullText, Base):
        __fulltext_columns__ = ('spam', 'ham')

    session.query(Foo).filter(FullTextSearch('Spam', Foo)) 

