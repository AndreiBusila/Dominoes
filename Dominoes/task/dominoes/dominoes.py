import random

pieces = [[i, j] for i in range(7) for j in range(i, 7)]


class Domino:
    def __init__(self):
        self.pieces = [[i, j] for i in range(7) for j in range(i, 7)]
        self.stock = []
        self.player = []
        self.computer = []
        self.snake = []
        self.status = ""

    def generate_piece(self):
        random.shuffle(pieces)
        self.stock = pieces[0: 14]
        self.player = pieces[14: 21]
        self.computer = pieces[21: 28]
        self.first_move()

    def first_move(self):
        best_moves = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
        best_move = []
        for i in range(7):
            if self.player[i] in best_moves:
                best_move = max(best_move, self.player[i])
            if self.computer[i] in best_moves:
                best_move = max(best_move, self.computer[i])

        if best_move in self.player:
            self.player.remove(best_move)
            self.status = "computer"
        elif best_move in self.computer:
            self.computer.remove(best_move)
            self.status = "player"
        else:
            self.reset()
            self.generate_piece()
        self.snake.append(best_move)

    def reset(self):
        self.stock = []
        self.player = []
        self.computer = []
        self.snake = []
        self.status = ""

    def start(self):
        self.generate_piece()
        self.display()
        while True:
            if self.status == "player":
                self.user_move()
            elif self.status == "computer":
                self.computer_move_v2()
            self.display()
            if self.verify_game():
                break

    @staticmethod
    def delete_piece(location, piece):
        location.remove(piece)

    def move_from_stock(self, user):
        piece = random.choice(self.stock)
        user.append(piece)
        self.delete_piece(self.stock, piece)

    def move_front(self, piece):
        self.snake.append(piece)

    def move_back(self, piece):
        self.snake.insert(0, piece)

    def verify_compatibility_left(self, piece, index):
        for i in range(0, len(piece)):
            if piece[i] == self.snake[index][0]:
                return True
        return False

    def verify_compatibility_right(self, piece, index):
        for i in range(0, len(piece)):
            if piece[i] == self.snake[index][1]:
                return True
        return False

    def reverse_left(self, piece, index):
        if piece[1] != self.snake[index][0]:
            piece.reverse()
        return piece

    def reversed_right(self, piece, index):
        if piece[0] != self.snake[index][1]:
            piece.reverse()
        return piece

    def user_move(self):
        print("Status: It's your turn to make a move. Enter your command.")
        while True:
            try:
                user_input = int(input())
                if -len(self.player) <= user_input <= len(self.player):

                    if user_input == 0:
                        if len(self.stock) != 0:
                            self.move_from_stock(self.player)
                        else:
                            self.status = "computer"
                            break

                    piece = self.player[abs(user_input) - 1]

                    if user_input > 0:
                        if self.verify_compatibility_right(piece, len(self.snake) - 1):
                            self.delete_piece(self.player, piece)
                            revers_piece = self.reversed_right(piece, len(self.snake) - 1)
                            self.move_front(revers_piece)
                        else:
                            print("Illegal move. Please try again.")
                            continue
                    if user_input < 0:
                        if self.verify_compatibility_left(piece, 0):
                            self.delete_piece(self.player, piece)
                            revers_piece = self.reverse_left(piece, 0)
                            self.move_back(revers_piece)
                        else:
                            print("Illegal move. Please try again.")
                            continue
                    self.status = "computer"
                    break
                else:
                    print("Invalid input. Please try again.")
                    continue

            except ValueError:
                print("Invalid input. Please try again.")

    def computer_move(self):
        user_input = input("Status: Computer is about to make a move. Press Enter to continue...\n")
        if user_input == "":
            while True:
                r = random.randint(-len(self.computer), len(self.computer))
                # r = user_input
                if r == 0:
                    if len(self.stock) != 0:
                        self.move_from_stock(self.computer)
                    else:
                        continue

                    # piece = random.choice(self.stock)
                    # self.computer.append(piece)
                    # self.stock.remove(piece)
                else:
                    piece = self.computer[abs(r) - 1]
                    if r > 0:
                        if self.verify_compatibility_right(piece, len(self.snake) - 1):
                            piece = self.reversed_right(piece, len(self.snake) - 1)
                            self.move_front(self.computer, piece)
                        else:
                            continue
                        # self.snake.append(piece)
                        # self.computer.remove(piece)
                    if r < 0:
                        if self.verify_compatibility_left(piece, 0):
                            piece = self.reverse_left(piece, 0)
                            self.move_back(self.computer, piece)
                        else:
                            continue
                        # self.snake.insert(0, piece)
                        # self.computer.remove(piece)
                self.status = "player"
                break

        else:
            print("Invalid input. Please try again.")

    def computer_move_v2(self):
        user_input = input("Status: Computer is about to make a move. Press Enter to continue...\n")
        if user_input == "":
            rarity_number = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
            rarity_pieces = {}
            for i in self.computer:
                for j in i:
                    rarity_number[j] += 1
            for i in self.snake:
                for j in i:
                    rarity_number[j] += 1
            for i in self.computer:
                rarity_pieces["".join(str(j) for j in i)] = rarity_number[i[0]] + rarity_number[i[1]]

            rarity_pieces = {key: value for key, value in sorted(rarity_pieces.items(), key=lambda item: item[1])}
            ok = False
            for keys in rarity_pieces:
                piece = [int(x) for x in keys]
                if self.verify_compatibility_left(piece, 0):
                    self.delete_piece(self.computer, piece)
                    revers_piece = self.reverse_left(piece, 0)
                    self.move_back(revers_piece)
                    ok = True

                    break
                elif self.verify_compatibility_right(piece, len(self.snake) - 1):
                    self.delete_piece(self.computer, piece)
                    revers_piece = self.reversed_right(piece, len(self.snake) - 1)
                    self.move_front(revers_piece)
                    ok = True
                    break
            if not ok:
                if len(self.stock) != 0:
                    self.move_from_stock(self.computer)
            self.status = "player"
        else:
            print("Invalid input. Please try again.")


    def verify_game(self):
        if len(self.player) == 0:
            print("Status: The game is over. You won!")
            return True
        if len(self.computer) == 0:
            print("Status: The game is over. The computer won!")
            return True
        first_number = self.snake[0][0]
        last_number = self.snake[len(self.snake) - 1][1]
        if first_number == last_number:
            nr = 0
            for i in self.snake:
                for j in i:
                    if j == first_number:
                        nr += 1
            if nr == 8:
                print("Status: The game is over. It's a draw!")
                return True
        return False

    def display(self):
        print("======================================================================")
        print("Stock size: {0}".format(len(self.stock)))
        print("Computer pieces: {0}\n".format(len(self.computer)))
        if len(self.snake) < 7:
            for i in range(0, len(self.snake)):
                print(self.snake[i], end="")
        else:
            for i in range(0, 3):
                print(self.snake[i], end="")
            print(end="...")
            for i in range(len(self.snake) - 3, len(self.snake)):
                print(self.snake[i], end="")
        print("\n\nYour pieces:")
        for i in range(0, len(self.player)):
            print("{0}:{1}".format(i + 1, self.player[i]))
        print()


game = Domino()
game.start()
