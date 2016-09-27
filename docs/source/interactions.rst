Logis is meant to be hosted on a web-server, so we'll need to think carefully about how we handle interactions
between different users and the tasks/task contexts/assets that will be stored on the server.

Interactions
============
Generally, to avoid the headaches that come with asynchronous programming, task management in Logis will be
more serial than we are used to. Though there is a disadvantage to not being able to edit concurrently, I
don't think the ability to edit concurrently really gives us much of an advantage in the first place, and
the simplicity it affords in implementing our transactional model is more than worth whatever we give up for
such ease of use.

The basic idea is this. For editing a current task context:

#. User logs onto Logis
#. User opens up a task context
#. User then decides to edit task context
    - If no one else is editing the task context, the user acquires a write-lock for that context and
      is able to make changes to details to it, assign/remove roles, tasks, etc.
    - If someone else is already editing the context, the user gets a message alerting them to this
      fact. It may be useful to provide them a chat service to the person already editing this document
      if they have something they want to talk about.
