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
app1 = dash.Dash(
           __name__,
           server=app,

           )
app1.layout = html.Div(children=[
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

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/analysis')
def analysis():
    x1 = request.args.get('x1')
    y1 = request.args.get('y1')
    x2 = request.args.get('x2')
    y2 = request.args.get('y2')

    return render_template('analysis.html', x1=x1, x2=x2, y1=y1, y2=y2,
                           w =request.args.get('w'), h = request.args.get('h'),
                           name = app1.layout)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
   
    
if __name__=='__main__':
    app.run(debug=True)
