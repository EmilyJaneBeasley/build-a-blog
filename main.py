from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:sidney@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():
    if request.args:
        blog_id = request.args.get('id')
        blogs = Blog.query.filter_by(id=blog_id).all()
        return render_template('blog.html',blogs=blogs)
    else:
        blogs = Blog.query.all()
        return render_template('blog.html',blogs=blogs)



@app.route('/newpost', methods=['POST', 'GET'])
def add_blog():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ''
        body_error = ''

        if blog_title == '':
            title_error = 'Please enter a title'
        if blog_body == '':
            body_error = 'Please enter a post'
        
        if not title_error and not body_error:
            new_post = Blog(blog_title, blog_body)
            db.session.add(new_post)
            db.session.commit()
            new_id = str(new_post.id)
            return redirect('/blog?id='+new_id)
        else:
            return render_template('newpost.html', title = blog_title, body = blog_body, 
                title_error = title_error, body_error = body_error,)
    
    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()