# Run server

PROJECT_BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $PROJECT_BASE_DIR

rm -rf logs
rm cinema/db.sqlite3
rm -rf $(find . -type d -name "__pycache__")
rm -rf $(find . -type d -name "migrations")

python manage.py makemigrations backend
python manage.py migrate

echo '\033[96mInitializing Database:\033[0m'
python manage.py initGroupPermissions
python manage.py initUsers

python manage.py runserver 0.0.0.0:8000
