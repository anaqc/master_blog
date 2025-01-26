from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)
DATA_FILE = "data/data.json"

"""
[
    {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
    {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'},
    # More blog posts can go here...
]
"""
@app.route('/')
def index():
    # add code here to fetch the job posts from a file

    blog_posts = read_data()
    return render_template('index.html', posts=blog_posts)


def read_data():
    """
    This function read all the data from DATA_FILE and return it
    """
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
        if data == "" or data == None:
            return []
        return data
    except FileNotFoundError:
        return []


def write_date(data):
    """
    This function write the data in the DATA_FILE
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
     This function handles the addition of a new Author.
    - If the request method is 'POST', it processes the submitted form data,
      creates a new blog post, and appends it to the existing data.
    - If the request method is 'GET', it renders the 'add.html' template,
      which contains the form for adding a new post.
    """
    data = read_data()
    if request.method == 'POST':
        new_author = {
            "id" : len(read_data()),
            "author" : request.form.get("author"),
            "title" : request.form.get("title"),
            "content" : request.form.get("content")
        }
        data.append(new_author)
        write_date(data)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route("/delete/<int:post_id>", methods=['POST'])
def delete(post_id):
    data = read_data()
    data.pop(post_id)
    write_date(data)
    return redirect(url_for('index'))




if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)