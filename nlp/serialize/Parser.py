from unittest import TestCase
from Document.Document import Document

class Parser(object):
    """Classe parente pour tous les parsers"""
    def create(self):
        return self

    def read_file(self, filename: str) -> Document:
        with open(filename, 'r', encoding='utf-8') as fp:
            content = fp.read()
        return self.read(content)

class SimpleTextParser(Parser):
    def read(self, content: str) -> Document:
        return Document().create_from_text(content)


class EnglishNerParser(Parser):
    def read(self, content: str) -> Document:
        """Reads the content of a NER/POS data file and returns one document instance per document it finds."""
        documents = []

        # 1. Split the text in documents using string '-DOCSTART- -X- O O' and loop over it
        if documents[0][self._colmap.get('words', 0)] == '-DOCSTART-':
            del documents[0]


        # 2. Slit lines and loop over
            documents = [line.split() for line in documents.split('\n')]
        # 3. Make vectors of tokens and labels (colunn 4) and at the '\n\n' make a sentence

        # 4. Create a Document object


        return documents