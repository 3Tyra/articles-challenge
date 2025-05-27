from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        if not title:
            raise ValueError("Title cannot be empty")
        if not isinstance(author_id, int):
            raise ValueError("author_id must be an integer")
        if not isinstance(magazine_id, int):
            raise ValueError("magazine_id must be an integer")

        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("""
                UPDATE articles 
                SET title = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
            """, (self.title, self.author_id, self.magazine_id, self.id))
        else:
            cursor.execute("""
                INSERT INTO articles (title, author_id, magazine_id)
                VALUES (?, ?, ?)
            """, (self.title, self.author_id, self.magazine_id))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @classmethod
    def find_by_id(cls, article_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(row["title"], row["author_id"], row["magazine_id"], row["id"])
        return None

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["title"], row["author_id"], row["magazine_id"], row["id"]) for row in rows]

    def delete(self):
        if not self.id:
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM articles WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
        self.id = None

    def __repr__(self):
        return f"<Article id={self.id} title={self.title!r} author_id={self.author_id} magazine_id={self.magazine_id}>"
