from app import app, db
from app.models import User
from dotenv import load_dotenv

load_dotenv('.env')


@app.shell_context_processor
def make_shell_context():
    """ Adds db and User models when using 'flask shell' commandflask  """
    return {'db': db, 'User': User}


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=True,
            passthrough_errors=True)
