# Word game for Overlord Discord bot

Word game similar to the game wordle

## About
- Allows user to play wordle in discord
- When the game starts, the bot picks a random 5 lettered word and users try to guess it
- Users can check the words they guessed by using checkstatus
- The game ends when the correct word is guessed
- Games can be started and stopped and seperate channels
- Overlord picks words from the words.txt document


## Adding words
- Whenever a user sends a word, the bot matches it against the solution
- The bot sends a series of emojis relating to the correctness of the guessed word
- Green square means the letter in the word is correct
- Yellow square means the letter is in the solution, but not in the correct spot
- Black square means the letter is not in the solution

## Commands

### !wordgame <rounds>

- Starts the word game if not already started
- rounds: An optional argument to supply the number of rounds

### !addword <word>

- Adds a word to the game list
- word: A 5 letter word to add to the game list. Must be in the dictionary

### !endwordgame

- Ends a currently running word game

### !checkstatus

- Checks the status of the current word game
- Displays square emojis and the input words
