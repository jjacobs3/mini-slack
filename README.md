# mini-slack

MiniSlack project! To set it up, do the following:

(1) Clone or download the repository

(2) IN THE FOLDER WHERE YOU DOWNLOADED OR CLONED THE REPOSITORY, set up your Heroku project by running
```
heroku create <APP NAME>
```
where you put the name of your app in place of <APP NAME>

(3) Create a new database by running
```
heroku addons:create heroku-postgresql:hobby-dev
```

(4) Find out your database url by running
```
heroku config
```

(5) Put the database url (in quotes!) at the point in app.py with the line
```
db_url = YOUR_URL_HERE!!!
```
