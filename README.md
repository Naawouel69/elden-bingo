# Elden Bingo

A shared, live-updating bingo board for playing custom Elden Ring objectives with friends.
One person creates a room and picks board size / categories / difficulty, everyone else
joins with the room code, and the board updates instantly for the whole group as squares
get marked.

## 1. Install

Requires Python 3.9+.

```bash
cd elden-bingo
pip install -r requirements.txt
```

## 2. Run

```bash
python app.py
```

This starts a server at `http://localhost:5000`. Open that in your browser — you (as host)
create the room there.

## 3. Get your friends in

The tricky part of any "shared board" tool: everyone's browser needs to reach *your*
computer, not just localhost. Pick whichever fits your group:

- **Same house / same Wi-Fi:** find your machine's local IP (`ipconfig` on Windows,
  `ifconfig` or `ip addr` on Mac/Linux — look for something like `192.168.x.x`), then have
  friends open `http://192.168.x.x:5000`. Give them the room code shown on your board too.
- **Different networks (most groups):** use a tunnel so your localhost is reachable
  from the internet. Easiest option is [ngrok](https://ngrok.com/):
  ```bash
  ngrok http 5000
  ```
  Share the `https://....ngrok-free.app` URL it gives you instead of localhost. Free tier
  is fine for a game night.
- **Want it always-on / no tunnel:** deploy `app.py` to a small free host (Render, Railway,
  Fly.io, PythonAnywhere all work). Nothing in the code assumes localhost.

## 4. How it works

- The host fills in the **Forge a New Board** form (name, board size, categories,
  difficulty) and hits Create. That generates a room code (e.g. `FOG7X`).
- Everyone else uses **Join an Existing Board** with that code and their own name.
- Clicking any square toggles it marked/unmarked for *everyone* in the room in real time —
  it's one shared team board, not separate boards per player.
- Completed rows, columns, or diagonals get a gold outline and a "BINGO!" flash for
  whoever's looking at the moment it completes.
- The host (whoever created the room) gets two extra buttons: **Reroll board** (new
  objectives, clears marks) and **Reset marks** (same objectives, clears marks).

## 5. Customizing objectives

Open `objectives.py` — it's a plain list of dicts:

```python
{"text": "Defeat Malenia, Blade of Miquella", "category": "Bosses", "difficulty": "Hard"}
```

Add, remove, or edit entries freely (categories/difficulties on the landing page are
generated from whatever's in the file), then restart the server. If a room's chosen
filters don't have enough objectives for the board size, the app automatically widens the
filter and shows a small note explaining what it did.

## Notes & limits

- Room state lives in memory — restarting the server clears all rooms. Fine for a single
  game session; not meant as a persistent service.
- No login/accounts — a "name" is just a display label for that room. Two players
  shouldn't use the exact same name in one room.
- Everything runs over plain HTTP by default. That's fine for a LAN or an ngrok tunnel
  (which adds HTTPS for you); don't expose it raw on the open internet for anything you
  care about securing.
