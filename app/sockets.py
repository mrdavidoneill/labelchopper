from app import socketio
from flask_login import current_user
from flask_socketio import send, emit, join_room, leave_room


def send_progress(value):
    emit("progress", value, room=current_user.id, namespace="/progress")


def on_join(room):
    join_room(room)


ROOMS = {}


@socketio.on('start', namespace='/progress')
def on_create(room):
    """Create a room """
    ROOMS[room] = room
    on_join(room)


@socketio.on('stop', namespace='/progress')
def handle_disconnect():
    ROOMS.pop(current_user.id)

