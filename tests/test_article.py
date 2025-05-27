import pytest
from lib.models.article import Article
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def clear_tables():
    # Clear tables before each test
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_article_creation_and_saving():
    author = Author(name="Test Author")
    magazine = Magazine(name="Test Mag", category="Test Category")
    author.save()
    magazine.save()

    article = Article(title="Test Article", author_id=author.id, magazine_id=magazine.id)
    article.save()

    assert article.id is not None

def test_article_missing_title():
    with pytest.raises(ValueError):
        Article(title="", author_id=1, magazine_id=1)

def test_article_invalid_author_id():
    with pytest.raises(ValueError):
        Article(title="Invalid", author_id="abc", magazine_id=1)

def test_article_find_by_title():
    author = Author(name="Test Author")
    magazine = Magazine(name="Test Mag", category="Test Category")
    author.save()
    magazine.save()
    article = Article(title="Unique Title", author_id=author.id, magazine_id=magazine.id)
    article.save()

    found = Article.find_by_title("Unique Title")
    assert len(found) == 1
    assert found[0].title == "Unique Title"

def test_article_update_title():
    author = Author(name="Author for Update")
    magazine = Magazine(name="Mag for Update", category="UpdateCat")
    author.save()
    magazine.save()

    article = Article(title="Old Title", author_id=author.id, magazine_id=magazine.id)
    article.save()

    article.title = "New Title"
    article.save()

    fetched = Article.find_by_id(article.id)
    assert fetched.title == "New Title"

def test_article_delete():
    author = Author(name="Author Del")
    magazine = Magazine(name="Mag Del", category="DelCat")
    author.save()
    magazine.save()

    article = Article(title="Delete Me", author_id=author.id, magazine_id=magazine.id)
    article.save()
    article_id = article.id

    article.delete()

    assert article.id is None
    assert Article.find_by_id(article_id) is None
