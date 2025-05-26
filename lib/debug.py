import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article


author = Author(name="Chinua Achebe")
author.save()


mag = Magazine(name="African Literature", category="Culture")
mag.save()


article = Article(title="The Power of Storytelling", author_id=author.id, magazine_id=mag.id)
article.save()

print("=== Test Data Added ===")
print(f"Author: {author.id} - {author.name}")
print(f"Magazine: {mag.id} - {mag.name} ({mag.category})")
print(f"Article: {article.id} - {article.title}")

print("\n=== Author Articles ===")
for a in author.articles():
    print(f"- {a.title}")

print("\n=== Author Magazines ===")
for m in author.magazines():
    print(f"- {m.name}")

print("\n=== Magazine Articles ===")
for a in mag.articles():
    print(f"- {a.title}")

print("\n=== Magazine Contributors ===")
for c in mag.contributors():
    print(f"- {c.name}")
