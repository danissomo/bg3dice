# Small Baldur's Gate 3 dice animation generator

Example:

![example](https://github.com/danissomo/bg3dice/raw/refs/heads/master/doc/ex.gif)

## Install 

### From source

linux
```bash
git clone https://github.com/danissomo/bg3dice
cd bg3dice
python3 -m venv venv
source venv/bin/activate
pip install .
```

Windows
```shell
git clone https://github.com/danissomo/bg3dice
cd bg3dice
py -m venv venv
.\venv\Scripts\activate
py -m pip install .
```

### From TestPyPi

```bash
pip install -i https://test.pypi.org/simple/ bg3dice
```

## Usage

### As CLI utility 

```text
usage: bg3dice [-h] [-n {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}] [-o OUTPUT] [-s]

Render a BG3 dice roll animation.

options:
  -h, --help            show this help message and exit
  -n {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}, --number {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}
                        The dice number to roll (0-19). If not provided, a random number will be chosen.
  -o OUTPUT, --output OUTPUT
                        The output GIF file name. Default is 'output.gif'.
  -s, --silent          If set, suppresses console output.
```

### As Python lib

```python
from bg3dice import render_animation, save_animation
frames, n = render_animation() 

save_animation(frames, f"{n}_roll.gif")

frames, _ = render_animation(10) 
```