import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
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

def test_author_creation():
    author = Author(name="Test Author")
    author.save()
    assert author.id is not None

def test_author_empty_name():
    with pytest.raises(ValueError):
        Author(name="")

def test_author_update_name():
    author = Author(name="Initial Name")
    author.save()

    author.name = "Updated Name"
    author.save()

    fetched = Author.find_by_id(author.id)
    assert fetched.name == "Updated Name"

def test_author_topic_areas():
    author = Author(name="Topic Tester")
    author.save()
    mag1 = Magazine(name="Mag1", category="Science")
    mag2 = Magazine(name="Mag2", category="Art")
    mag1.save()
    mag2.save()
    author.add_article(mag1, "Science Article")
    author.add_article(mag2, "Art Article")

    topics = author.topic_areas()
    assert "Science" in topics
    assert "Art" in topics
    assert len(topics) == 2
