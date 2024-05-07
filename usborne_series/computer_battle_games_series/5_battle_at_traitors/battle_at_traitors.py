import curses
import math
import random
import time

def main(stdscr):

    # Initial settings:
    curses.curs_set(0)  # Hides cursor
    stdscr.clear()      # Clears screen

    # Get screen size:
    height, width = stdscr.getmaxyx()

#------------------------------------------------------------------------------#
# GAME PARAMETERS
#------------------------------------------------------------------------------#

    g_frame_time = 0.01
    g_spaces = 2 # Spaces separating the enemy positions
    g_quit_chr = 'q' # Key used to exit the game
    g_enemy_sym_1 = "O" # Symbol used for enemy #1
    g_barricade_spaces = 1 # Lines between player and enemy field
    g_player_chances = 3 # Max number of misses before a game over
    g_starting_time = 40 # Starting time to beat the game in seconds
    g_min_score = 600 # Minimum score for a victory
    g_enemy_qt_1 = 2  # Max quantity for enemy #1 on screen at the same time
    g_enemy_sc_1 = 10 # Score awarded for each enemy #1
    g_game_over = "Game Over" # Message #1 at Game Over screen
    g_go_misses = "You missed too much! The traitor has escaped!" # Message #2 at Game Over screen
    g_go_timer = "Your time is over! The traitor has escaped" # Message #3 at Game Over screen
    g_go_victory_1 = "CONGRATULATIONS!!!" # Message #1 at victory screen
    g_go_victory_2 = "The traitor was captured!" # Message #2 at victory screen

#------------------------------------------------------------------------------#
# FUNCTIONS
#------------------------------------------------------------------------------#

    # X positioning function:
    def text_pos_x(pos_flag: int, x_increment: int) -> int:
        """
        Returns the starting X position of the desired screen part in char spaces.
 
        Args:
            pos_flag: The flag used for the screen part.
            (0: center; else: left side)

            x_increment: How many char spaces to add or subtract on X.

        Returns:
            X: The desired X position in char spaces.
        """

        if pos_flag == 0:
            x = width // 2 + x_increment
        
        else:
            x = x_increment
        
        return x
    
#------------------------------------------------------------------------------#
    
    # Y positioning function:
    def text_pos_y(pos_flag: int, y_increment: int) -> int:
        """
        Returns the starting Y position of the desired screen part in char spaces.
 
        Args:
            pos_flag: The flag used for the screen part.
            (0: center; 1: top side; else: bottom side)

            y_increment: How many char spaces to add or subtract on Y.

        Returns:
            Y: The desired Y position in char spaces.
        """

        if pos_flag == 0:
            y = height // 2 + y_increment
        
        elif pos_flag == 1:
            y = y_increment
        
        else:
            # 0 is the 1st line, heigh is the line after the last one. 
            # That's why we must add the -1.
            y = (height -1) + y_increment 
        
        return y
    
#------------------------------------------------------------------------------#
    
    # Message printing function:
    def print_message(pos_flag_x: int, 
                      x_increment: int, 
                      pos_flag_y: int, 
                      y_increment: int, 
                      message_str: str):
        """
        Prints message on screen in the desired position.
 
        Args:
            pos_flag_x: The flag used for the X screen part.
            (0: center; else: left side)

            x_increment: How many char spaces to add or subtract on X.

            pos_flag_y: The flag used for the Y screen part.
            (0: center; 1: top side; else: bottom side)

            y_increment: How many char spaces to add or subtract on Y.

            message_str: String that will be printed.
        """
        
        if pos_flag_x == 0:
            # Message will be centered on X
            x = text_pos_x(pos_flag_x, x_increment) - len(message_str) // 2

        else:
            # Message will be printed on the left side
            x = text_pos_x(pos_flag_x, x_increment)

        # Y can be calculated using text_pos_y function and the increment
        y = text_pos_y(pos_flag_y, + y_increment)

        # Command to print message on screen from the curses module
        stdscr.addstr(y, x, message_str)

#------------------------------------------------------------------------------#

    # Title Screen function:
    def title_screen(title_str: str):
        """
        Calls the title screen.
 
        Args:
            title_str: Title of the game
        """

        stdscr.clear() # Clears screen
        
        title_frame = '#' + (len(title_str) + 2) * '-' + '#'
        title_str = '| ' + title_str + ' |'

        # Print title within a frame
        print_message(0, 0, 0, 1, title_frame)
        print_message(0, 0, 0, 0, title_str)
        print_message(0, 0, 0, -1, title_frame)

        # Print start message
        print_message(0, 0, 0, +4, "Press ENTER to start!")

        # Updates screen
        stdscr.refresh()

        # Loop waiting for the key press
        k = 1
        while k != 10:
            # Get user input, 10 for ENTER
            k = stdscr.getch()

#------------------------------------------------------------------------------#

    # Function to mount the scenario (interactive lists and barricades)
    def mount_scenario(spaces: int, player_chances: int) -> list:
        '''
        This function will initialize the game, making a list that will be used
        during the game flow by various other functions

        Args:
            spaces: Number of spaces between each valid position for a enemy in
            their base.

            player_chances: Max number of possible player misses before a Game
            Over.
        '''

        length = 10 + spaces * 9

        # Mounts the list that will be used to display enemies
        inter_enemy_list = []
        
        for x in range(length):
            
            if x % (spaces + 1) == 0:
                inter_enemy_list.append('.')
            
            else:
                inter_enemy_list.append(' ')
        
        # Mounts the string that will be used for enemy barricade
        enemy_barricade = ''
        y = 1

        for x in range(length):
           

            if x % (spaces + 1) == 0:
                
                if y == 10:
                    enemy_barricade += '0'
                
                else:
                    enemy_barricade += str(y)
                    y += 1
            
            else:
                enemy_barricade += '#'

        # Mounts string that will be used as player barricade
        player_barricade = '-' * length

        # Mounts interactive list that will be used as player position
        player_pos_list = [' ' for x in range(length)]

        main_list = [inter_enemy_list, 
                     enemy_barricade, 
                     player_barricade, 
                     player_pos_list,
                     "SCORE:", # Name used for the score
                     0, # Initial score value
                     "MISSES:", # Name used for the misses left
                     player_chances] # Starting number of possible misses
        
        return main_list

#------------------------------------------------------------------------------#
    
    # Function to transform a list into a string
    def list_string(list_: list) -> str:

        string_ = ''
        for element in list_:
            string_ += str(element)
            
        return string_

#------------------------------------------------------------------------------#
    
    # Function to print the list returned by mount_scenario
    def print_scenario(main_list: list, barricade_spaces: int):
        '''
        Made to print the list that is returned by mount_scenario
        '''
           
        # Prints bases on screen
        print_message(0, 0, 0, -2, list_string(main_list[0]))
        print_message(0, 0, 0, -1, main_list[1])
        print_message(0, 0, 0, barricade_spaces, main_list[2])
        print_message(0, 0, 0, (barricade_spaces + 1), list_string(main_list[3]))
        print_message(-1, 0, 1, 0, main_list[4])
        print_message(-1, 0, 1, 1, str(main_list[5]))
        print_message(-1, 0, 1, 2, main_list[6])
        print_message(-1, 0, 1, 3, str(main_list[7]))

        stdscr.refresh()

#------------------------------------------------------------------------------#

    # Function to print quit message
    def print_quit(quit_key: chr):
        '''
        Simply print "Press {key} to quit" centered at bottom screen

        Args:
            quit_key: Key configurated to act as a quit key
        '''

        quit_message = f'Press "{quit_key}" to quit!'
        print_message(0, 0, -1, 0, quit_message)
#------------------------------------------------------------------------------#

    # Makes an enemy appear at random position
    def enemy_spawn(symbol: chr, 
                    max_quant: int, 
                    spaces: int, 
                    main_list: list) -> list:
        '''
        This function will receive the main list and return another list
        containing the enemies in it.
 
        Args:
            symbol: The symbol that will be used to indicate an enemy.

            max_quant: The maximum number of enemies allowed om the enemy side.

            spaces: The number of spaces used to mount the scenario.

            main_list: The main list that is being used in the process. 

        Returns:
            new_list: The main_list updated containing the enemies.
        '''

        # Checks if the max_quant is in the desired interval (there can't be 
        # more than 10 enemies at any given time).
        if max_quant > 10:
            max_quant = 10
        
        if max_quant < 0:
            max_quant = 1
        
        # Checks how many enemies are already in the screen
        enenmies_os = main_list[0].count(symbol)
        enemies_add = max_quant - enenmies_os

        # If there are enemies on screen, we must take note of their positions
        enemies_os_pos = []
        if enemies_add > 0:
            for i in range(len(main_list[0])):
                if main_list[0][i] == symbol:
                    enemies_os_pos.append(i)

        # Makes a list containing the random positions the enemies can spawn
        enemy_spawn_pos = [x for x in range(0, len(main_list[0]), spaces + 1) 
                           if x not in enemies_os_pos]
        enemies_spawn_pos_2 = random.sample(enemy_spawn_pos, enemies_add)

        # Make the updated enemy list:
        for element in enemies_spawn_pos_2:
            main_list[0][element] = symbol
        
        return main_list
#------------------------------------------------------------------------------#

    # Function used to convert an ASCII number into a valid position in the
    # enemy list
    def key_to_pos(key_pressed: int, spaces: int) -> int:
        '''
        This function will receive the main list and return another list
        containing the enemies in it.
 
        Args:
            key_pressed: ASCII number of the pressed key.

            spaces: The number of spaces used to mount the scenario.

        Returns:
            position: The position corresponding to the pressed key in the
            enemy list. The function will return -1 if the player press a
            key not listed.
        '''

        position = -1

        if key_pressed == 48: # 0
            position = ((spaces + 1) * 9)
        
        elif 49 <= key_pressed and key_pressed <= 57: # 2 to 9
            position = (spaces + 1) * (key_pressed - 49)
        
        return position

#------------------------------------------------------------------------------#    
    
    # Function to check if an enemy was hit
    def enemy_hit(key_pressed: int, 
                  spaces: int, 
                  symbol: chr,
                  score_add: int,  
                  main_list: list) -> list:
        '''
            This function checks if the key pressed by the player corresponds
            to the position of a enemy on screen. If true, it will replace that
            position with '.' (indicating a blank space) and add the score. If
            false, a possible miss will be discounted.
    
            Args:
                key_pressed: ASCII number of the pressed key.

                spaces: The number of spaces used to mount the scenario.

                symbol: The symbol that will be used to indicate an enemy.

                score_add: Score awarded if enemy is hit

                main_list: The main list that is being used in the process.

            Returns:
                new_list: The main_list updated containing the enemies.
        '''

        pos = key_to_pos(key_pressed, spaces)

        if pos != -1: # Check for invalid key press
            
            if main_list[0][pos] != symbol: # Check if there was a miss
                main_list[7] -= 1
            
            elif main_list[0][pos] == symbol: # Check if there is an enemy
                main_list[0][pos] = '.' # Replaces enemy symbol for an empty space
                main_list[5] += score_add
            
        return main_list

#------------------------------------------------------------------------------#

    # Function to print the Timer
    def print_timer(time_to_print: float, algarisms):
        '''
        Function created to print the timer on screen.

        Args:
            time_to_print: Time remaining to end the game.

            algarisms: How many algarisms the starting time has (it's better to
            put the processing for the number of algarisms outside this function
            as it will be called for every frame)
        '''

        # We will need to use the zfill() str method here. If not used, the
        # number won't be correctly printed on screen when its algarisms number
        # go down during the countdown as we aren't using the clear screen
        # function between frames

        print_message(0, 0, 1, 1, 
                      f'Timer: {str(math.ceil(timer)).zfill(algarisms)}') 

#------------------------------------------------------------------------------#

    # Function for calling the Game Over screen

    def game_over(score: int, go_message: str, message: str):
        """
        Calls the Game Over screen.
 
        Args:
            score: The player ending score

            go_message: What will be displayed as "Game Over"

            message: Message to be displayed alongside the "Game Over"
        """

        stdscr.clear() # Clears screen

        # Prepares the 1st frame
        go_message_1 = go_message
        go_frame_1 = '#' + (len(go_message_1) + 2) * '-' + '#'
        go_message_1 = '| ' + go_message_1 + ' |'

        # Print Game Over frame
        print_message(0, 0, 0, -6, go_frame_1)
        print_message(0, 0, 0, -7, go_message_1)
        print_message(0, 0, 0, -8, go_frame_1)

        # Prepares the 2nd frame
        go_message_2 = message
        go_frame_2 = '#' + (len(go_message_2) + 2) * '-' + '#'
        go_message_2 = '| ' + go_message_2 + ' |'

        # Print the additional frame
        print_message(0, 0, 0, 1, go_frame_2)
        print_message(0, 0, 0, 0, go_message_2)
        print_message(0, 0, 0, -1, go_frame_2)

        # Print last score:
        print_message(0, 0, -1, -1, f'Final score: {score}')

        # Print quit message
        print_message(0, 0, 0, 7, "Press ENTER to quit")

        # Updates screen
        stdscr.refresh()

        # Loop waiting for the key press
        k = 1
        while k != 10:
            # Get user input, 10 for ENTER
            k = stdscr.getch()

#------------------------------------------------------------------------------#
# GAME FLOW
#------------------------------------------------------------------------------#

    # 1: Shows title screen and wait for ENTER key press
    title_screen("Battle at Traitors Castle")
    stdscr.clear()

    # 2: Print the initial scenario
    main_list = mount_scenario(g_spaces, g_player_chances)
    print_scenario(main_list, g_barricade_spaces)
    
    # 3: Frame processing
    stdscr.nodelay(True) # Won't pause the processing flow to wait for input
    timer = g_starting_time
    timer_algarisms = len(str(g_starting_time))

    while True:

        enemy_spawn(g_enemy_sym_1, g_enemy_qt_1, g_spaces, main_list)
        print_scenario(main_list, g_barricade_spaces)
        print_quit(g_quit_chr)
        print_timer(timer, timer_algarisms)
        timer -= g_frame_time # At each frame, the timer will be deducted
        stdscr.refresh()
        key = stdscr.getch() # Gets user input
        enemy_hit(key, g_spaces, g_enemy_sym_1, g_enemy_sc_1, main_list)

        # Verifies if the player has no misses left
        if main_list[7] <= 0:
            game_over(main_list[5], g_game_over, g_go_misses)
            break

        # Verifies if the player has no time left
        if timer <= 0:
            
            # Verifies if the player has the victory condition
            if main_list[5] >= g_min_score:
                game_over(main_list[5], g_go_victory_1, g_go_victory_2)
                break
            
            else:
                game_over(main_list[5], g_game_over, g_go_timer)
                break

        # Verifies if the quit key has been pressed
        if key == ord(g_quit_chr):
            break

        time.sleep(g_frame_time) # Processing simulation

# Starts the program
curses.wrapper(main)