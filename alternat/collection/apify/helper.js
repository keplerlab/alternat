
const https = require('https');
const http = require('http');
const fs = require('fs');

function remove_parameters_from_url(urlString)
{
    var result = urlString.split("?")
    return result[0]
}


const downloadHTTPS = (url, destination) => new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destination);
  
    https.get(url, response => {
      response.pipe(file);
  
      file.on('finish', () => {
        file.close(resolve(true));
      });
    }).on('error', error => {
      fs.unlink(destination);
  
      reject(error.message);
    });
  });

  const downloadHTTP = (url, destination) => new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destination);
  
    http.get(url, response => {
      response.pipe(file);
  
      file.on('finish', () => {
        file.close(resolve(true));
      });
    }).on('error', error => {
      fs.unlink(destination);
  
      reject(error.message);
    });
  });


  function check_supported_file_extensions(url)
  {
    if (url.endsWith(".jpeg") || url.endsWith(".jpg") || url.endsWith(".JPG") || url.endsWith(".png"))
      return true
    else
      return false

  }


module.exports = { check_supported_file_extensions, remove_parameters_from_url, downloadHTTPS,downloadHTTP }