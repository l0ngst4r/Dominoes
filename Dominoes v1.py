# Project Dominoes
# Jetbrains project 2021 by Zsolt Pal


import random


def generate_dominoes():
    # this creates the available dominoes at start
    dominoes = [[i, j] for i in range(0, 7) for j in range(i, 7)]
    random.shuffle(dominoes)
    return dominoes  # tried "return shuffle(dominoes)" but it returns empty object


def generate_pieces(dominoes):
    # generates both player and computer starting pieces
    pieces = []
    for i in range(7):
        pieces.append(dominoes.pop())
    return pieces


def display_game(list_stock, list_computer, list_snake, list_player):
    # 2D 4K graphics engine
    print("=" * 70)
    print(f'Stock size: {len(list_stock)}')
    print(f'Computer pieces: {len(list_computer)}')
    print("")
    # if "domino snake" exceeds six dominoes in length, drawing only the first 3 and last 3 dominoes
    # to avoid display cluttering
    if len(list_snake) > 6:
        snake_left_side = "".join(str(item) for item in list_snake[:3])
        snake_right_side = "".join(str(item) for item in list_snake[-3:])
        print(f'{snake_left_side}...{snake_right_side}')
    else:
        print("".join(str(item) for item in list_snake))  # prints the snake in one row
    print("")
    print("Your pieces:")
    for index in range(len(list_player)):
        print(f'{index + 1}:{list_player[index]}')
    print("")


def is_number(a_key):
    # checking the input for integers // stripping "-" sign as it's a string
    return a_key.lstrip("-").isnumeric()


def draw_game(list_snake):
    # end-game condition for draw
    # same number on both ends of snake and appears 8 times --> no more move possible
    if list_snake[0][0] == list_snake[-1][1] and list_snake.count(list_snake[0][0]) == 8:
        return True
    return False


def valid_move_left(a_domino, list_snake):
    if a_domino[0] == list_snake[0][0] or a_domino[1] == list_snake[0][0]:
        return True
    return False


def valid_move_right(a_domino, list_snake):
    if a_domino[0] == list_snake[-1][1] or a_domino[1] == list_snake[-1][1]:
        return True
    return False


def orient_domino_left(player_domino, snake_piece):
    if player_domino[0] == snake_piece[0]:
        player_domino[0], player_domino[1] = player_domino[1], player_domino[0]
        return player_domino
    return player_domino


def orient_domino_right(player_domino, snake_piece):
    if player_domino[1] == snake_piece[1]:
        player_domino[0], player_domino[1] = player_domino[1], player_domino[0]
        return player_domino
    return player_domino


def best_domino(list_snake, list_domino):
    snake_counted = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    # Count the number of 0's, 1's, 2's, etc., in hand, and in the snake.
    new_list = list_snake + list_domino
    for l in new_list:
        for i in l:
            snake_counted[i] += 1
    # Each domino in hand receives a score equal to the sum of appearances of each of its numbers.
    scored = {}
    for domino in list_domino:
        score = 0
        for num in domino:
            score += snake_counted[num]
        scored[list_domino.index(domino)] = score
    # choosing key of highest value which is the index of the highest scoring domino
    max_key = max(scored, key=scored.get)
    return list_domino[max_key]


def dominoes_game():
    stock_pieces = generate_dominoes()
    player_pieces = generate_pieces(stock_pieces)
    computer_pieces = generate_pieces(stock_pieces)
    # determining snake and starting player
    snake_domino = []
    if max(player_pieces) > max(computer_pieces):
        snake_domino.append(max(player_pieces))
        player_pieces.remove(max(player_pieces))
        player_status = "computer"
    else:
        snake_domino.append(max(computer_pieces))
        computer_pieces.remove(max(computer_pieces))
        player_status = "player"
    display_game(stock_pieces, computer_pieces, snake_domino, player_pieces)
    # game loop
    while True:
        if player_status == "player":
            print("Status: It's your turn to make a move. Enter your command.")
            # player loop
            while player_status == "player":
                pressed_key = input()
                if is_number(pressed_key):
                    if int(pressed_key) == 0:  # zero means add to player pieces from stock and skip turn
                        if not stock_pieces:  # if stock runs out, game gets to a draw
                            break
                        else:
                            player_pieces.append(stock_pieces.pop())
                            player_status = "computer"
                    elif len(player_pieces) * (-1) <= int(pressed_key) < 0:
                        # negative domino piece goes to the left of snake
                        if valid_move_left(player_pieces[int(pressed_key) * (-1) - 1], snake_domino):
                            oriented_domino = orient_domino_left(player_pieces.pop((int(pressed_key) * (-1) - 1)),
                                                                 snake_domino[0])
                            snake_domino.insert(0, oriented_domino)
                            player_status = "computer"
                        else:
                            print("Illegal move. Please try again.")
                    elif 0 < int(pressed_key) <= len(player_pieces):
                        # positive domino piece goes to the right
                        if valid_move_right(player_pieces[int(pressed_key) - 1], snake_domino):
                            oriented_domino = orient_domino_right(player_pieces.pop(int(pressed_key) - 1),
                                                                  snake_domino[-1])
                            snake_domino.insert(len(snake_domino), oriented_domino)
                            player_status = "computer"
                        else:
                            print("Illegal move. Please try again.")
                    else:
                        print("Invalid input. Please try again.")
                else:
                    print("Invalid input. Please try again.")
        if player_status == "computer":
            print("Status: Computer is about to make a move. Press Enter to continue...")
            while True:
                pressed_key = input()
                if pressed_key == "":  # checking if enter pressed
                    break
                else:
                    print("Please press enter")
            # computer loop
            computer_pieces_copy = computer_pieces[:]  # make a copy and iterate through that
            while player_status == "computer":
                if not computer_pieces_copy:  # checking if all dominoes have been tried in the copy
                    if not stock_pieces:  # if stock runs out, game gets to a draw
                        break
                    else:
                        computer_pieces.append(stock_pieces.pop())
                        player_status = "player"
                        break
                computer_move = best_domino(snake_domino, computer_pieces_copy)
                if valid_move_left(computer_move, snake_domino):
                    # negative domino piece goes to the left of snake
                    oriented_domino = orient_domino_left(computer_move, snake_domino[0])
                    computer_pieces.remove(computer_move)
                    snake_domino.insert(0, oriented_domino)
                    player_status = "player"
                elif valid_move_right(computer_move, snake_domino):
                    # positive domino piece goes to the right of snake
                    oriented_domino = orient_domino_right(computer_move, snake_domino[-1])
                    computer_pieces.remove(computer_move)
                    snake_domino.insert(len(snake_domino), oriented_domino)
                    player_status = "player"
                else:
                    computer_pieces_copy.remove(computer_move)  # if domino cannot be played, remove from copy
        display_game(stock_pieces, computer_pieces, snake_domino, player_pieces)
        # checking for end-game conditions
        if not player_pieces:
            print("Status: The game is over. You won!")
            break
        if not computer_pieces:
            print("Status: The game is over. The computer won!")
            break
        if draw_game(snake_domino):
            print("Status: The game is over. It's a draw!")
            break
        # if stock runs out, there are different scenarios
        if not stock_pieces:
            # if any_valid_move(player_pieces, snake_domino):  # player still has move
            #     player_status = "player"
            # elif any_valid_move(computer_pieces, snake_domino):  # computer still has move left
            #     player_status = "computer"
            # else:
            #     print("Status: The game is over. It's a draw!")  # no more moves possible
            #     break
            print("Status: The game is over. It's a draw!")
            break


dominoes_game()