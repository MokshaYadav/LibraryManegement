import sqlite3
from datetime import datetime
import difflib

DB_NAME = "library.db"

# ------------------ Database Setup ------------------
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            added_date TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database ready.")

# ------------------ Add Book ------------------
def add_book(title, author, year, genre):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO books (title, author, year, genre, added_date) VALUES (?, ?, ?, ?, ?)",
                   (title, author, year, genre, added_date))
    conn.commit()
    conn.close()
    print(f"✅ Book '{title}' added.")

#Multiple books
def add_books_interactively():
    books = []
    while True:
        print("\nEnter details for a new book:")
        title = input("Title: ")
        author = input("Author: ")
        year = input("Year: ")
        genre = input("Genre: ")

        # Validate year input
        try:
            year = int(year)
        except ValueError:
            print("❌ Invalid year entered. Please enter a number.")
            continue

        books.append((title, author, year, genre))

        cont = input("Add another book? (y/n): ").strip().lower()
        if cont != 'y':
            break

    for book in books:
        add_book(*book)

    print(f"\n✅ Added {len(books)} books successfully!")




# ------------------ View All Books ------------------
def view_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY id DESC")
    books = cursor.fetchall()
    conn.close()

    if books:
        print("\n📚 Library Collection:")
        print("-" * 60)
        for book in books:
            print(f"[{book[0]}] {book[1]} by {book[2]} ({book[3]}) - Genre: {book[4]}, Added: {book[5]}")
        print("-" * 60)
    else:
        print("📭 No books in the library.")

# ------------------ Search Books ------------------
def search_books(keyword):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    books = cursor.fetchall()
    conn.close()

    if books:
        print(f"\n🔍 Search Results for '{keyword}':")
        print("-" * 60)
        for book in books:
            print(f"[{book[0]}] {book[1]} by {book[2]} ({book[3]}) - Genre: {book[4]}, Added: {book[5]}")
        print("-" * 60)
    else:
        print("❌ No matching books found.")

 # ------------------ Delete Book ------------------
def delete_book(book_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()

    if book:
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        print(f"✅ Book with ID {book_id} deleted successfully.")
    else:
        print(f"❌ No book found with ID {book_id}.")

    conn.close()


# ------------------ AI Recommendation ------------------
def recommend_books(search_title):
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    # Check if 'added_date' column exists in the table
    cursor.execute("PRAGMA table_info(books)")
    columns = [col[1] for col in cursor.fetchall()]
    has_added_date = "added_date" in columns

    # Select query depending on available columns
    if has_added_date:
        cursor.execute("SELECT id, title, author, year, genre, added_date FROM books")
    else:
        cursor.execute("SELECT id, title, author, year, genre FROM books")

    books = cursor.fetchall()
    conn.close()

    if not books:
        print("📭 No books available for recommendation.")
        return

    # Basic AI: Recommend books with similar words in title or genre
    recommendations = []
    for book in books:
        if search_title.lower() in book[1].lower() or search_title.lower() in book[4].lower():
            recommendations.append(book)

    print("\n🤖 AI Recommendations:")
    print("-" * 60)
    if recommendations:
        for book in recommendations:
            if has_added_date:
                print(f"[{book[0]}] {book[1]} by {book[2]} ({book[3]}) - Genre: {book[4]}, Added: {book[5]}")
            else:
                print(f"[{book[0]}] {book[1]} by {book[2]} ({book[3]}) - Genre: {book[4]}")
    else:
        print("No similar books found.")
    print("-" * 60)



#UPDATE DATABASE
def update_database_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE books ADD COLUMN added_date TEXT")
        print("✅ Database schema updated: 'added_date' column added.")
    except sqlite3.OperationalError:
        print("⚠️ 'added_date' column already exists or cannot be added.")
    conn.commit()
    conn.close()    

# ------------------ Main Menu ------------------
def main():
    create_table()
    while True:
        print("\n📌 Library Menu:")
        print("1. Add Book")
        print("2. Interactive Bulk Add Books")
        print("3. View All Books")
        print("4. Search Books")
        print("5. Delete a Book")                   # New option added here
        print("6. AI Book Recommendations")
        print("7. Update Database Schema (Add Columns)")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            year = input("Enter publication year: ")
            genre = input("Enter genre: ")
            add_book(title, author, year, genre)

        elif choice == "2":
            add_books_interactively()

        elif choice == "3":
            view_books()

        elif choice == "4":
            keyword = input("Enter search keyword: ")
            search_books(keyword)

        elif choice == "5":
            book_id = input("Enter the ID of the book to delete: ")
            if book_id.isdigit():
                delete_book(int(book_id))
            else:
                print("❌ Invalid ID. Please enter a numeric ID.")

        elif choice == "6":
            search_title = input("Enter book title for recommendations: ")
            recommend_books(search_title)

        elif choice == "7":
            update_database_schema()

        elif choice == "8":
            print("📕 Exiting Library Management. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")


   
if __name__ == "__main__":
    main()

    
