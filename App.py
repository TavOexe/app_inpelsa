from flask import Flask, render_template, request,url_for,redirect,flash
import pypyodbc as inpelsadb


app = Flask(__name__)

DRIVER = 'SQL Server'
SERVER = 'DESKTOP-T3ER55E\SQLEXPRESS'
DATABASE = 'inpelsadb'
#uid = <username>
# pwd = <password>
connection_string = f"""
    DRIVER={{{DRIVER}}};
    SERVER={SERVER};
    DATABASE={DATABASE};
    Trusted_Connection=yes;
"""

conn = inpelsadb.connect(connection_string)
print(conn) 

#settings
app.secret_key = 'mysecret key'


@app.route('/')
def Home():
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts')
    data=cur.fetchall()
    cur.close()
    return render_template('home.html', contacts = data)


@app.route('/addcontact', methods=['POST'])
def addcontact():
    if request.method=='POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (fullname, phone, email) VALUES (?,?,?)", (fullname, phone, email))
        conn.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('Home'))

@app.route('/edit/<id>')
def editcontact(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

#@app.route('/update/<id>', methods = ['POST'])
def updatecontact(id):
    if request.method=='POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = ?,
                phone = ?,
                email = ?
            WHERE id = ?
        """, (fullname, phone, email, id))
        conn.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('Home'))

@app.route('/delete/<string:id>')
def deletecontact(id):
    print(id)
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    conn.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Home'))


@app.route('/search', methods=['POST'])
def search():
    if request.method=='POST':
        search = request.form['search']
        cur = conn.cursor()
        cur.execute("SELECT * FROM contacts WHERE fullname LIKE '%{0}%'".format(search))
        data = cur.fetchall()
        return render_template('home.html', contacts = data)

@app.route('/contactdetails/<string:id>')
def contactdetails(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('contact-details.html', contact = data[0])



if __name__ == '__main__':
    app.run(port=5000, debug=True)



