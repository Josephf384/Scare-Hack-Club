# Browser build for itch.io

This folder contains a browser-ready copy of The Button. The desktop version remains in `../theButton.py`.

## Build and preview

From the repository root, install Pygbag for Python 3.13 and build the web package:

```powershell
py -3.13 -m pip install pygbag
py -3.13 -m pygbag --archive .\theBottonHorrorGame\itch_build
```

Pygbag serves a local preview at `http://localhost:8000` and creates `itch_build/build/web.zip` for upload. The first web preview may take a while to load because it downloads the browser runtime.

## Upload to itch.io

Create or edit an itch.io project, choose **HTML** as the project type, and upload `build/web.zip`. Enable the option to play the uploaded file in the browser. The archive contains the `index.html` entry point itch.io requires.

## Sound

The web build looks for `assets/jumpscare.ogg`. If that file is absent, the visual game still runs and the jumpscare is silent. Pygbag recommends OGG audio for browser builds. Convert the desktop `../assets/jumpscare.wav` to OGG and place the result in this folder's `assets` directory to enable web audio.
