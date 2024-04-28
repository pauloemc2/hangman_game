from msvcrt import kbhit
from os import system
from random import randint
from time import sleep

# Clear the terminal screen using 'cls' for Windows or 'clear' for Unix 
system('cls || clear')

print('----------------')
print('Cowboy Shootout!')
print('----------------')

input('Press ENTER to beggin:')
system('cls || clear')

sleep(1)
print('You are back to back!')
sleep(0.5)
print('Take 10 paces')
sleep(1)

# Counts the paces from 10 to 1
for i in range(10, 0, -1):
    print(f'{i}...')
    sleep(0.5)
    
    # Checks if you drew your gun during the paces
    if kbhit() == True:
        print('You drew your gun too fast!'
              '\n'
              'You lost!')
        input('Press ENTER to exit:')
        exit()

# Generates a random waiting time before the shootout
wait_interval = randint(10, 20)
for i in range(wait_interval, 0, -1):
    sleep(0.1)

    # Checks if you drew your gun during the random waiting time
    if kbhit() == True:
        print('Not so fast, amigo!'
              '\n'
              'You lost!')
        input('Press ENTER to exit:')
        exit()

# Initiates valid time frame to win
print('He draws...')
for i in range(16):
    sleep(0.1)

    # Victory condition is met
    if kbhit() == True:
        print('BANG!')
        sleep(1)
        print('You are really fast!')
        print('You won!')
        input('Press ENTER to exit:')
        exit()

print('BANG!')
sleep(1)
print('You were too slow!')
print('You were shoot!')
input('Press ENTER to exit:')