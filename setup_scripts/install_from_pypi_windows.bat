cd ..
pip install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install alternat
pushd .
if not exist %userprofile%\.alternat mkdir %userprofile%\.alternat
cd  %userprofile%\.alternat 
npm install apify@0.21.9 --save
popd
