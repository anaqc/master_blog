from flask import Flask, render_template, request, redirect, url_for
import json
from pathlib import Path


app = Flask(__name__)

# Gloval variables use pathlib for better path handling
DATA_FILE = Path("data/data.json")


@app.route('/')
def index():
    # add code here to fetch the job posts from a file

    blog_posts = read_data()
    return render_template('index.html', posts=blog_posts)


def read_data():
    """
    Reads all the data from DATA_FILE and returns it.
    Returns an empty list if the file does not exist or is empty.
    """
    try:
        # Check if file exists before opening
        if not DATA_FILE.exists():
            return []
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Return data or empty list if None/empty
        return data if data else []
    # Handle corrupt JSON file
    except json.JSONDecodeError:
        return []
    # Catch unexpected errors
    except Exception as e:
        return []


def write_data(data):
    """Writes data to a JSON file safely, ensuring the directory exists."""
    try:
        # Ensure the 'data' directory exists before writing the file
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        # Open the file and write data as JSON
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Data successfully written to {DATA_FILE}")
    except PermissionError:
        print(f"Error: No permission to write to '{DATA_FILE}'. Try running with admin rights.")
    except IsADirectoryError:
        print(f"Error: '{DATA_FILE}' is a directory, not a file.")
    except IOError as e:
        print(f"IO error occurred: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


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
            "id" : max(post['id'] for post in data) + 1,
            "author" : request.form.get("author"),
            "title" : request.form.get("title"),
            "content" : request.form.get("content"),
            "like": 0
        }
        data.append(new_author)
        write_data(data)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route("/delete/<int:post_id>", methods=['POST'])
def delete(post_id):
    """
    This function delete a post by Id
    """
    data = read_data()
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return page_not_found("Post not found")
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
        return page_not_found("Post not found")
    if request.method == 'POST':
        # Update the post in the JSON file
        for i, dict_data in enumerate(data):
            if i == post_id:
                dict_data["author"] = request.form.get("author", dict_data["author"])
                dict_data["title"] = request.form.get("title", dict_data["title"])
                dict_data["content"] = request.form.get("content", dict_data["content"])
            new_data.append(dict_data)
        write_data(data)
        # Redirect back to index
        return redirect(url_for('index'))
    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


def fetch_post_by_id(post_id):
    """
       This function Retrieves a blog post by its ID.
    """
    data = read_data()
    # Ensure post_id is within the valid range
    for post in data:
        if post["id"] == post_id:
            return data[post_id]
    return None


@app.route("/like/<int:id_post>",  methods=['POST'])
def like(id_post):
    """
    This function show the “Like” button for each post. The button display the number of likes the
    post currently has, which is 0 initially.
    """
    post = fetch_post_by_id(id_post)
    if post is None:
        # Post not found
        return page_not_found("Post not found")
    new_data = []
    data = read_data()
    if 0 <= id_post < len(data):
        for i, dict_data in enumerate(data):
            if i == id_post:
                dict_data["like"] += 1
            new_data.append(dict_data)
    write_data(new_data)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
