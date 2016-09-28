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
     is able to make changes to details to it, assign/remove roles, tasks, etc. From now on, if someone
     else tries to edit the same task context, they will be denied such access.
   - If someone else is already editing the context, the user gets a message alerting them to this
     fact. It may be useful to provide them a chat service to the person already editing this document
     if they have something they want to talk about.

#. While editing the task context, consistency checks are made against the main server for each of these steps:

   - When an actor is assigned to a task
   - When a global asset is assigned to a task

   Additionally, after each of these steps, consistency checks are performed with the main server to make sure that
   the task context, as it currently is, does not conflict with the internal state of the server. This also allows us
   to update the task context view so that other people can see changes as they are being made.

#. When all edits are complete, the user submits the changes to the main server, where a final consistency check is
   done. If everything passes, then the changes are stored on the server, and the write-lock is released so that others
   may edit the documents.

Anticipated complications are:

- If the user unexpectedly loses contact with the server in the middle of editing the document, the write-lock may lock
  everyone out until the user logs back in and pushes his/her changes or cancels them.

  - The mitigation here would be to use a websocket connection to automatically cancel all changes and release the
    write-lock upon detecting a disconnect event.

- If the user assigns an actor to a task, then, while s/he is editing the current context, someone else tries to
  assign that same actor to another task that is now incompatible.

  - The appropriate response here would be to display an error to the user with information about what task/context
    the actor is now assigned to, with a link to a planner view of that task context and, optionally, the ability to
    chat with whoever most recently assigned that actor. (Actually, we should probably have a chat associated with each
    task context)
  - The same idea applies to global assets.

- If a global asset or actor is assigned to a lot of tasks and then someone wants to delete that asset or actor. What
  should the appropriate response be?

  - For now, the preferred plan of action would be to be conservative and not allow this to happen. It should display an
    error message indicating which tasks the asset/actor is currently assigned to and provide links to them so that
    the user can edit those themselves first.
  - To avoid headaches, this also mandates that we impose an expiration date for all task contexts and tasks. They
    should automatically delete themselves within a week after the last task in it.


