import string
from binascii import crc32

def _read_data(filepath):
    with open(filepath, 'r') as f:
        result = []
        for line in f:
            first_space = line.find(' ')
            article_id = line[:first_space]
            text = line[(first_space+1):]
            item = (article_id, text)
            result.append(item)
    return result

def _process_articles(articles):
    _punct_table = str.maketrans(dict.fromkeys(string.punctuation)) # dictionary method fromkeys() creates a new dictionary with keys from seq and values set to value; maketrans creates a Unicode representation of each character for translation.

    def _process_one(x):
        docid, text = x
        return (docid, text.strip() \
                        .translate(_punct_table) \
                        .lower() \
                        .replace(' ', ''))

    return [_process_one(x) for x in articles]

def _shingle_text(text, k):
    shingles = set()
    text = text.strip().lower().replace(' ', '')
    n = len(text)

    for i in range(0, n-k):
        shingle = text[i:(i+k)]
        shingles.add(shingle)
    return shingles

def _shingle_document(text, k):
    shingles = set()
    n = len(text)
    for i in range(0, n-k):
        shingle = text[i:(i+k)]
        hashed_shingle = crc32(shingle.encode('utf-8')) & 0xffffffff
        shingles.add(hashed_shingle)
    return shingles

class ArticleDB:
    def __init__(self, filename):
        self._filename = filename
        self._articles = _read_data(self._filename)
        self._processed_articles = _process_articles(self._articles)
        self._docids = [docid for docid, _ in self._processed_articles]

    def shingle_data(self, k):
        def _shingle_one(x):
            docid, text = x
            sharded_doc = _shingle_document(text, k)
            return (docid, sharded_doc)

        return [_shingle_one(x) for x in self._processed_articles]
