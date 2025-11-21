from flask import Flask,render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('index.html')


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
    return 'Films'


@app.route('/films/<film_id>', methods=['GET', 'PUT'])
def film_detail(film_id):
    return f'Film {film_id}'


@app.route('/films/<film_id>', methods=['DELETE'])
def film_delete(film_id):
    return f'Delete Film {film_id}'


@app.route('/films/<film_id>/rating', methods=['GET', 'POST'])
def film_rating(film_id):
    return f'Rating for Film {film_id}'


@app.route('/films/<film_id>/rating/<feedback_id>', methods=['GET', 'POST'])
def film_feedback(film_id, feedback_id):
    return f'Feedback {feedback_id} for Film {film_id}'


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
    app.run()
