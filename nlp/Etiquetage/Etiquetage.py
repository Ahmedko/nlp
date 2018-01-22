from nltk import word_tokenize, pos_tag
text = "There are no secrets to success. It is the result of preparation, hard work, and learning from failure."
tokens = word_tokenize(text)
print(pos_tag(tokens))