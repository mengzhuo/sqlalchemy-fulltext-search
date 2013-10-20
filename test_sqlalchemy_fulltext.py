#!/usr/bin/env python
# -*- coding: utf-8 -*-s
import unittest

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy_fulltext import FullText, FullTextSearch


FULLTEXT_TABLE = "test_full_text"
BASE = declarative_base()
ENGINE = create_engine('mysql+mysqldb://travis@localhost/test_full_text?charset=utf8', echo=True)
SESSION = sessionmaker(bind=ENGINE)()
SESSION.execute('DROP TABLE IF EXISTS {0};'.format(FULLTEXT_TABLE))

MYSQL_ENGINES = [i[0] for i in SESSION.execute('SHOW ENGINES;').fetchall()
                if i[1] == "YES"]
MYSQL_VERSION = SESSION.execute('SHOW VARIABLES LIKE "version";').fetchone()[1]

class RecipeReviewModel(FullText, BASE):

    __tablename__ = FULLTEXT_TABLE
    # mroonga engine supporting CJK chars
    __table_args__ = {'mysql_engine':'MyISAM',
                      'mysql_charset':'utf8'}
    
    __fulltext_columns__ = ('commentor','review')

    id        = Column(Integer,primary_key=True)
    commentor = Column(String(length=100))
    review    = Column(Text())

    def __init__(self, commentor, review):
        self.review = review
        self.commentor = commentor

class TestSQLAlchemyFullText(unittest.TestCase):

    def setUp(self):
        self.base = BASE
        self.engine = ENGINE
        self.session = SESSION


        self.entries = []

    def test_fulltext_abuild(self):
        self.assertIsNone(self.base.metadata.create_all(self.engine))

    def test_fulltext_add(self):
        import json
        with open('test_fulltext.json') as fp:
            bulk = json.load(fp)
            for entry in bulk:
                self.entries.append(RecipeReviewModel(
                                entry['commentor'],
                                entry['review']))

        for entry in self.entries:
            self.assertIsNone( self.session.add(entry))
        self.session.commit()
    def test_fulltext_form_query(self):
        FullTextSearch('spam', RecipeReviewModel)

    def test_fulltext_query(self):
        full = self.session.query(RecipeReviewModel).filter(FullTextSearch('spam', RecipeReviewModel))
        self.assertEqual(full.count(), 2,)
        raw = self.session.execute('SELECT * FROM {0} WHERE MATCH (commentor, review) AGAINST ("spam")'.format(RecipeReviewModel.__tablename__))
        self.assertEqual(full.count(), raw.rowcount, 'Query Test Failed')
   
    @unittest.skipIf(not 'mroonga' in MYSQL_ENGINES, 'mroonga engines not available')
    def test_fulltext_cjk_query(self):
        cjk = self.session.query(RecipeReviewModel).filter(
                                  FullTextSearch('中国人'.decode('utf8'),
                                                 RecipeReviewModel))
        self.assertEqual(cjk.count(), 2)


if __name__ == '__main__':
    unittest.main()
