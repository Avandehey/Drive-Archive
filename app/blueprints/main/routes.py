from flask import render_template, g
from . import bp
from app import app
from app.forms import UserSearchForm

@app.before_request
def before_request():
    g.user_search_form = UserSearchForm()

@bp.route('/')
def home():
    # Define a dictionary with keys 'instructors' and 'students'
    key = {
        'instructors': ('Sean', 'Dylan'),
        'students': ['ray', 'hamed', 'gian', 'ben', 'christopher', 'alec']
    }
    
    # Render the index.jinja template with the title, instructors, students, and user_search_form
    return render_template('index.jinja', title='Drive Archive', instructors=key['instructors'], students=key['students'], user_search_form=g.user_search_form)

@bp.route('/about')
def about():
    # Render the about.jinja template with the title and user_search_form
    return render_template('about.jinja', title='Drive Archive', user_search_form=g.user_search_form)
