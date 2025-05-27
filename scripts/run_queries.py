import sqlite3

def run_query(query, params=()):
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == '__main__':
   
    query = "SELECT * FROM authors"
    authors = run_query(query)
    for author in authors:
        print(dict(author))

   