from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('home.html')
    #return '<h1>Hello World!</h1>'
    #return '<h1>Bad Request</h1>', 400
    #user_agent = request.headers.get('User-Agent')
    #return '<p>Your browser is %s</p>' % user_agent
    #user_agent = request.headers.get('User-Agent')
    # return '<p>Your browser is %s</p>' % user_agent
    # return '<h1>Hello World!</h1>'
    # return '<h1>Bad Request.</h1>', 400
    
    # response = make_response('<h1>This document carries a cookie!</h1>')
    # response.set_cookie('answer', '42')
    # return response
    # return redirect('http://www.google.com')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
# @app.route('/user/<name>')
# def user(name):
#     return 'hello, %s!</h1>' % name

# @app.route('/user/<id>')
# def get_user(id):
#     user = load_user(id)
    
#     if not user:
#         abort(404)
#     return '<h1>Hello, %s</h1>' % user.name


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
   
    
if __name__=='__main__':
    app.run(debug=True)
