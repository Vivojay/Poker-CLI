# Poker-CLI

### This is a simple offline Command Line Based poker game with fake virtual money
[Windows-Only at the time, tested on Windows 10]

## Why would I play this game?
Well, to enjoy yourself and have a fun time of course, right?. Even if you don't have playing cards at home or just want to enjoy some poker on your laptop for a couple minutes or even if you're just bored.

**\*Note:** Before running, you must add Your **Gmail ID** and **Password** to your local machine's *environment variables* and save them as `GMAIL_ID` and `GMAIL_PASS`.

## How to play
### How to get started
1. Locate and **run** the python file `main.py`.
2. The command line game first asks for the specifics of **money distribution**, i.e. the value of the *small blind* and also the amount of *money* that each player gets at the start of the game.
3. Next, it asks for the **number of players** who will be playing and then asks for their **usernames** one-by-one.
   (After the usernames are *registered*, they are listed at once as a bulleted list).
4. The game will then ask for the **email ids** of the users (*This is to email the private cards to each user*).
   (**Note:** It is important that the email ids be **correctly entered** the first time!)
5. The game of [poker](https://en.wikipedia.org/wiki/Poker) proceeds like normal after this. Click [here](https://www.instructables.com/Learn-To-Play-Poker---Texas-Hold-Em-aka-Texas-Ho/#:~:text=Each%20player%20is%20dealt%20two,by%20a%20third%20betting%20round.) for rules.

### Showdown and displaying the winner

Each player's final hands are shown in a table like this and the *winner* is also *marked* explicitly

```markdown
Please hit [enter] to see the final hands of each player: 
+------------------+----------------+---------------------------------------------------------+
| Player           | Cards          |                                                         |
|------------------+----------------+---------------------------------------------------------|
| Winner >> [abra] | 5C 5H 5D QS AD | ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐ |
|                  |                | │5        ││5        ││5        ││Q        ││A        │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │    ♣    ││    ♥    ││    ♦    ││    ♠    ││    ♦    │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │        5││        5││        5││        Q││        A│ |
|                  |                | └─────────┘└─────────┘└─────────┘└─────────┘└─────────┘ |
| abba             | 2H 2S 5H 5D AD | ┌─────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐ |
|                  |                | │2        ││2        ││5        ││5        ││A        │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │    ♥    ││    ♠    ││    ♥    ││    ♦    ││    ♦    │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │         ││         ││         ││         ││         │ |
|                  |                | │        2││        2││        5││        5││        A│ |
|                  |                | └─────────┘└─────────┘└─────────┘└─────────┘└─────────┘ |
+------------------+----------------+---------------------------------------------------------+

player [abra] won with 'Three of a kind'
Cards are: [5C, 5H, 5D, QS, AD]


The pot amount of 35 has been transferred to player [abra]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The current game has been saved
```
