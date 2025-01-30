# Chain Story

## Run App
1. Make sure you have pip installed and updated
2. Run the following command in the root directory of the project (the directory with requirements.txt in it)
```pip install -r requirements.txt```
3. Then inside the `chainstory` directory run `daphne -p 8000 chainstory.asgi:application`
4: Connect to app in a browser at localhost:8000/lobby/

## Run migrations
If it's your first time, you may need to run the migrations to populate your db.sqlite3
`python manage.py migrate` 