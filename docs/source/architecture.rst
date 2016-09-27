Architecture
============
If you're familiar with software patterns (and I am not), you will realize that Logis implements the 
`Model-View-Controller <https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ 
architecture pattern. Refer to the link if you need to know what it actually is, but it's rather 
straightforward. 

Here, we will give a high-level overview of all of the components involved. More detailed descriptions 
will be broken out into the appropriate sub-pages.

Models
------

This section details the abstract models that drive the Logis project.

Tasks
+++++

The basic unit of work in Logis will be called a **task**. A task is deemed to be an "atomic", that is, 
indivisible, unit of work to which you can assign a person/people and a due date. These are items such 
as "load trailer by 5PM on Saturday". 

Task Contexts
+++++++++++++

Now, tasks by themselves tell you what you ought to do, but they are rather meaningless without a 
context in which they are to be done. Great, you say to yourself, I know that I need to load the 
trailer by 5PM, but what am I loading it for, and are there are other things that I need to do afterwards?

That's why **task contexts** exist. You can think of a task context as a collection of different 
tasks. This would be analogous to your What's Up Doc, or an event planning doc. These documents 
not only show what tasks there are to be done, but it also shows how all the tasks all fit together 
for an event or some other context.

Actor
+++++

In Logis, an **actor** is a human being that is capable of performing a task. Each actor can be assigned 
multiple tasks, but no actor should be assigned two or more tasks that conflict in time and/or location. 
That is because we humans, being of the world, literally cannot be in two places at once. Conversely, 
many actors can be assigned a single task, but again, no one actor should be assigned to a task if it 
conflicts with the assignments s/he already has.

Assets
++++++

A church has lots of stuff lying around. Things like cars, inflatable mattresses, Course 101 books, 
and bags of rice. Like actor, they can be inserted into certain tasks. Again, since assets are meant 
to be physical objects, they must occupy a certain location at a certain time, so they will be subjected 
to the same conflict rules that actor are.


Views
-----

There are two general classes of views in Logis: 

Planner views
    These views show an administrative-level view of tasks. The What's Up Doc is a planner view, as it 
    shows all of the tasks that different people have in a way that is useful to one who is planning 
    and event or drafting logistics. It lets whoever is planning keep track of different assets, see 
    which actors are assigned to which task, and what task will happen in relation to another task.

Peon views
    These views show a summary of tasks as they pertain to one particular user. In a peon view,
    a user sees all the tasks that s/he is assigned to, and only those tasks. This way, you narrow
    down the scope of pages and documents one must check in order to see what one's duties are. 

With both views, we want the ability to be able to view multiple task contexts in one pane.

Controllers
-----------

Some basic ground rules for defining controllers:

- Tasks must always be created from a context; there can be no "one-offs" that can be assigned to people

- When a task is assigned to an actor, it must not conflict in time or location with tasks that have
  been/are assigned to other actors.

  - Similarly, assets must not be associated with tasks that conflict with each other

- Only tasks can be embedded in task contexts. Task contexts may not embed each other

- Only in the planner views can one create and delegate tasks. Peon views are meant to be "read-only".

So far, I can only think of one kind of controller, and that is closely coupled with the task context 
model and the planner view.

From the planner view, one can create and delegate tasks via a task context to other actors and 
assign assets and roles to those tasks. In this way, you can see that a task context also acts like
a controller, in that through it, you can manage and set different tasks.

Interactions
------------
The following is a rough diagram that illustrates the interactions that exist between all of the 
elements described above:

.. image:: _static/images/architecture_UML.png

