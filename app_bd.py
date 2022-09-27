import json
from flask import Flask, request, jsonify
import sqlite3
import os

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def welcome():
    return "Welcome to mi API conected to my books database"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def get_all():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    select_books = "SELECT * FROM books"
    result = cursor.execute(select_books).fetchall()
    connection.close()
    return jsonify(result)

# 1.Ruta para obtener el conteo de libros por autor ordenados de forma descendente
@app.route('/authors/count/', methods=['GET'])
def count_authors():
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    query = "SELECT author, count(author) FROM books GROUP BY 1 ORDER BY 2 DESC"
    result = cursor.execute(query).fetchall()
    connection.close()
    return jsonify(result)

# 2.Ruta para obtener los libros de un autor como argumento en la llamada
@app.route('/books/', methods = ['GET'])
def filter_author():
    author = '%' + request.args['author'] + '%'
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    query = "SELECT * FROM books WHERE author LIKE ?"
    result = cursor.execute(query, (author,)).fetchall()
    connection.close()
    return jsonify(result)

# 3.Ruta para obtener los libros filtrados por título, publicación y autor
@app.route('/books/filters/', methods = ['GET'])
def filters():
    query = "SELECT * FROM books WHERE"
    to_filter = []
    if 'author' in request.args:
        author = '%' + request.args['author'] + '%'
        query += " author LIKE ? AND"
        to_filter.append(author)
    if 'title' in request.args:
        title = '%' + request.args['title'] + '%'
        query += " title LIKE ? AND"
        to_filter.append(title)
    if 'published' in request.args:
        published = request.args['published']
        query += " published = ? AND"
        to_filter.append(published)
    connection = sqlite3.connect('books.db')
    cursor = connection.cursor()
    query = query[:-4]
    result = cursor.execute(query, to_filter).fetchall()
    connection.close()
    return jsonify(result)

app.run()