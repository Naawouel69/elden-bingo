import os
import random
import string

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, join_room as sio_join_room, emit

from objectives import OBJECTIVES

app = Flask(__name__)
app.config["SECRET_KEY"] = "elden-bingo-dev-key"
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

CATEGORIES = sorted({o["category"] for o in OBJECTIVES})
DIFFICULTIES = ["Easy", "Medium", "Hard"]

PLAYER_COLORS = [
    "#c9a227",  # gold
    "#8a3a3a",  # crimson
    "#3f6b5c",  # verdigris
    "#5c6b9e",  # steel blue
    "#9e5c8a",  # amethyst
    "#b8763f",  # amber
    "#4a8a8a",  # teal
    "#8a6b4a",  # bronze
]

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O/1/I

# In-memory room store. Fine for a one-off game night; state resets on restart.
# rooms[code] = {
#   "size": int,
#   "board": [ {text, category, difficulty}, ... ]  length size*size
#   "marks": { "0": ["Alice", "Bob"], ... }          cell index -> player names
#   "players": { sid: {"name": str, "color": str} },
#   "host_name": str,
#   "categories": [str], "difficulties": [str],
#   "note": str | None,
# }
rooms = {}


def gen_room_code():
    while True:
        code = "".join(random.choices(CODE_ALPHABET, k=5))
        if code not in rooms:
            return code


def build_board(size, categories, difficulties):
    """Pick size*size objectives, broadening the filter if the pool is too small."""
    needed = size * size

    def matches(o, cats, diffs):
        return (not cats or o["category"] in cats) and (not diffs or o["difficulty"] in diffs)

    pool = [o for o in OBJECTIVES if matches(o, categories, difficulties)]
    note = None

    if len(pool) < needed:
        wider = [o for o in OBJECTIVES if matches(o, categories, [])]
        if len(wider) >= needed:
            pool = wider
            note = "Not enough objectives at that difficulty — broadened to all difficulties in your chosen categories."
        else:
            pool = list(OBJECTIVES)
            note = "Not enough objectives matched your filters — used the full objective pool instead."

    if len(pool) >= needed:
        chosen = random.sample(pool, needed)
    else:
        # Should only happen for very large boards; repeats allowed as last resort.
        chosen = random.choices(pool, k=needed)
        note = "Board is larger than the objective pool — some objectives repeat."

    random.shuffle(chosen)
    return chosen, note


def completed_lines(size, marks):
    marked = {int(i) for i in marks.keys()}
    lines = []
    for r in range(size):
        row = set(range(r * size, r * size + size))
        if row <= marked:
            lines.append(f"row-{r}")
    for c in range(size):
        col = set(range(c, size * size, size))
        if col <= marked:
            lines.append(f"col-{c}")
    diag1 = set(range(0, size * size, size + 1))
    if diag1 <= marked:
        lines.append("diag-0")
    diag2 = set(range(size - 1, size * size - 1, size - 1))
    if diag2 <= marked:
        lines.append("diag-1")
    return lines


def room_state(room):
    return {
        "board": room["board"],
        "marks": room["marks"],
        "players": list(room["players"].values()),
        "size": room["size"],
        "note": room.get("note"),
        "host_name": room["host_name"],
        "lines": completed_lines(room["size"], room["marks"]),
    }


# ---------------------------------------------------------------- HTTP routes

@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES, difficulties=DIFFICULTIES, error=None)


@app.route("/create", methods=["POST"])
def create():
    name = (request.form.get("name") or "").strip()[:20] or "Tarnished"
    try:
        size = int(request.form.get("size", 5))
    except ValueError:
        size = 5
    size = max(3, min(size, 7))
    categories = request.form.getlist("categories")
    difficulties = request.form.getlist("difficulties")

    code = gen_room_code()
    board, note = build_board(size, categories, difficulties)
    rooms[code] = {
        "size": size,
        "board": board,
        "marks": {},
        "players": {},
        "host_name": name,
        "categories": categories,
        "difficulties": difficulties,
        "note": note,
    }
    return redirect(url_for("room", code=code, name=name))


@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "GET":
        code = (request.args.get("code") or "").strip().upper()
        if code and code in rooms:
            return redirect(url_for("room", code=code))
        return redirect(url_for("index"))

    code = (request.form.get("code") or "").strip().upper()
    name = (request.form.get("name") or "").strip()[:20] or "Tarnished"
    if code not in rooms:
        return render_template(
            "index.html", categories=CATEGORIES, difficulties=DIFFICULTIES,
            error=f"No room found with code {code}.",
        )
    return redirect(url_for("room", code=code, name=name))


@app.route("/room/<code>")
def room(code):
    code = code.upper()
    if code not in rooms:
        return redirect(url_for("index"))
    name = (request.args.get("name") or "").strip()[:20] or "Tarnished"
    r = rooms[code]
    return render_template(
        "room.html",
        code=code,
        name=name,
        size=r["size"],
        board=r["board"],
        marks=r["marks"],
        note=r.get("note"),
        host_name=r["host_name"],
    )


# --------------------------------------------------------------- Socket.IO

@socketio.on("join")
def on_join(data):
    code = (data.get("code") or "").upper()
    name = (data.get("name") or "Tarnished")[:20]
    if code not in rooms:
        emit("error_msg", "That room no longer exists.")
        return

    room_obj = rooms[code]
    used_colors = {p["color"] for p in room_obj["players"].values()}
    color = next((c for c in PLAYER_COLORS if c not in used_colors), random.choice(PLAYER_COLORS))
    room_obj["players"][request.sid] = {"name": name, "color": color}

    sio_join_room(code)
    emit("state", room_state(room_obj))
    emit("players_update", list(room_obj["players"].values()), room=code)
    emit("toast", f"{name} entered the Lands Between.", room=code, include_self=False)


@socketio.on("disconnect")
def on_disconnect():
    for code, room_obj in list(rooms.items()):
        if request.sid in room_obj["players"]:
            name = room_obj["players"].pop(request.sid)["name"]
            emit("players_update", list(room_obj["players"].values()), room=code)
            emit("toast", f"{name} left.", room=code)
            break


@socketio.on("toggle_cell")
def on_toggle_cell(data):
    code = (data.get("code") or "").upper()
    if code not in rooms or request.sid not in rooms[code]["players"]:
        return
    room_obj = rooms[code]
    name = room_obj["players"][request.sid]["name"]

    idx = str(data.get("index"))
    try:
        i = int(idx)
    except (TypeError, ValueError):
        return
    if not (0 <= i < room_obj["size"] ** 2):
        return

    marks = room_obj["marks"].setdefault(idx, [])
    if name in marks:
        marks.remove(name)
        if not marks:
            del room_obj["marks"][idx]
    else:
        marks.append(name)

    emit(
        "marks_update",
        {"marks": room_obj["marks"], "lines": completed_lines(room_obj["size"], room_obj["marks"])},
        room=code,
    )


@socketio.on("reroll")
def on_reroll(data):
    code = (data.get("code") or "").upper()
    if code not in rooms or request.sid not in rooms[code]["players"]:
        return
    room_obj = rooms[code]
    if room_obj["players"][request.sid]["name"] != room_obj["host_name"]:
        emit("error_msg", "Only the host who created the room can reroll the board.")
        return

    board, note = build_board(room_obj["size"], room_obj["categories"], room_obj["difficulties"])
    room_obj["board"] = board
    room_obj["marks"] = {}
    room_obj["note"] = note
    emit("state", room_state(room_obj), room=code)
    emit("toast", f"{room_obj['host_name']} rerolled the board.", room=code)


@socketio.on("reset_marks")
def on_reset_marks(data):
    code = (data.get("code") or "").upper()
    if code not in rooms or request.sid not in rooms[code]["players"]:
        return
    room_obj = rooms[code]
    if room_obj["players"][request.sid]["name"] != room_obj["host_name"]:
        emit("error_msg", "Only the host who created the room can reset marks.")
        return

    room_obj["marks"] = {}
    emit("marks_update", {"marks": {}, "lines": []}, room=code)
    emit("toast", f"{room_obj['host_name']} reset the board.", room=code)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == True
    socketio.run(app, host="0.0.0.0", port=port, debug=debug)
