# -*- coding: utf-8 -*-s
import unittest

from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import sys
sys.path.insert(0, '../')
from sqlalchemy_fulltext import FullText, FullTextSearch


FULLTEXT_TABLE = "test_full_text"
BASE = declarative_base()
ENGINE = create_engine('mysql+mysqldb://foo:bar@localhost/test_fulltext?charset=utf8', echo=False)
SESSION = sessionmaker(bind=ENGINE)()
SESSION.execute('DROP TABLE IF EXISTS {0};'.format(FULLTEXT_TABLE))


class RecipeReviewModel(FullText, BASE):

    __tablename__ = FULLTEXT_TABLE
    # mroonga engine supporting CJK chars
    __table_args__ = {'mysql_engine':'mroonga',
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
        with open('./test_fulltext.json') as fp:
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
        self.assertEqual(full.count(), 3,)
        raw = self.session.execute('SELECT * FROM {0} WHERE MATCH (commentor, review) AGAINST ("spam")'.format(RecipeReviewModel.__tablename__))
        self.assertEqual(full.count(), raw.rowcount, 'Query Test Failed')
    
    def test_fulltext_cjk_query(self):
        cjk = self.session.query(RecipeReviewModel).filter(
                                  FullTextSearch('中国人'.decode('utf8'),
                                                 RecipeReviewModel))
        self.assertEqual(cjk.count(), 2)


if __name__ == '__main__':
    unittest.main()
