Understanding alternat
======================

alternat features are centered around tasks. Following table
features break up across each task:

+------------+---------------------------+---------------------------+----------------------+
| **Task**   | **Description**           | **Options**               | **Details**          |
+============+===========================+===========================+======================+
| Collection | Scans the website and     | Uses puppeteer to crawl   | We are using apify - |
|            | downloads images          | the web page.             | A puppeteer scrapper |
|            |                           |                           | that crawls website  |
|            |                           |                           | using the headless   |
|            |                           |                           | chrome               |
|            |                           |                           |                      |
|            |                           |                           | https://apify.com    |
|            |                           |                           |                      |
|            |                           |                           |                      |
+------------+---------------------------+---------------------------+----------------------+
| Generate   | Generates alt-text using, | Azure ML API              | Use azure CV API     |
|            | image captioning, OCR and |                           | for caption & OCR    |
|            | images labels             +---------------------------+----------------------+
|            |                           |                           |  Use Google vision   |
|            |                           | Google ML API based.      |  OCR and Image       |
|            |                           |                           |  Labelling           |
|            |                           +---------------------------+----------------------+
|            |                           | Open source based.        | Use pytorch based    |
|            |                           |                           | model for OCR        |
|            |                           |                           | (EasyOCR) as well as |
|            |                           |                           | image captioning     |
|            |                           |                           |                      |
+------------+---------------------------+---------------------------+----------------------+

Library offers the flexibility of choosing either or both tasks and selecting suitable options from each task.
Options are called drivers in alternat lingo.
So, if you want to use azure for alt-text generation then you initialize the generator with azure driver.
Same goes for google and “opensource” driver. Read the options as drivers.

There are few reasons for providing 3 drivers:

- Azure and google gives ready to use API, essentially lowering the barrier to get started.

- Most of the organizations don’t have the data to train their own model for OCR and image captioning.

- Open source is a free alternative but can be little less accurate in few situations.

The tradeoff here is between cost and accuracy.


The OCR function is responsible for reading text from images. However, most of the ML API for OCR would
treat single line as one text blob and might lead to unexpected out-of-order OCR text.
For this reason, alternat comes with its own clustering implementation for OCR.
alternat by default applies a clustering algorithm to create nearby
data as a single text blob and combines them into a single line thereby generating more
in-order human friendly OCR text.