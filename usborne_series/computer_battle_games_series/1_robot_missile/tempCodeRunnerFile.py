if ord(player_try) < ord(random_char) and tries != 0:
            print('Code >')
            
        elif ord(player_try) > ord(random_char) and tries != 0:
            print('Code <')
        
        elif ord(player_try) == ord(random_char) and tries != 0:
          