from flask import Flask, request, redirect, render_template
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
    

    def __init__(self, title='', body=''):
        self.title = title
        self.body = body


@app.route('/blog', methods=['POST','GET'])
def index():
    if request.args:
        blog_id=request.args.get("id")
        blog=Blog.query.get(blog_id)

        return render_template('single_entry.html',blog=blog)

    else:
        blogs=Blog.query.all()
        return render_template('blog.html', blogs=blogs)



@app.route('/newpost',methods=["POST", "GET"])
def add_blog():
    if request.method=="GET":
        return render_template('newpost.html')

    title_error=''
    body_error=''

    if request.method=="POST":
        blog_title=request.form['title']
        blog_body=request.form['body']
    


    if not title_error and not body_error:
            new_blog=Blog(blog_title,blog_body)
            db.session.add(new_blog)
            db.session.commit()
            query_param_url = "/blog?id=" + str(new_blog.id)
  
            return redirect(query_param_url)
    
    if blog_body == '':
            blog_title = request.form['title']
            return render_template('newpost.html', blog_title=blog_title) 
    if blog_title == '':
            blog_body = request.form['body']
            return render_template('newpost.html', blog_body=blog_body)
   



    else:

            return render_template('newpost.html', title_error=title_error, body_error=body_error,blog_title=blog_title,blog_body=blog_body)

if __name__ == '__main__':
    app.run()   