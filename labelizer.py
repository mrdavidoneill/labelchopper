import os

# REMOVED due to bug crashing the web server.  Works locally and also prints secret on web server so not sure why it crashes
# from app import environmentvariables
# environmentvariables.load()

from app import app, db, socketio
from app.models import User

@app.shell_context_processor
def make_shell_context():
    """ Adds db and User models when using 'flask shell' commandflask  """
    return {'db': db, 'User': User}


if __name__ == '__main__':
    # app.run(debug=True, use_debugger=False, use_reloader=True,
    #         passthrough_errors=True)
    socketio.run(app, host="0.0.0.0", port=5000, use_reloader=True)

