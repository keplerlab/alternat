apt-get update
apt-get install -y wget gnupg curl procps
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
apt-get update
apt-get install -y google-chrome-stable fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst fonts-freefont-ttf libxss1 --no-install-recommends
rm -rf /var/lib/apt/lists/*


# node installation
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
. ~/.nvm/nvm.sh
. ~/.profile
. ~/.bashrc
nvm install --lts
nvm use --lts
mkdir -p ~/.alternat
chown -R $(whoami) ~/.alternat
cd ~/.alternat
npm install apify --unsafe-perm=true
cd -
