# thairod-django

## Getting Started

### Installation

1. Have Postgres running on your machine (or docker)
2. Setup your python environment with env (recommend: pipenv). Read more at https://pipenv.pypa.io/en/latest/install/
3. in `thairod` folder, create `.env` file with 
   ```
   DB_URL="postgres://user:secret@localhost:5432/dbname"
   ```
   or
   ```
   DB_HOST="dbhost"
   DB_NAME="dbname"
   DB_USER="dbuser"
   DB_PASSWORD="password"
   ```
   *Make sure to have database connection with your specified user.
4. Run migration files
   ```sh
   python manage.py migrate
   ```
5. Run the application 
   ```
   python manage.py runserver
   ```
