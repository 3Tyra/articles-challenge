import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.models.article import Article
from lib.db.connection import get_connection

@pytest.fixture(autouse=True)
def clear_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    cursor.execute("DELETE FROM authors")
    cursor.execute("DELETE FROM magazines")
    conn.commit()
    conn.close()

def test_magazine_creation_and_saving():
    mag = Magazine(name="Test Magazine", category="Test Category")
    mag.save()
    assert mag.id is not None

def test_find_by_id():
    mag = Magazine(name="FindMe", category="TestCat")
    mag.save()

    fetched = Magazine.find_by_id(mag.id)
    assert fetched is not None
    assert fetched.name == "FindMe"

def test_articles_and_contributors_methods():
    author = Author(name="Author 1")
    author.save()
    mag = Magazine(name="Mag 1", category="Category 1")
    mag.save()
    article = Article(title="Title 1", author_id=author.id, magazine_id=mag.id)
    article.save()

    assert len(mag.articles()) == 1
    assert author in mag.contributors()
    assert "Title 1" in mag.article_titles()

def test_article_titles_method():
    mag = Magazine(name="Mag Titles", category="Cat")
    mag.save()
    assert mag.article_titles() == []

def test_contributing_authors_method():
    author = Author(name="Author 1")
    author.save()
    mag = Magazine(name="Mag 1", category="Category 1")
    mag.save()

    # Create 3 articles for author in this magazine (more than 2)
    for i in range(3):
        article = Article(title=f"Article {i+1}", author_id=author.id, magazine_id=mag.id)
        article.save()

    contributing_authors = mag.contributing_authors()
    assert any(a.id == author.id for a in contributing_authors)

def test_magazine_empty_name_or_category():
    with pytest.raises(Exception):
        Magazine(name="", category="Tech")
    with pytest.raises(Exception):
        Magazine(name="Tech Mag", category="")

def test_magazine_update_category():
    mag = Magazine(name="Old Mag", category="OldCat")
    mag.save()

    mag.category = "NewCat"
    mag.save()

    fetched = Magazine.find_by_id(mag.id)
    assert fetched.category == "NewCat"
