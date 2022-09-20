from flask import Flask, render_template, request, url_for, redirect, abort
import sqlite3

app = Flask(__name__) 

def get_db_connection():
    conn=sqlite3.connect('sqlite/books.sdb')
    conn.row_factory=sqlite3.Row
    return conn

#This is using the books table and is for searching the Database for books only. 
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
    
    
    return render_template('data.html', datas=data)

@app.route('/hello')
def hello():
    return render_template('add.html')



@app.route('/add', methods = ['POST', 'GET'])
def add():
    if request.method == 'POST':
        add_title = request.form['title']
        add_author = request.form['author']
        add_date_published = request.form['date_published']

        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, date_published) VALUES (?,?,?)', (add_title, add_author, add_date_published))   
        conn.commit()
        conn.close()
        return redirect(url_for('data', title=add_title, author=add_author, date_published=add_date_published, add=add))

    
    return render_template('add.html')

@app.route('/delete', methods = ['POST', 'GET'])
def delete():
    if request.method == 'POST':
        rm_title = request.form['rm_title']
        rm_author = request.form['rm_author']
        rm_date_published = request.form['rm_date_published']

        conn = get_db_connection()
        conn.execute('DELETE from books WHERE title like ? or author like ? or date_published like ?', (rm_title, rm_author, rm_date_published))   
        conn.commit()
        conn.close()
        return redirect(url_for('data', title=rm_title, author=rm_author, date_published=rm_date_published))
    return render_template('delete.html')
    
@app.route('/borrow/<int:book_id>', methods = ['POST', 'GET'])
def borrow(book_id):

    conn=get_db_connection()
    conn.execute('SELECT * from books WHERE idbooks is ?',(int(book_id)))
    conn.commit()
    conn.close()
    return render_template('borrow.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug= True)

    


