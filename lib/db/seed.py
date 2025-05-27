from lib.db.connection import get_connection

def run_schema():
    conn = get_connection()
    with open('lib/db/schema.sql', 'r') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.close()

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    # Insert sample authors
    authors = [
        ('Jane Doe',),
        ('John Smith',),
        ('Alice Johnson',)
    ]
    cursor.executemany("INSERT INTO authors (name) VALUES (?)", authors)

    # Insert sample magazines
    magazines = [
        ('Tech Today', 'Technology'),
        ('Health Weekly', 'Health'),
        ('Fashion Forward', 'Fashion')
    ]
    cursor.executemany("INSERT INTO magazines (name, category) VALUES (?, ?)", magazines)

    # Insert sample articles
    articles = [
        ('AI Innovations', 1, 1),  # title, author_id, magazine_id
        ('Wellness Tips', 2, 2),
        ('Summer Trends', 3, 3),
        ('Future of Tech', 1, 1),
        ('Healthy Eating', 2, 2),
    ]
    cursor.executemany(
        "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", articles
    )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_schema()
    seed_data()
    print("Database seeded successfully!")
