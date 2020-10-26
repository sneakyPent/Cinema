sleep 3
echo '\033[96mInstalling NPM packages:\033[0m'
cd frontend
npm install -g @vue/cli
npm run serve -- --port 80