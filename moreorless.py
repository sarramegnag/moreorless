from random import randrange


# Ask the number to the user and ask again if it's not a number
def ask_number():
    result = -1

    while result < 0:
        result = input('Guess it? ')

        # Gére le cas de quelqu'un qui ne saisit pas un nombre
        try:
            result = int(result)
            print('You chosed ', result, '.', sep='')
        except ValueError:
            print('This is not a number. Try again.')
            result = -1

    return result


# Check if player has found computer number, display a message and returns if number has been found
def player_has_found(player_number, computer_number, number_of_tries):
    found = False

    if player_number == computer_number:
        found = True
        print('Bravo! You found in', number_of_tries, 'tries!')
    elif player_number > computer_number:
        print('It\'s less.')
    else:
        print('It\'s more.')

    return found


continue_game = True

while continue_game:
    number_found = False
    guess_tries = 0

    number_to_find = randrange(101)

    while not number_found:
        player_choice = ask_number()

        guess_tries += 1

        number_found = player_has_found(player_choice, number_to_find, guess_tries)

    restart = input('Restart (Y/n) ? ')
    if restart == 'n' or restart == 'N':
        continue_game = False
