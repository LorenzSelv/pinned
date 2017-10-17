## Assuming linux - bash:

0) install `virtualenvwrapper`, `python 3.6`
1) ```mkvirutalenv pinned --python=    `which python3.6` ``` 
2) `git clone git@github.com:LorenzSelv/pinned.git`
3) `cd pinned`
4) `pip install -r requirements.txt # make sure the virutalenv pinned is activated`
5) `export PINNED_DJANGO_SECRET_KEY='<ask lorenzo>' # SINGLE quotes are important`
6) `make db`
7) `make tests`
