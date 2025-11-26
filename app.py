from flask import Flask,render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def main_page():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT name, year, country FROM film ORDER BY added_at DESC LIMIT 5')
    result_films = cur.fetchall()
    return render_template('index.html', films=result_films)


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def user_login():
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def user_logout():
    return 'Logout'


@app.route('/users/<user_id>', methods=['GET', 'PUT'])
def user_profile(user_id):
    return f'User {user_id}'


@app.route('/users/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    return f'User {user_id}'


@app.route('/films', methods=['GET', 'POST'])
def films():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT id, poster, name FROM film ORDER BY added_at DESC')
    result_films = cur.fetchall()
    return f'Films {result_films}'


@app.route('/films/<film_id>', methods=['GET', 'PUT'])
def film_detail(film_id):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM film WHERE id = ?', (film_id,)) # more secure with parameterized query
    result = cur.fetchone()

    actors = cur.execute(f'SELECT * FROM actor JOIN actor_film on actor.id == actor_film.actor_id WHERE actor_film.film_id = ?', (film_id,)).fetchall()
    genres = cur.execute(f'SELECT * FROM genre_film WHERE film_id = ?', (film_id,)).fetchall()
    return f'Film {result}, Actors: {actors}, Genres: {genres}'


@app.route('/films/<film_id>', methods=['DELETE'])
def film_delete(film_id):
    return f'Delete Film {film_id}'


@app.route('/films/<film_id>/rating', methods=['GET', 'POST'])
def film_rating(film_id):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    rating = cur.execute('SELECT id, rating FROM film WHERE id = ?', (film_id,)).fetchone()
    return f'Rating for Film {film_id}: {rating}'

@app.route('/films/<film_id>/rating/<feedback_id>', methods=['GET', 'POST'])
def film_feedback(film_id, feedback_id):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    feedback = cur.execute('SELECT film, grade, description FROM feedback WHERE film = ? AND id = ?' , (film_id,feedback_id)).fetchone()
    return f'Feedback {feedback_id} for Film {film_id}: {feedback}'


@app.route('/users/<user_id>/lists', methods=['GET', 'POST'])
def user_lists(user_id):
    return f'Lists for User {user_id}'


@app.route('/users/<user_id>/lists/<list_id>', methods=['DELETE'])
def user_list_detail(user_id, list_id):
    return f'List {list_id} for User {user_id}'


@app.route('/users/<user_id>/lists/<list_id>', methods=['GET', 'POST'])
def user_watch_later_list(user_id, list_id):
    return f'Watch Later List {list_id} for User {user_id}'


@app.route('/users/<user_id>/lists/<list_id>/<film_id>', methods=['DELETE'])
def remove_film_from_list(user_id, list_id, film_id):
    return f'Remove Film {film_id} from List {list_id} for User {user_id}'


if __name__ == '__main__':
    app.run(debug=True)
