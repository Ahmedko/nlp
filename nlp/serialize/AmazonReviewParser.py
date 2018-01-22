from Document.Document import Document
from serialize.Parser import Parser


class AmazonReviewParser(Parser):
    def read(self, content: str) -> Document:
        """Reads the content of an amazon data file and returns one document instance per document it finds."""
        import json
        documents = []
        # Split lines and loop over them
        # Read json with: data = json.loads(line)
        # Instantiate Document object from "reviewText" and label from "overall"

        with open('Video_Games_5.json') as f:
            for line in f:
                documents= json.loads(line)

        return documents