import sys
import os

# Insert the parent directory at the start of sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article

def main():
    try:
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

        print("=== Data Added ===")
        print(f"{author1.name} wrote '{article1.title}' in {mag1.name}")
        print(f"{author2.name} wrote '{article2.title}' in {mag2.name}")

        print("\nArticles by", author1.name)
        for article in author1.articles():
            print(f"- {article.title}")

        print("\nMagazines featuring", author1.name)
        for mag in author1.magazines():
            print(f"- {mag.name}")

        print("\nContributors to", mag2.name)
        for contributor in mag2.contributors():
            print(f"- {contributor.name}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
