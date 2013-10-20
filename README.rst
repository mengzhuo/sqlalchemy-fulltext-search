SQLAlchemy-FullText-Search
==========================

.. image:: https://travis-ci.org/mengzhuo/sqlalchemy-fulltext-search.png?branch=master

Fulltext search support with MySQL & SQLAlchemy

Examples:

Default 

.. code:: python

    from sqlalchemy_fulltext import FullText, FullTextSearch
    class Foo(FullText, Base):
        __fulltext_columns__ = ('spam', 'ham')

    session.query(Foo).filter(FullTextSearch('Spam', Foo)) 

Using "IN BOOLEAN MODE":

.. code:: python

    from sqlalchemy_fulltext import FullText, FullTextSearch
    import sqlalchemy_fulltext.modes as FullTextMode
    class Foo(FullText, Base):
        __fulltext_columns__ = ('spam', 'ham')

    session.query(Foo).filter(FullTextSearch('Spa*', Foo, FullTextMode.BOOLEAN))

Using "IN NATURAL LANGUAGE MODE":

.. code:: python

    from sqlalchemy_fulltext import FullText, FullTextSearch
    import sqlalchemy_fulltext.modes as FullTextMode
    class Foo(FullText, Base):
        __fulltext_columns__ = ('spam', 'ham')

    session.query(Foo).filter(FullTextSearch('Spam', Foo, FullTextMode.NATURAL))

Using "WITH QUERY EXPANSION"

.. code:: python

    from sqlalchemy_fulltext import FullText, FullTextSearch
    import sqlalchemy_fulltext.modes as FullTextMode
    class Foo(FullText, Base):
        __fulltext_columns__ = ('spam', 'ham')

    session.query(Foo).filter(FullTextSearch('Spam', Foo, FullTextMode.QUERY_EXPANSION))
