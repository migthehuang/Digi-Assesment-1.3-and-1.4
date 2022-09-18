from turtle import title
from flask import Flask, render_template, request, url_for, redirect, abort
import sqlite3

app = Flask(__name__) 

def get_db_connection():
    conn=sqlite3.connect('sqlite/books.sdb')
    conn.row_factory=sqlite3.Row
    return conn

@app.route('/', methods = ['POST', 'GET'])
def home():
    
    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('search', term=search ))
        
        
    return render_template ('home.html')
            


@app.route('/dad') 
def dad():
    return render_template('dad.html')

@app.route('/error') 
def error():
    return render_template('error.html')

@app.route('/search/<term>')
def search(term):
    conn = get_db_connection()
    search_term = "%"+term+"%"
    books = conn.execute('SELECT * FROM books WHERE title LIKE ?  or author LIKE ? or date_published like?',(search_term,search_term, search_term)).fetchall()
    conn.close()
     
    return render_template('search.html', term=term, books=books)


@app.route('/data')
def data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM books').fetchall()
    print(len(data))
    conn.close()
    #add_title = "%"+title+"%"
    #add_author = "%"+author+"%"
    #add_date_published = "%"+date_published+"%"
    #conn.execute('INSERT INTO books (title, author, date_published)', 'VALUES (?,?,?)'), (add_title, add_author, add_date_published)
    return render_template('data.html', datas=data)

@app.route('/hello')
def hello():
    return render_template('add.html')



@app.route('/add', methods = ['POST', 'GET'])
def add():
    #if request.method == 'POST':
        #title = request.form['title']
        #author = request.form['author']
        #date_published = request.form['date_published']
        #return redirect(url_for('data', title=title, author=author, date_published=date_published))
    #conn = get_db_connection()
    
    #conn.close()
    
    return render_template('add.html')
    
    #title=add_title, author=add_author, date_published=add_date_published)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug= True)

    


