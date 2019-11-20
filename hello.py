from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort
from flask import render_template
from flask_bootstrap import Bootstrap

import dash
import dash_core_components as dcc
import dash_html_components as html 
#from dashapp import server as application

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


@app.route('/analysis')
def analyse():
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),
    
        html.Div(children='''
            Dash: A web application framework for Python.
        '''),
    
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ])
    #return render_template('analysis.html', name=app)
    return app.index()
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
   
    
if __name__=='__main__':
    app.run(debug=True)
