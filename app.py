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
        title = request.form['search']
        return redirect(url_for('search', term=search ))
        
        if title == "dad":
            return redirect(url_for('dad'))  

        else:
            abort(404)
    else:
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
    books = conn.execute('SELECT * FROM books WHERE title LIKE ?',(search_term,)).fetchall()
    conn.close()

    return render_template('search.html', term=search_term, books=books)

#term=term, books=books

@app.errorhandler(404)
def error_404(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug= True)

    


