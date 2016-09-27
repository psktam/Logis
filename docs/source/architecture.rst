Architecture
============
If you're familiar with software patterns (and I am not), you will realize that Logis implements the 
`Model-View-Controller <https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ 
architecture pattern. Refer to the link if you need to know what it actually is, but it's rather 
straightforward. 

Here, we will give a high-level overview of all of the components involved. More detailed descriptions will be broken out into the appropriate sub-pages.

Models
------

This section details the abstract models that drive the Logis project.

Tasks
+++++

The basic unit of work in Logis will be called a **task**. A task is deemed to be an "atomic", that is, indivisible, unit of work to which you can assign a person/people and a due date. These are items such as "load trailer by 5PM on Saturday". 

Task Contexts
+++++++++++++

Now, tasks by themselves tell you what you ought to do, but they are rather meaningless without a context in which they are to be done. Great, you say to yourself, I know that I need to load the trailer by 5PM, but what am I loading it for, and are there are other things that I need to do afterwards?

That's why **task contexts** exist. You can think of a task context as a collection of different tasks. This would be analogous to your What's Up Doc, or an event planning doc. These documents not only show what tasks there are to be done, but it also shows how all the tasks all fit together for an event or some other context.

Users
+++++

In Logis, a **user** is a human being that is capable of performing a task. Each user can be assigned multiple tasks, but no user should be assigned two or more tasks that conflict in time and/or location. That is because we humans, being of the world, literally cannot be in two places at once. Conversely, many users can be assigned a single task, but again, no one usere should be assigned to a task if it conflicts with the assignments s/he already has.

Assets
++++++

A church has lots of stuff lying around. Things like cars, inflatable mattresses, Course 101 books, and bags of rice. Like users, they can be inserted into certain tasks. Again, since assets are meant to be physical objects, they must occupy a certain location at a certain time, so they will be subjected to the same conflict rules that users are.


Views
-----

