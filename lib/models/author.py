from lib.db.connection import get_connection

class Author:
    def __init__(self, name: str, id: int = None):
        if not name:
            raise ValueError("Name cannot be empty")
        self.id = id
        self.name = name

    def save(self) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self.name, self.id))
        else:
            cursor.execute("INSERT INTO authors (name) VALUES (?)", (self.name,))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row["name"], row["id"]) if row else None

    @classmethod
    def find_by_name(cls, name: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(row["name"], row["id"]) if row else None

    def articles(self):
        from .article import Article
        return Article.find_by_author(self.id)

    def magazines(self):
        from .magazine import Magazine
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row["name"], row["category"], row["id"]) for row in rows]

    def add_article(self, magazine, title: str):
        from .article import Article
        article = Article(title=title, author_id=self.id, magazine_id=magazine.id)
        article.save()
        return article

    def topic_areas(self):
        return list(set([m.category for m in self.magazines()]))

    def __repr__(self):
        return f"<Author id={self.id} name={self.name!r}>"

    def __eq__(self, other):
        if isinstance(other, Author):
            return self.id == other.id and self.name == other.name
        return False

    def __hash__(self):
        return hash((self.id, self.name))
