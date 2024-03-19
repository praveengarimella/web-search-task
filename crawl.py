class Indexer:
    # Inverted index (words -> document URLs)
    def __init__(self):
        self.inverted_index = defaultdict(list)
        # Stop words from NLTK (assumed imported)
        self.stop_words = set(stopwords.words('english'))

    # Clean and normalize text (lowercase, alnum, remove stop words)
    def process_text(self, text):
        words = word_tokenize(text)
        words = [word.lower() for word in words if word.isalnum() and word.lower() not in self.stop_words]
        return words

    # Build index from text, optionally associate URL
    def build_index_from_text(self, text, url=None):
        words = self.process_text(text)
        for word in words:
            self.inverted_index[word].append(url)

    # Get the built inverted index
    def get_index(self):
        return self.inverted_index
