# word_memorizing
This project is Personal Dictionary and Memorizing application.
- You can login and register a new user. (Example users: username: "a",  password:"b" or username: "abc", password: "123".)
- You can search for words on the Search page.
- You can see the entire dictionary on the Definition page.
- You can practice if you have saved at least 10 words in your dictionary.
- WordsAPI was not used in this project. There was a problem while creating a membership.
- There are 3 databases (sqlite3):

  - user_db: Contains "id", "username" and "password".
  - word_practice: There are "username" and the words registered by this username. At the same time, there is information about word power, how many searches are made, how many times a practice is made.
  - words: It is the database containing the word list. "id", "word" and "word_definition" information is included.
Due to workload and limited time, some checks could not be made, they can be completed. 
