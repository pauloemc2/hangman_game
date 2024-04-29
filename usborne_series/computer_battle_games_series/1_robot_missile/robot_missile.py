from os import system
from random import randint

print('-------------')
print('ROBOT MISSILE')
print('-------------')

input('Press ENTER to start')

# Clear the terminal on Windows (cls) or Unix (clear)
system('cls || clear')

# Declare victory condition and number of tries
victory_condition = False
tries = 4

print('Type the correct character from A to Z.')
print(f'You have {tries} tries to defuse the missile!')
print('"Code >" means the secret character comes after the one you choose!')
print('"Code <" means the secret character comes before the one you choose!')
print('Good luck!')

# The program chooses a random character from A to Z:
random_char = chr(randint(65, 90))

# The program goes for the 4 tries of the player
tries_count = 1
while tries != 0 and victory_condition == False:
    player_try = input(f'Try #{tries_count} - Enter a character: ')
    tries -= 1
    tries_count += 1

    # Checks if the input was valid (Game Over if not):
    if len(player_try) != 1 or player_try.isalpha == False:
        tries = 0
    
    else:
        # Convert player char to uppercase
        player_try = player_try.upper()
    
        if ord(player_try) < ord(random_char) and tries != 0:
            print('Code >')
            
        elif ord(player_try) > ord(random_char) and tries != 0:
            print('Code <')
        
        elif ord(player_try) == ord(random_char):
            victory_condition = True

# Checks victory condition to award the player:

if victory_condition == True:
    print('Congratulations! You defused the bomb!')

else:
    print('BOOOOOOOOOOOOOOOOOOM')
    print('Mission failed! The robot missile exploded!')
    print(f'The secret char was {random_char}!')