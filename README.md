# Wii U on iOS: game compatibility

A community list of Wii U games that have been run on iPhone and iPad, with the device, the frame rate, known problems and gameplay footage.

It is made for [MuffinEMU](https://github.com/MuffinEMU/Muffin-EMU) and is open to results from any Wii U emulator on iOS. The same data feeds the [compatibility page on the MuffinEMU website](https://muffinemu.github.io/MuffinEMU/docs/compatibility.html).

**Add a game:** [open a report](../../issues/new?template=report-a-game.yml). **Add footage:** see [CONTRIBUTING.md](CONTRIBUTING.md).

## Statuses

| Status | Meaning |
|---|---|
| Runs well | Reported at a steady 60 fps or close to it on at least one device |
| Playable | Reported playable; the frame rate or small problems vary |
| Runs with issues | Starts and plays, with a clear problem such as audio or graphics |
| Doesn't work yet | Reported not working |
| Reported working | Reported working on at least one device, without more detail yet |

Frame rates depend on the device, on JIT, on graphic packs and on the version. A game that is not listed has not been reported yet.

## Games

<!-- GAMES:START -->
| Game | Status | Reports | Footage |
|---|---|---|---|
| **Bayonetta** | Runs with issues | unstable frame rate. Audio is delayed. Reported on an earlier build. | Wanted |
| **Call of Duty: Black Ops II** | Runs with issues | Loads and plays. The graphics side still needs work. One report with a video. | Wanted |
| **Captain Toad: Treasure Tracker** | Reported working | No details yet | Wanted |
| **Mario Kart 8** | Runs well | iPad Pro 11 (A12Z, 6 GB): 42 to 54 fps. MuffinEMU 10.2 with JIT active (StikDebug). Measured with the on-screen frame counter. Footage: a 2 minute 11 second race clip.<br>iPhone 16: 60 fps. | [1](https://github.com/MuffinEMU/wiiu-ios-compatibility/blob/main/snapshots/mario-kart-8/mario-kart-8_ipad-pro-a12z-6gb_jit-active_muffinemu-10.2.mp4) |
| **Need for Speed: Most Wanted** | Doesn't work yet | iPhone 15 Pro. Reported not working with JIT on and keys set up. Not resolved. | Wanted |
| **New Super Mario Bros. U** | Reported working | No details yet | Wanted |
| **Splatoon** | Playable | iPhone 12: up to 60 fps. Not independently confirmed.<br>15 to 30 fps. | Wanted |
| **Super Mario 3D World** | Runs well | iPhone 13: 60 fps. With JIT. Screenshot attached to the report. | Wanted |
| **The Legend of Zelda: Breath of the Wild** | Playable | iPhone 13 Pro Max: 23 to 30 fps. With the FPS++ graphic pack. One report of a save that would not load the next day.<br>iPhone 15 Pro. Reported to run well. | Wanted |
| **The Legend of Zelda: The Wind Waker HD** | Reported working | No details yet | Wanted |
<!-- GAMES:END -->

## Where the data lives

`data/games.json` is the source of truth. `tools/build.py` rebuilds the table above from it, and CI checks that the table is current. Gameplay footage and snapshots go in `snapshots/<game-slug>/` or are linked from the game's `footage` list.

## Licence

The code is GPL-3.0 (see [LICENSE](LICENSE)). The data and text are CC BY 4.0: reuse them freely and credit "Wii U on iOS compatibility list (MuffinEMU)". See [DATA-LICENSE.md](DATA-LICENSE.md).

Wii U and the game titles are trademarks of Nintendo and their owners. This list is not affiliated with Nintendo. It contains no games, keys or firmware.
