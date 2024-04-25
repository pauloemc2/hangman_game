# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 23:13:47 2024

@author: paulo
Hangman Game
"""
import random

# Gets the words from the .txt and converts it on a list
# The .txt file must be on the same directory as the .py code
file = open(r"hangman.txt")
word_list = file.readlines()
file.close()

# Randomly choses a word from the list
list_size = len(word_list)
word_index = random.randint(0, list_size)
chosen_word = word_list[word_index]
chosen_word = chosen_word[0: -1] # Must do this slice to eliminate the \n command at the end of the string

# Prepare the interface
print("***********************************************************")
print("                      Hangman                              ")
print("***********************************************************")

# Player number of guesses
guesses = 7 

# Victory condition
victory_condition = False

# String that is visible to the player
visible_str = (len(chosen_word)) * "?"

while guesses > 0 and victory_condition == False:
    print("\n-----------------------------------------------------------")
    print(visible_str)
    print("Guesses left: ", guesses)
    
    player_str = input("Name a character or risk it all by naming the entire word: ")
    
    if len(player_str) == 0:
        print("Enter a valid character!\n")
        
    elif len(player_str) == 1:
        guess_char_index = chosen_word.find(player_str)
        
        if guess_char_index == -1:
            print("Sorry, you guessed wrong!")
            guesses -= 1
        
        else:
            print("Nice!")
            
            for i in range(len(chosen_word)):
                if chosen_word[i] == player_str:

                    slice_a = visible_str[0: i]
                    slice_b = visible_str[i + 1: len(chosen_word) + 1]
                    visible_str = slice_a + player_str + slice_b
            
            if visible_str.find("?") == -1:
                victory_condition = True
                
    elif len(player_str) > 1:
        
        if player_str == chosen_word:
            print("Congratulations! You guessed correctly!")
            victory_condition = True
            
        else:
            print("Sorry, you guessed wrong!")
            guesses = 0
            
if guesses == 0:
    print("\n-----------------------------------------------------------")
    print("Game Over T_T\nThe word was:", chosen_word)
    
elif victory_condition == True:
    print("\n-----------------------------------------------------------")
    print("Congratulations! You won!\nThe word was:", chosen_word)
        