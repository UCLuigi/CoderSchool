import random

def main():

	# set lives to 6
	lives = 0

	# set correct letters to empty list
	correct_guesses = []

	# set guessed letters to empty list
	guessed_letters = []

	# make a word list
	f = open("words.txt", "r")
	dictionary = []
	for line in f:
		dictionary.append(line.strip())

	# make secret_word equal to a random word from the word list
	secret_word = get_random_word(dictionary)

	# ask for their name (raw_input)
	name = input("> What is your name?\n")
	print ("Hello, ", name)

	# welcome the player
	welcome()

	# Player guess
	player_guess = None

	# Converts secret word into blanks
	for letter in secret_word:
		correct_guesses.append("_")

	winner = False

	# Repeat until lives == 9
	while lives < 9:

		print("You have ", 9 - lives, " lives")

		print(Hangman_pics[lives])

		# Print guesses so far
		print(correct_guesses)

		# Ask player for a guess
		player_guess = input("> Make a guess\n")

		# Make sure guess is one letter long and its a letter
		while len(player_guess) != 1 and not player_guess.isalpha():
			print("Invalid guess, try again!")
			player_guess = input("> Make a guess\n")

		# if player has guessed this before
		if player_guess in guessed_letters:

			# Reduce by one life
			print("You have already guessed that letter")
			lives += 1
		else:

			# add guess to guessed letters
			guessed_letters.append(player_guess)

			# Check if secret word contains guessed letters
			if player_guess in secret_word:

				# Correct guess
				print("That was correct")

				# Put correct guess in correct spot
				for i in range(len(secret_word)):
					if player_guess == secret_word[i]:
						correct_guesses[i] = player_guess

			else:
				# Incorrect guess
				print("Incorrect guess")
				lives += 1

		if secret_word == "".join(correct_guesses):
			print("You win!")
			winner = True
			break

	if not winner:
		print("You lose")

	print("The secret word was ", secret_word)


def welcome():
	print("Welcome to Hangman!")
	print("You have 9 lives, repeated guesses will be penalized!")

def get_random_word(word_list):
	return random.choice(word_list)

Hangman_pics = [

"""
-----
|   |
|
|
|
|
|
|
|
--------
""",
"""
-----
|   |
|   O
|
|
|
|
|
|
--------
""",
"""
-----
|   |
|   O
|  -+-
|
|
|
|
|
--------
""",
"""
-----
|   |
|   O
| /-+-
|
|
|
|
|
--------
""",
"""
-----
|   |
|   O
| /-+-\
|
|
|
|
|
--------
""",
"""
-----
|   |
|   O
| /-+-\
|   |
|
|
|
|
--------
""",
"""
-----
|   |
|   O
| /-+-\
|   |
|   |
|
|
|
--------
""",
"""
-----
|   |
|   O
| /-+-\
|   |
|   |
|  |
|
|
--------
""",
"""
-----
|   |
|   O
| /-+-\
|   |
|   |
|  |
|  |
|
--------
""",
"""
-----
|   |
|   O
| /-+-\
|   |
|   |
|  | |
|  |
|
--------
""",
"""
-----
|   |
|   O
| /-+-\
|   |
|   |
|  | |
|  | |
|
--------
"""
]


if __name__ == '__main__':
	main()
