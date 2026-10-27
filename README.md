# BlockComet Engine

A game engine editor based on [Godot Engine](https://godotengine.org) (MIT, version 4.7.2) with a different look and layout:

* dark grey panels with a blue selection, thin borders, small corner radius and compact spacing;
* the **Project** (file system) panel at the bottom next to Output and the debugger, the scene tree on the left, the
  inspector on the right;
* BlockComet name, splash screen, icon and logos.

All of these are the *defaults of a fresh editor*; everything can still be changed in Editor Settings.

> Not affiliated with the Godot Foundation. "Godot" is a trademark of its owners. This project does not use Unity's name,
> assets or code; it only arranges the panels in a similar familiar order.

## How it works

This repository holds a **recipe**, not a copy of Godot:

| File | What it does |
|---|---|
| `.github/workflows/godot.yml` | downloads Godot at the tag in `GODOT_TAG`, applies the changes, builds the Linux editor with SCons, takes screenshots in a virtual screen and publishes them |
| `godot-custom/apply.py` | the changes. Each replacement asserts that the text it edits exists, so a different Godot version fails loudly |
| `godot-custom/assets/` | logo, splash screen, application icon |
| `godot-custom/demo/` | a small project opened for the screenshots |
| `godot-custom/screenshot.sh` | runs the editor in Xvfb (software OpenGL) and takes screenshots |

Results appear under **Releases**: `godot-test` (screenshots of the project manager and the editor) and `godot-latest`
(the Linux editor).

## Status

The patch script was tested on a local copy of Godot 4.7.2 (8 files change). The editor has **not been compiled yet** with these
changes, so there are no screenshots; the first build will show whether anything needs fixing. Building only the Linux editor
for now; Windows and Android editor builds come after the look is right.

## Build it yourself

```sh
git clone --depth 1 --branch 4.7.2-stable https://github.com/godotengine/godot.git godot
python3 godot-custom/apply.py godot
cd godot && scons platform=linuxbsd target=editor scu_build=yes lto=none debug_symbols=no wayland=no speechd=no dbus=no
```

## License

MIT, see [LICENSE](LICENSE). Godot Engine is also MIT; its notice stays in the built editor.
