.. alternat documentation master file, created by
   sphinx-quickstart
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
========

**alternat** is a collection of open-source toolsets with the ambition
of lowering the barrier of adopting accessibility solutions\ **.
alternat** helps to generate default intelligible alternative text for
images in websites.

Based on our experience, just adding alt-text is not a complete solution
but collecting images to be annotated is a big part of the task. Keeping
in mind above two requirements the current version of alternat offers
two features:

-  Collect images from a website

-  Generate recommended alternative text

Why alternat
------------

70% of the sites are inaccessible and the inaccessibility is causing a
loss of 7 billion every year. In spite of availability of accessibility
standards for long and tools to point out where you are falling short,
there is a shortage of solutions which allow you to implement them with
ease. One of these areas is – **Alternate Text (alt text)**.

The alt-text attribute of image tag in html is supposed to make images
in websites accessible. But in practice, one doesn’t see it meaningfully
implemented. Someone has to go through all the images in question and
craft a corresponding alt text based on context. The investment to do it
can become high and it could take time to author the content.

What if there is a library, which can be integrated in your projects,
that provides a recommended alt text for a given image, which can be
either passed on as is or as a recommendation to a reviewer?
**alternat** just does that.

.. toctree::
   :maxdepth: 1

   Installing alternat <installing_alternat>
   Running alternat in 5 minutes <running_alternat_in_5_minutes>
   Understanding alternat <understanding_alternat>
   Configuring alternat <configuring_alternat>
   Using alternat <using_alternat>
   Reference Guide <reference>
