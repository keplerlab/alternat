cd ..
pip install torch==1.7.0+cpu torchvision==0.8.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install alternat
pushd .
if not exist %userprofile%\.alternat mkdir %userprofile%\.alternat
cd  %userprofile%\.alternat 
npm install apify 
popd
