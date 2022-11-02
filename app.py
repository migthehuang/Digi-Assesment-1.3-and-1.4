from flask import Flask, render_template, request, url_for, redirect, abort
import sqlite3
from datetime import datetime, timedelta


app = Flask(__name__) 

def get_db_connection():
    conn=sqlite3.connect('sqlite/books.sdb')
    conn.row_factory=sqlite3.Row
    return conn

#This is using the books table and is for searching the Database for books only, by title author and date published
@app.route('/', methods = ['POST', 'GET'])
def home():
    
    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('search', term=search ))
        

    return render_template ('home.html')
#not really important anymore          
@app.route('/dad') 
def dad():
    return render_template('dad.html')

#Kinda important
@app.route('/error') 
def error():
    return render_template('error.html')

#very important - where it redirects to after searching in the home page
@app.route('/search/<term>')
def search(term):
    conn = get_db_connection()
    search_term = "%"+term+"%"
    books = conn.execute('SELECT * FROM books WHERE title LIKE ?  or author LIKE ? or date_published like?',(search_term,search_term, search_term)).fetchall()
    conn.commit
    conn.close()
     
    return render_template('search.html', term=term, books=books)

# displays all of the books in the database
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


#adding books, inserts the title, author and date published
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
        return redirect(url_for('data', title=add_title, author=add_author, date_published=add_date_published))

    
    return render_template('add.html')

#deletes a book using the id, in case the same books is added twice, I'll make a thing says you cant add it if it already in the database
@app.route('/delete', methods = ['POST', 'GET'])
def delete():
    if request.method == 'POST':
        rm_book_id = request.form['book_id']
        rm_book_id = [(int(rm_book_id))]

        conn = get_db_connection()
        conn.execute('DELETE from books where idbooks is ?', (rm_book_id))  
        conn.commit()
        conn.close()
        return redirect(url_for('data'))
    return render_template('delete.html')
    
#the hardedt bit so far
@app.route('/borrow/<int:old_book_id>', methods = ['POST', 'GET'])
def borrow(old_book_id):
    book_id=[(int(old_book_id))]
    conn=get_db_connection()
    bookid=conn.execute('SELECT * from books WHERE idbooks is ?',(book_id))
   
    conn.commit()
    conn.close()    

    if request.method == 'POST':
        #for the borrowers part
        borrower_fname = request.form['fname']
        borrower_lname = request.form['lname']
        borrower_email = request.form['email']
        borrower_number = request.form['number'] 
        
        date=datetime.utcnow()
        date_now=datetime.strftime(date,'%B %d %Y - %H:%M:%S')
        conn=get_db_connection()
        borrower_insert=conn.execute('INSERT INTO borrowers (fname,lname,borrower_email,borrower_number) VALUES (?,?,?,?)', (borrower_fname, borrower_lname, borrower_email, borrower_number))
        conn.commit()
        row=conn.execute('SELECT idborrowers FROM borrowers WHERE fname=? AND lname=?',(borrower_fname, borrower_lname))
        borrowers=row.fetchone()   
        idborrowers=borrowers[0]

        borrower_request=conn.execute('INSERT INTO borrowed_books(books_idbooks, borrowers_idborrowers, date_borrowed) VALUES(?,?,?)', (book_id, idborrowers, date_now))
        conn.commit() 

        return redirect(url_for('thankyou', borrower_insert=borrower_insert, borrower_request=borrower_request))


    return render_template('borrow.html', bookid=bookid)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug= True)

    


