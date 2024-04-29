# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 01:50:06 2024

@author: Paulo Oliveira
"""
import math
import os
import random
import time


# Function to clear the console screen:
def clear_console():
    
    # nt for windows, else for linux
    os.system("cls" if os.name == "nt" else "clear")
    

game_difficulty = 0

print("----------------------------------------------------------------------")
print("VITAL MESSAGE")
print("----------------------------------------------------------------------")


while game_difficulty < 4 or game_difficulty > 10: 
    game_difficulty = int(input("How difficult (4 ~ 10): "))
    
    if game_difficulty < 4 or game_difficulty > 10:
        print("Please, choose a valid value!")

# Creates a random str with i chars
random_str = ""
for i in range(game_difficulty):
    random_ascii = random.randint(65, 90)
    random_str += chr(random_ascii)

clear_console()

print("SEND THIS MESSAGE:\n")
print(random_str)

# Regressive counter time_for_clear to 1
for i in range(game_difficulty * 0.5, 0, -1):
    print(f"TIME: {i}", end = "")
    # After a time.sleep(), the cursor will aparently return to the end of the 
    # printed line regardless of its last position. That's why we must return
    # it to the line beggining AFTER the command!
    time.sleep(1)
    print("\r", end="")
    
clear_console()

print("ENTER THE MESSAGE:\n")
player_str = input()
player_str = player_str.upper()

if player_str == random_str:
    print("Congratulations!\nThe war has ended!")
    
else:
    print("You got it wrong!\nThe message was: " , random_str)