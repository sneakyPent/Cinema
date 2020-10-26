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

ech "=====================================================CREATING SUPERUSER"
echo    "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'admin')"| python manage.py shell
python manage.py runserver 0.0.0.0:8000
