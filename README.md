# chat-app-order
An in-development web based chat application project inspired by Discord.

Run serv.py to launch the server. Make sure socketio for python is installed.

Three accounts are already made available(UserA, UserB, UserC with password a,b,c respectively).

You can remove history by clearing log.txt, and remove accounts by clearing accs.json(remember to leave a pair of curly braces'{}' behind, and to clear profile pictures in /files/pfp).

# changelog
Version 0.1 (September 2, 2023):

1. Allows multiple clients to create accounts and login into a chat room.
2. Shows all online clients in a chat room.

Problems:
1. Atrocious UI
2. Loading profile pictures takes a while.
3. Allows multiple clients to login with the same account.
4. No security.
5. Needs an internet connection to work.

TODO:
1. Rooms
2. Nicknames
3. Fix problems
