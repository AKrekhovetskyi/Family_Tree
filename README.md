# Family tree
<strong>Family tree</strong> is a computer program with a graphical interface for creating and editing your family data.

![Main_window](/screenshots/Main_window.png)

More screenshots are available [here](/screenshots/).

## Prerequisites
> **NOTE:** Python version >3.8 is required.

```bash
python -m venv .venv
source .venv/bin/activate
export PYTHONPATH="$(pwd):$(pwd)/pyui:$(pwd)/business_logic"
pip install -r requirements.txt 
```

If you have issues installing the `pygraphviz` library on Linux Debian/Ubuntu like the ones below:
```bash
       3020 | #include "graphviz/cgraph.h"
            |          ^~~~~~~~~~~~~~~~~~~
      compilation terminated.
      error: command '/usr/bin/x86_64-linux-gnu-gcc' failed with exit code 1
      [end of output]
```

Run the following commands:
```bash
sudo apt-get update
sudo apt-get install graphviz libgraphviz-dev pkg-config
```

To install `tkinter` on Linux, please, follow [this instruction](https://tecadmin.net/how-to-install-python-tkinter-on-linux/).

## Getting started
You can clone the repo using the command below or download and unzip the archive.
```bash
git clone https://github.com/AndriyKy/Family_Tree.git
```

To launch the application, simply run the [main.py](/main.py) file:
```bash
python main.py
```

If there is an issue starting the app like the one below:
```bash
$ python main.py 
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, webgl, xcb.

Aborted (core dumped)
```

Run the following commands:
```bash
sudo apt-get update
sudo apt-get install libxcb-xinerama0 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-shm0
```
