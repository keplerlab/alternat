pushd .
if not exist %userprofile%\.alternat mkdir %userprofile%\.alternat
cd  %userprofile%\.alternat 
npm install apify@0.21.9 --save
popd
