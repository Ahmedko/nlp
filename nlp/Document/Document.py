import re
from typing import List

import nltk

from Document.Token import Sentence
from Document.Token import Token
from Document.Interval import Interval

def get_shape_category(token):
    if re.match('^[\n]+$', token):  # IS LINE BREAK
        return 'NL'
    if any(char.isdigit() for char in token) and re.match('^[0-9.,]+$', token):  # IS NUMBER (E.G., 2, 2.000)
        return 'NUMBER'
    if re.fullmatch('[^A-Za-z0-9\t\n ]+', token):  # IS SPECIAL CHARS (E.G., $, #, ., *)
        return 'SPECIAL'
    if re.fullmatch('^[A-Z\-.]+$', token):  # IS UPPERCASE (E.G., AGREEMENT, INC.)
        return 'ALL-CAPS'
    if re.fullmatch('^[A-Z][a-z\-.]+$', token):  # FIRST LETTER UPPERCASE (E.G. This, Agreement)
        return '1ST-CAP'
    if re.fullmatch('^[a-z\-.]+$', token):  # IS LOWERCASE (E.G., may, third-party)
        return 'LOWER'
    if not token.isupper() and not token.islower():  # WEIRD CASE (E.G., 3RD, E2, iPhone)
        return 'MISC'
    return 'MISC'

class Document:
    """
    A document is a combination of text and the positions of the tags and elements in that text.
    """

    def __init__(self):
        self.text = None
        self.tokens = None
        self.sentences = None

    @classmethod
    def create_from_text(cls, text: str = None):
        """
        :param text: document text as a string
        """
        doc = Document()
        doc.text = text
        # TODO: To be implemented
        # 1. Tokenize texte (tokens & phrases)
        words, pos_tags = zip(*nltk.pos_tag(nltk.word_tokenize(text)))
        sentences = nltk.sent_tokenize(text.replace('\n', ' '))
        # 2. Corriger la tokenisation (retokenize)
        #words, pos_tags = Document._retokenize(words, pos_tags)
        # 3. Trouver les intervalles de Tokens
        doc.tokens = Document._find_tokens(doc, words, pos_tags, text)
        # 4. Trouver les intervalles de phrases
        doc.sentences = Document._find_sentences(doc, sentences, text)

        return doc

    @staticmethod
    def _retokenize(word_tokens: List[str], pos_tags: List[str]):
        """
        Correct NLTK tokenization. We separate symbols from words, such as quotes, -, *, etc
        :param word_tokens: list of strings(tokens) coming out of nltk.word_tokenize
        :param pos_tags:  list of strings(pos tag) coming out of nltk.pos_tag
        :return: new list of tokens
        """
        split_ends = re.escape('-*·')
        split_always = re.escape('’`"\'“”/\\')
        # declare new lists
        for token, pos in zip(word_tokens, pos_tags):
            split_tokens = re.split('([' + split_always + ']+)|(\n)|(^[' + split_ends + '])|([' + split_ends + ']$)',
                                    token)
            split_tokens = [t for t in split_tokens if t is not None and t != '']
            # extend new token list
            # find new pos tags, extend pos tag list
            # return new lists

    @staticmethod
    def _find_tokens(doc, word_tokens, pos_tags, text):
        """ Calculate the span of each token, find which element it belongs to and create a new Token instance
            :param doc: Reference to documents instance
            :param word_Tokens:  list of strings(tokens) coming out of nltk.word_tokenize
            :param pos_tags:  list of strings(pos tag) coming out of nltk.pos_tag
            :return: list of tokens as Token class
         """
        offset = 0
        tokens = []
        missing = None
        for token, pos_tag in zip(word_tokens, pos_tags):
            # Traiter le changement de ligne '\n' avec pos tag 'NL'
            pos = text.find(token, offset, offset + max(30, len(token)))
            if pos > -1:
                tokens.append(Token(doc,pos,pos+len(token),pos_tag, get_shape_category(token), token))
                offset=pos+len(token)
        return  tokens

    @staticmethod
    def _find_sentences(doc, sentences, text: str):
        """ yield Sentence objects each time a sentence is found in the text """
        sentence_objects = []
        offset = 0
        for sentence in sentences:
            # Traiter le changement de ligne '\n' avec pos tag 'NL'
            pos = text.find(sentence, offset)
            if pos > -1:
                sentence_objects.append(Sentence(doc, pos, pos + len(sentence)))
                offset = pos + len(sentence)

        return sentence_objects

    @classmethod
    def create_from_vectors(cls, words: List[str], sentences: List[Interval] = None, labels: List[str] = None):
        doc = Document()
        text = []
        offset = 0
        doc.sentences = []
        for sentence in sentences:
            text.append(' '.join(words[sentence.start:sentence.end + 1]) + ' ')
            doc.sentences.append(Interval(offset, offset + len(text[-1])))
            offset += len(text[-1])
        doc.text = ''.join(text)

        offset = 0
        doc.tokens = []
        for word, label in zip(words, labels):
            pos = doc.text.find(word, offset)
            if pos >= 0:
                offset = pos + len(word)
                doc.tokens.append(Token(doc, pos, offset, None, get_shape_category(word), word, label=label))
        return doc