from lib.db.connection import get_connection

class Magazine:
    def __init__(self, name: str, category: str, id: int = None):
        if not name or not category:
            raise ValueError("Name and category cannot be empty")
        self.id = id
        self.name = name
        self.category = category

    def save(self) -> None:
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )
        else:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?)",
                (self.name, self.category)
            )
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, id: int):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row["name"], row["category"], row["id"]) if row else None

    def articles(self):
        from .article import Article
        return Article.find_by_magazine(self.id)

    def contributors(self):
        from .author import Author
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["name"], row["id"]) for row in rows]

    def article_titles(self):
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        authors = self.contributors()
        result = []
        for author in authors:
            articles_in_magazine = [a for a in author.articles() if a.magazine_id == self.id]
            if len(articles_in_magazine) > 2:
                result.append(author)
        return result

    def __repr__(self):
        return f"<Magazine id={self.id} name={self.name!r} category={self.category!r}>"
