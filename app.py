from flask import Flask, render_template
import json


app = Flask(__name__)

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
    with open('data/data.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)