## Initial setup (assuming linux - bash):

0) install `virtualenvwrapper`, `python 3.6`
1) ```mkvirutalenv pinned --python=    `which python3.6` ``` 
2) `git clone git@github.com:LorenzSelv/pinned.git`
3) `cd pinned`
4) `pip install -r requirements.txt # make sure the virutalenv pinned is activated`
5) **new**`sudo apt install curl`
6) **new**`curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.5/install.sh | bash`
7) **new**`nvm install node`
8) **new**`npm install`
9) `export PINNED_DJANGO_SECRET_KEY='<ask lorenzo>' # SINGLE quotes are important`
10) `make all`

## After each pull:
1) `make db`
2) `make tests`
3) `make frontend`

**or**

1) `make all`

## Modifiying front-end

### CSS
CSS is now handled through sass, which means both pure *css* and *scss/sass* are allowed. When creating new stylesheets keep in mind:
1) New stylesheets should be located in core/assets/sass/ and imported in the *sass* chain through `@import 'path/to/file'` (extention can be omitted) in one of the files that will be imported (*Note: the sass entry point is **app.scss**, so be sure that your stylesheet will be reachable by a series of `@import`s from it*)
2) It is good for general cleanliness of the assets dir to keep files separated for different components and creating new directoriess when needed in order to regroup stylesheets

### JS
Similarly to CSS, JS is now packed as well, so every new stylesheet should be reacheable through a series of `require('path/to/file')` (extention can be omitted) starting from **app.js**