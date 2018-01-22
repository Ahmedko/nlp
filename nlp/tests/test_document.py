from unittest import TestCase
from Document.Document import Document
import os
from Data import DATA_DIR

class TestDocument(TestCase):

    def test_create_from_text(self):
        text = 'Hello world. Hello France.'
        doc =Document.create_from_text(text)
        self.assertEquals(len(doc.tokens),6,'erreur sur document')
        self.assertEquals(len(doc.sentences),0,'erreur')


        filename = os.path.join(DATA_DIR, "test.txt")


