if which node > /dev/null
    then
    echo "node is installed, skipping..."
    else
    echo "# Make sure node version > 12 is installed"
fi
python setup.py install
cd alternat/collection/apify/ && npm install
cd ../../..