const Apify = require('apify');
var path = require('path');
const helper = require('./helper');


Apify.main(async () => {
    console.error("Crawling single page");
    const requestQueue = await Apify.openRequestQueue();

    PageURL = process.env.DOWNLOAD_URL
    OutputFolder = process.env.OUTPUT_FOLDER

    await requestQueue.addRequest({ url: PageURL });
    var arr = PageURL.split("/");
    var baseURL = arr[0] + "//" + arr[2]
    var pseudoURL = baseURL + "/" + "[.*]"
    const pseudoUrls = [new Apify.PseudoUrl(pseudoURL)];

    const crawler = new Apify.PuppeteerCrawler({
        requestQueue,
        handlePageFunction: async ({ request, page }) => {
            const images = await page.evaluate(() => Array.from(document.images, e => e.src));
            for (let i = 0; i < images.length; i++) {
                var filename = images[i].split('/').pop()
                filename = helper.remove_parameters_from_url(filename);
                if (helper.check_supported_file_extensions(filename))
                {
                    fullFileName = path.join(OutputFolder, filename)
                    if (images[i].substring(0,8)  == "https://")
                    {
                        result = await helper.downloadHTTPS(images[i], fullFileName);
                    }
                    if (images[i].substring(0,7)  == "http://")
                    {
                        result = await helper.downloadHTTP(images[i], fullFileName);
                    }
                    if (result === true)
                    {
                        console.log('Success:', images[i], 'has been downloaded successfully.');
                    } 
                    else 
                    {
                        console.log('Error:', images[i], 'was not downloaded.');
                        console.error(result);
                    }
                }
              }
        },
        maxRequestsPerCrawl: 100,
        maxConcurrency: 10,
        launchPuppeteerOptions: {   
          headless: true,   
          stealth: true,   
          useChrome: true,
          args: ['--no-sandbox'],

      },
    });

    await crawler.run();
});
