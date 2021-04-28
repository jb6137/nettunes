Design notes:

1.  We're allowing users to put a record on the queue even if it is already rented.
    Maybe you want to listen to the same record in 1 week.
    I.e. you can have a record rented, and also have it on the queue.
    But you cannot rent a record twice, or put it on the queue twice.

2.  Getting tests to work is proving pretty time consuming. Will prioritize adding
    enough code to get this working, since I don't think I'll have enough time for
    everything.

3.  When a user returns a record (creating a space to rent another record) the system
    immediately tries to pull a record from her waitlisted queue. This is a very simple
    algorithm that might not work well (fairly) in some circumstances. Using it in
    the interest of simplicity and time.

4.  In addition to tests, one thing that I skipped that if I had more time I would have added
    (or refactored to include): Error handling layer. All top level view methods should have
    try-catch blocks, to handle errors being passed up from downstream methods. E.g.
    try:
        do_something
    except AuthError:
        return 401
    except InputError:
        return 400
    except SomethingElse:
        return 500
    