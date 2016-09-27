Logis is meant to be hosted on a web-server, so we'll need to think carefully about how we handle interactions
between different users and the tasks/task contexts/assets that will be stored on the server.

Interactions
============
Logis can be a google-docs kind of thing, where multiple people can concurrently edit the same document, but
given the scope of the team working on this project, it will probably be best that someone editing a
task context be given a write-lock on that context until s/he exits the write-mode.

UI-Mockup
---------
Again, there are two general types of views: planner views and peon views. The following diagrams give mockups
of what each could look like, as well as features of each:

