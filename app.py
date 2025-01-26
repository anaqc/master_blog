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


def write_data(data):
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
        write_data(data)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route("/delete/<int:post_id>", methods=['POST'])
def delete(post_id):
    """
    This function delete a author by Id
    """
    data = read_data()
    data.pop(post_id)
    write_data(data)
    return redirect(url_for('index'))


@app.route("/update/<int:post_id>", methods=["GET","POST"])
def update(post_id):
    """
    this function Fetch the blog posts from the JSON file
    """
    data = read_data()
    post = fetch_post_by_id(post_id)
    new_data = []
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        for i, dict_data in enumerate(data):
            if i == post_id:
                dict_data["author"] = request.form.get("author")
                dict_data["title"] = request.form.get("title")
                dict_data["content"] = request.form.get("content")
            new_data.append(dict_data)
        write_data(data)
        # Redirect back to index
        return redirect(url_for('index'))
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


def fetch_post_by_id(post_id):
    """
       Retrieves a blog post by its ID.
    """
    data = read_data()
    # Ensure post_id is within the valid range
    if 0 <= post_id < len(data):
        return data[post_id]
    return None


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)