from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure the SQL database; here we use SQLite for simplicity.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model for a Book
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_year = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Book {self.title}>"

# Home route (Welcome page)
@app.route('/')
def index():
    return render_template('index.html')

# Route to list all books
@app.route('/books')
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

# Route to add a new book
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        published_year = request.form.get('published_year', type=int)
        new_book = Book(title=title, author=author, published_year=published_year)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('add_book.html')

# Route to display details of a specific book
@app.route('/book/<int:id>')
def book_detail(id):
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html', book=book)

# Route to edit an existing book
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.published_year = request.form.get('published_year', type=int)
        db.session.commit()
        return redirect(url_for('books'))
    return render_template('edit_book.html', book=book)

# Route to delete a book
@app.route('/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('books'))

def seed_books():
    books_data = [
        {'title': '1984', 'author': 'George Orwell', 'published_year': 1949},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'published_year': 1960},
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'published_year': 1925},
        {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'published_year': 1813},
        {'title': 'Moby-Dick', 'author': 'Herman Melville', 'published_year': 1851},
        {'title': 'War and Peace', 'author': 'Leo Tolstoy', 'published_year': 1869},
        {'title': 'The Odyssey', 'author': 'Homer', 'published_year': -750},
        {'title': 'Hamlet', 'author': 'William Shakespeare', 'published_year': 1603},
        {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'published_year': 1951},
        {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'published_year': 1937},
    ]
    for data in books_data:
        book = Book(**data)
        db.session.add(book)
    db.session.commit()

# Make sure this runs once (or check if table is empty) to avoid duplicate entries.
with app.app_context():
    seed_books()

if __name__ == '__main__':
    # Create the database and tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)