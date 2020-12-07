if which node > /dev/null
    then
    echo "node is installed, skipping..."
    else
    echo "# Make sure node version > 12 is installed"
fi
cd ..
python setup.py install
cd alternat/collection/apify/ && npm install
cd ../../..
cd api
uvicorn message_processor:app --port 8080 --host 0.0.0.0 --reload 2>&1 | tee -a log.txt
