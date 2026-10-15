# Contributing

You can help in three ways. All of them need your **own legally dumped games**. Never share games, keys, firmware, or links to them.

## 1. Report a game

[Open a report](../../issues/new?template=report-a-game.yml) and fill in the form: the game, how it ran, your device and iOS version, the app and its version, whether JIT was on, and the frame rate. One report per game and device is perfect.

## 2. Add gameplay footage

Footage makes the list far more useful. A good clip:

- is **30 to 60 seconds** of actual gameplay, not a menu
- **shows the frame rate** (turn on the performance overlay) so people can see how it really ran
- names the **device, iOS version and app version** in the file name or the report, for example `mario-kart-8_ipad-pro-a12z_ios26_muffinemu-10.3.mp4`
- has **no personal information** on screen: no Apple ID, usernames, notifications or messages (turn on Do Not Disturb first)

Upload a clip by attaching it to a report (GitHub hosts it) and linking it, or add it to `snapshots/<game-slug>/` in a pull request. Keep files small (under 25 MB) and prefer a link for long videos.

## 3. Fix or improve the data

Edit `data/games.json`, then run `python3 tools/build.py` to rebuild the table, and open a pull request. CI fails if the README table is out of date.

A game entry looks like this:

```json
{
  "slug": "mario-kart-8",
  "name": "Mario Kart 8",
  "status": "runs-well",
  "reports": [
    { "device": "iPad Pro 11 (A12Z, 6 GB)", "fps": "42 to 54", "source": "Void (MuffinEMU 10.x)", "note": "" }
  ],
  "footage": []
}
```

Statuses are `runs-well`, `playable`, `runs-with-issues`, `broken` and `reported-working`.

## Rules

- Report what you saw. If you are unsure, say so in the note.
- Be kind. This is a small community project.
