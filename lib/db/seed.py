# seed.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib')))

from models.author import Author
from models.magazine import Magazine
from models.article import Article

def seed():
    author1 = Author(name="Ngũgĩ wa Thiong’o")
    author2 = Author(name="Wole Soyinka")
    author1.save()
    author2.save()

    mag1 = Magazine(name="Pan African Voice", category="Politics")
    mag2 = Magazine(name="Lit & Verse", category="Literature")
    mag1.save()
    mag2.save()

    article1 = Article(title="Writing for Freedom", author_id=author1.id, magazine_id=mag1.id)
    article2 = Article(title="The Drama of Language", author_id=author2.id, magazine_id=mag2.id)
    article1.save()
    article2.save()

    return {
        "authors": [author1, author2],
        "magazines": [mag1, mag2],
        "articles": [article1, article2],
    }

if __name__ == "__main__":
    seed()

