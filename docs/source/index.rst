.. Logis documentation master file, created by
   sphinx-quickstart on Mon Sep 26 13:19:46 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Logis
=====
This is the design documentation of the Logis project, which is my attempt to overhaul the way we
do logistics at our church because, frankly, I don't like it.

What and Why?
-------------
At our church, our logistics are essentially driven by Google docs. Namely, by tons of spreadsheets on Google drive. I think we do things this way because of the following main reasons:
    
Flexibility
    since spreadsheets only enforce that you have tabular data, it's easy to whip up a new one without 
    having to think too hard about it. 

Easily Accessible/Widely Available 
    Having them on Google drive means that new information can be quickly disseminated to the rest of the 
    team. Additionally, having them on Google drive means there is a (somewhat) centralized location for 
    all of the information you need to know

Automated Rendering/Editing 
    Lots of pretty formatting options allow you to make your logistics documents "easy to read", and 
    formulas allow you to reduce the number of lines you have to change when you want to reassign someone 
    or change a task.

There are, however, many problems with this that I see, and some actually arise from the strenghts of
spreadsheets:

Too much flexibility
    The flexibility afforded by spreadsheets means that people inevitably end up abusing its free-form 
    nature, creating many custom formats that make sense to one person, but not to the general population 
    who has to constantly change gears in order to parse the document.

Information hoarding
    Because spreadsheets allow you to define multiple tabs in one sheet, it obfuscates what the true 
    hierarchical organization of logistics actually is. The doc that looks simple enough in the file
    explorer suddenly grows to a monstrous size once you click on it and actually take a look around the
    spreadsheet. This typically happens because once an event is over, rather than delete the events tab
    for it, we keep it in the spreadsheet and simply add a new tab for a new event.

Redundant/Inconsistent Information:
    Though spreadsheets allow you to define formulas that should make correlating data across pages easy 
    to do, in practice, this is rarely ever done because it's so much easier to copy-paste people's
    names rather than type in a cumbersome formula. Because of this, in a document that experiences 
    frequent edits, there is a high likelihood that the information on one tab will conflict with 
    information on another tab.


The Solution
------------

Logis will attempt to solve as many of the problems enumerated above while trying to retain as many of 
the advantages of spreadsheets as possible. The idea is to be able to retain the ability to edit and 
maintain multiple kinds of documents while at the same time adding the ability to generate a single,
consistent summary of all of the tasks that are assigned to one person or group of people. That way, you 
don't have to scramble around to find out what your responsibilities are, nor do you have to edit five
different spreadsheets to effect one change.


Contents
========

.. toctree::
   :maxdepth: 2

   architecture
   interactions

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

