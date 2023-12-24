from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['WEATHER_API_KEY'] = 'cfde192246d556e8dd2f996af0c12527'

app.config['MYSQL_HOST'] = 'amatdeska.mysql.pythonanywhere-services.com' #amatdeska.mysql.pythonanywhere-services.com
app.config['MYSQL_USER'] = 'amatdeska' #amatdeska
app.config['MYSQL_PASSWORD'] = 'RAPTOR18!' #RAPTOR18!
app.config['MYSQL_DB'] = 'amatdeska$task' #amatdeska$task

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
# def home():
#     return render_template('index.html')

def home():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()

        if user and 'password' in user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
            session['username'] = username
            return redirect(url_for('dash'))
        else:
            # Opsi 1: Menampilkan pesan kesalahan
            return render_template('dash.html', error='Invalid username or password')

            # Opsi 2: Mengarahkan kembali ke halaman login
            # return redirect(url_for('login'))

    return render_template('index.html')

    
@app.route('/regis' , methods=['GET', 'POST'])
# def regis():
#     return render_template('regis.html')

def regis():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO user (username, email, password) VALUES (%s, %s, %s)', (username, email, hashed_password))
        mysql.connection.commit()
        cur.close()

        #session['username'] = username
        return redirect(url_for('home'))

    return render_template('regis.html')

@app.route('/dashboard')
# @login_required
def dashboard():
#     return render_template('dash.html')
    if 'username' in session:
        username = session['username']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE username = %s', (username,))
        user = cur.fetchone()
        cur.close()

        # Mengambil kolom 'name' dari tabel user (sesuaikan dengan struktur tabel Anda)
        user_name = user['username'] if user and 'username' in user else 'Unknown'  # Sesuaikan dengan kolom 'name'

        # Mendapatkan waktu dan tanggal saat ini
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return render_template('dash.html', username=username, user_name=user_name, current_datetime=current_datetime)
    else:
        return redirect(url_for('dashboard'))  
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# @app.route('/time')
# def waktu():
#     today_date = datetime.today().strftime('%Y-%m-%d')
#     return render_template('waktu.html', today_date=today_date)

if __name__ == '__main__':
    app.run(debug=True)
