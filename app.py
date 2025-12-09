from functools import wraps

from flask import Flask, render_template, request, session, redirect, url_for

from database_connection import DatabaseConnection

app = Flask(__name__)
app.secret_key = 'AS1214jds123%!@#'

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('user_login'))
    return wrapper


@app.route('/')
def main_page():
    user_session = session.get('logged_in', False)  # session as dict key: logged_in value: True/False
    username = None  # Guarantee that variable exists
    if user_session:
        with DatabaseConnection() as db:
            user = db.execute('SELECT * FROM user WHERE id = ?', (session['user_id'],)).fetchone()
            if user:
                username = user[
                    'login']  # Get username from database and display it on main page in Hello block if user exists

    # Collecting the 5 latest films added to the database
    with DatabaseConnection() as db:
        list_of_films = db.execute('SELECT id,name, year, country FROM film ORDER BY added_at DESC LIMIT 5').fetchall()

    return render_template('index.html', user_session=user_session, username=username, latest_films=list_of_films)


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        first_name = request.form['username']
        last_name = request.form['lname']
        login = request.form['login']
        email = request.form['email']
        password = request.form['password']
        birth_date = request.form['birth_date']
        with DatabaseConnection() as db:
            db.execute(
                'INSERT INTO user (first_name, last_name, password, login,email, birth_date) VALUES (?, ?, ?, ?, ?, ?)',
                (first_name, last_name, password, login, email, birth_date))
        return redirect(url_for('user_login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        with DatabaseConnection() as db:
            user = db.execute('SELECT * FROM user WHERE login = ? AND password = ?', (login, password)).fetchone()
            if user:
                session['logged_in'] = True
                session['user_id'] = user['id']
                return redirect(url_for('main_page'))
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def user_logout():
    session.clear()
    return redirect(url_for('main_page'))


@app.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    session_user_id = session['user_id']
    if request.method == 'POST':
        if user_id != session_user_id or session_user_id is None:
            return 'Unauthorized', 403

        first_name = request.form['username']
        last_name = request.form['lname']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        birth_date = request.form['birth_date']
        photo = request.form['photo']
        additional_info = request.form['additional_info']
        with DatabaseConnection() as db:
            db.execute('''
                UPDATE user 
                SET first_name = ?, last_name = ?, password = ?, email = ?, phone_number = ?, birth_date = ?, photo = ?, additional_info = ? 
                WHERE id = ?
            ''', (first_name, last_name, password, email, phone_number, birth_date, photo, additional_info, user_id))
        return 'Profile updated successfully'

    else:
        with DatabaseConnection() as db:
            user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
            if user is None:
                return 'User not found', 404

            if session_user_id:
                user_session = db.execute('SELECT * FROM user WHERE id = ?', (session_user_id,)).fetchone()
            return render_template('user_profile.html', user=user, user_session=user_session)


@app.route('/users/<user_id>/delete', methods=['DELETE'])
@login_required
def user_delete(user_id):
    return f'User {user_id}'


@app.route('/films', methods=['GET'])
def films():
    filter_list = []
    actor_filter = False  # need to know if JOIN is needed
    genre_filter = False
    for key, value in request.args.items():
        if value:
            if key == 'name':
                filter_list.append(f"film.name LIKE '%{value}%'")
            elif key == 'actor':
                actor_filter = True
                filter_list.append(f"(actor.first_name LIKE '%{value}%' OR actor.last_name LIKE '%{value}%')")
            elif key == 'genre':
                genre_filter = True
                filter_list.append(f"genre_film.genre_id = '{value}'")
            else:
                filter_list.append(f"film.{key} = '{value}'")

    base_query = 'SELECT * FROM film'
    actor_query = 'SELECT * FROM film JOIN actor_film ON film.id = actor_film.film_id JOIN actor ON actor_film.actor_id = actor.id'
    genre_query = 'SELECT * FROM film JOIN genre_film ON film.id = genre_film.film_id'
    actor_genre_query = 'SELECT * FROM film JOIN actor_film ON film.id = actor_film.film_id JOIN actor ON actor_film.actor_id = actor.id JOIN genre_film ON film.id = genre_film.film_id'

    if actor_filter and genre_filter:
        query_to_use = actor_genre_query
    elif actor_filter:
        query_to_use = actor_query
    elif genre_filter:
        query_to_use = genre_query
    else:
        query_to_use = base_query

    if filter_list:
        query_to_use += ' WHERE ' + ' AND '.join(filter_list)
    query_to_use += ' ORDER BY film.added_at DESC'

    with DatabaseConnection() as db:
        result_films = db.execute(query_to_use).fetchall()
        countries = db.execute("SELECT * FROM country").fetchall()
        actors = db.execute("SELECT first_name, last_name FROM actor").fetchall()
        genres = db.execute("SELECT * FROM genre").fetchall()
    return render_template('films.html', filtered_films=result_films, countries=countries, actors=actors, genres=genres)

@app.route('/films/<film_id>', methods=['GET', 'PUT'])
def film_detail(film_id):
    with DatabaseConnection() as db:
        result = db.execute('SELECT * FROM film WHERE id = ?', (film_id,)).fetchone()
        actors = db.execute(
            f'SELECT * FROM actor JOIN actor_film on actor.id == actor_film.actor_id WHERE actor_film.film_id = ?',
            (film_id,)).fetchall()
        genres = db.execute(f'SELECT genre FROM genre  JOIN genre_film ON genre.genre = genre_film.genre_id JOIN film ON film.id = genre_film.film_id WHERE film.id = ?', (film_id,)).fetchall()
        return render_template('film_detail.html', film=result, actors=actors, genres=genres)

@app.route('/films/<film_id>', methods=['DELETE'])
@login_required
def film_delete(film_id):
    with DatabaseConnection() as db:
        db.execute('DELETE FROM film WHERE id = ?', (film_id,))
    return redirect(url_for('films'))


@app.route('/films/<film_id>/rating', methods=['GET', 'POST'])
@login_required
def film_rating(film_id):
    with DatabaseConnection() as db:
        rating = db.execute('SELECT id, rating FROM film WHERE id = ?', (film_id,)).fetchone()
        return f'Rating for Film {film_id}: {rating}'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['GET', 'POST'])
@login_required
def film_feedback(film_id, feedback_id):
    with DatabaseConnection() as db:
        feedback = db.execute('SELECT film, grade, description FROM feedback WHERE film = ? AND id = ?',
                              (film_id, feedback_id)).fetchone()
        return f'Feedback {feedback_id} for Film {film_id}: {feedback}'


@app.route('/users/<user_id>/lists', methods=['GET', 'POST'])
@login_required
def user_lists(user_id):
    return f'Lists for User {user_id}'


@app.route('/users/<user_id>/lists/<list_id>', methods=['DELETE'])
@login_required
def user_list_detail(user_id, list_id):
    return f'List {list_id} for User {user_id}'


@app.route('/users/<user_id>/lists/<list_id>', methods=['GET', 'POST'])
@login_required
def user_watch_later_list(user_id, list_id):
    return f'Watch Later List {list_id} for User {user_id}'


@app.route('/users/<user_id>/lists/<list_id>/<film_id>', methods=['DELETE'])
@login_required
def remove_film_from_list(user_id, list_id, film_id):
    return f'Remove Film {film_id} from List {list_id} for User {user_id}'


if __name__ == '__main__':
    app.run(debug=True)
