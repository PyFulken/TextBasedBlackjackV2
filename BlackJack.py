# --------------------------------------------------FUNCTIONS------------------------------------------------------------
# This is the Pycharm Version, cloned for git push testing
# This is the first commit test line!
def input_int_sanitize():
    """
    Sanitizes Player input in instances that only an integer is supported
    """
    while True:
        try:
            helper = int(input())
        except ValueError:
            print("That is not a number, please input a number!")
        else:
            if helper > 0:
                break
            print("Please input a positive number!")
    return helper


# -----------------------------------------------------------------------------------------------------------------------
def game_start_number_players():
    """
    Starts the game by asking how many players will play.
    """
    print("How many players will be playing?")
    player_amount = input_int_sanitize()
    while player_amount > 7:
        player_amount = input_int_sanitize()
        print("Way too many players, I can handle up to 7.")
    clear_output()
    print_banner()
    print("Creating", player_amount, "players!")
    c = []
    for i in range(1, player_amount + 1):
        var_name = "player" + str(i)
        c.append(var_name)
    for i in c:
        player_dict[i] = Player()
    global currentbetamount
    currentbetamount = 0
    global deck
    deck = Deck()
    deck.shuffle()
    global dealer
    dealer = Dealer()


# -----------------------------------------------------------------------------------------------------------------------
def restart_game_check():
    """
    Asks players if they want to restart the game.
    """
    restart = input("Would you like to play another game? (Y,N)")
    while restart == "Y" or restart == "y":
        player_status()
        blackjack()
        check = input("Would you like to play another game? (Y,N)")
    if restart == "N" or restart == "n":
        clear_output()
        print_banner()
        print("Game Over!")


# -----------------------------------------------------------------------------------------------------------------------
def print_banner():
    """
    Keeps game clean and prints the game banner!
    """
    print("+-------------------------------------------------------------------+")
    print("|                                                                   |")
    print("|                        WELCOME TO FULKEN'S                        |")
    print("|                             BLACKJACK                             |")
    print("|                                                                   |")
    print("+-------------------------------------------------------------------+")
    print()


# -----------------------------------------------------------------------------------------------------------------------
def player_status():
    """
    Shows all player's name, balance and hand.
    """
    for i in player_dict:
        print("Player:", player_dict[i].name)
        print("Balance:", player_dict[i].balance)
        if player_dict[i].playerhand == []:
            print("It's an empty hand!")
        else:
            print("Hand:")
            player_dict[i].hand_show()


# -----------------------------------------------------------------------------------------------------------------------
def player_begin_game():
    """
    Lets the players begin the game with an input, while also offering to show text commands.
    """
    print("Are all players ready? Type Help for input commands")
    covid = input()
    while True:
        if covid.lower() == "help":
            clear_output()
            print_banner()
            print("After betting and being dealt a hand, the possible player moves are:",
                  "\nSurrender - You end your turn, lose half your bet and secure the other half, only possible as a first move.",
                  "\nHit - You draw another card.",
                  "\nDoubleDown - You bet upt to 100% of your original bet more, draw one card and end your turn",
                  "\nStand - You end your turn.")
            print("Type yes to begin the games!")
            covid = input()
        elif covid.lower() == "yes":
            print("Let the game begin!")
            break
        else:
            print("Just type yes whenever you feel like, no rush...")
            covid = input()


# -----------------------------------------------------------------------------------------------------------------------
def game_bets():
    """
    Forces each player to place their bets, deals 2 cards to each player and shows it.
    """
    for i in player_dict:
        player_dict[i].move_bet()
        time.sleep(1)
        dealer.bet_recieve()
        player_dict[i].hand_draw()
        player_dict[i].hand_draw()
        print("The dealer deals two cards!")
        time.sleep(2)
        print(player_dict[i].name, "'s hand is:")
        player_dict[i].hand_show()


# -----------------------------------------------------------------------------------------------------------------------
def game_player_turn():
    """
    Allows every player to play its turn, sequencially.
    """
    for i in player_dict:
        clear_output()
        print_banner()
        print("Player", player_dict[i].name, "'s turn!")
        print("Hand:")
        player_dict[i].hand_show()
        moves_made = 0
        print("What will you do?")
        while True:
            move = input()

            if move.lower() == "surrender" and moves_made == 0:
                dealer.bet_player_surrender()
                player_dict[i].move_surrender()
                break
            elif move.lower() == "surrender" and moves_made != 0:
                print("You can only surrender as a first move!")
                move = input()
            elif move.lower() == "hit":
                moves_made += 1
                player_dict[i].hand_draw()
                print("Hand:")
                player_dict[i].hand_show()
                worth = player_dict[i].hand_worth()
                if worth == 0 or worth == 21:
                    break
            elif move.lower() == "doubledown":
                player_dict[i].move_ddown()
                print("Hand:")
                player_dict[i].hand_show()
                break
            elif move.lower() == "stand":
                break
        print(player_dict[i].name, "ends the turn!")
        time.sleep(3)


# -----------------------------------------------------------------------------------------------------------------------
def payouts():
    """
    Checks for winners and distributes cash. NEEDS FIXING
    """
    global dealer
    for i in player_dict:
        current_worth = player_dict[i].hand_worth()
        if current_worth == 21 and current_worth > dealer.deal_hand_worth():
            print(player_dict[i].name, "wins with a blackjack! It recieves",
                  int((player_dict[i].playerbet * 1.5) + player_dict[i].playerbet))
            player_dict[i].balance += int((player_dict[i].playerbet * 1.5) + player_dict[i].playerbet)
            player_dict[i].playerbet = 0
            player_dict[i].hand_reset()
        elif current_worth == 21 and current_worth == dealer.deal_hand_worth():
            print(player_dict[i].name, "wins with a blackjack! But so does the dealer, so the payout is just",
                  player_dict[i].playerbet * 2)
            player_dict[i].balance += player_dict[i].playerbet * 2
            player_dict[i].playerbet = 0
            player_dict[i].hand_reset()
        elif current_worth > dealer.deal_hand_worth():
            print(player_dict[i].name, "wins! The payout is", player_dict[i].playerbet * 2)
            player_dict[i].balance += player_dict[i].playerbet * 2
            player_dict[i].playerbet = 0
            player_dict[i].hand_reset()
        elif current_worth == 0 and dealer.deal_hand_worth() > 0:
            print(player_dict[i].name, "lost!")
            player_dict[i].playerbet = 0
            player_dict[i].hand_reset()
        else:
            print(player_dict[i].name, "lost! but so did the dealer, so the bet money is returned.")
            player_dict[i].balance += player_dict[i].playerbet
            player_dict[i].playerbet = 0
            player_dict[i].hand_reset()
    global currentbetamount
    currentbetamount = 0
    global deck
    deck = Deck()
    deck.shuffle()
    dealer = Dealer()
    time.sleep(10)


# -----------------------------------------------------------------------------------------------------------------------
def blackjack():
    """
    Main game loop.
    """
    time.sleep(1)
    clear_output()
    print_banner()
    dealer.deal_hand_draw()
    print("The dealer drew a:")
    time.sleep(1)
    dealer.deal_hand_show()
    # Game loop goes here
    game_bets()
    print("The dealer is gathering all the money!")
    time.sleep(4)
    clear_output()
    print_banner()
    print("The dealer has", dealer.bettingpool, "dollars in the betting pool!")
    print("Time for the players to make their moves!")
    game_player_turn()
    clear_output()
    print_banner()
    print("It's the dealer's turn!")
    dealer.deal_hit()
    payouts()
    clear_output()
    print_banner()
    print("The dealer resets the game, hands, board, and shuffles the deck!")
    player_status()


# ------------------------------------------------------CLASSES----------------------------------------------------------
class Card():
    """
    Esta classe é criada para nos ajudar a criar o deck de cartas.
    Cada carta em 2 atributos: o seu valor e a sua naipe.
    """

    def __init__(self, value, color):
        self.value = value
        self.color = color

    def show(self):
        """
        Esta função é criada para mostrar cada carta.
        Primeiro o valor e depois a naipe.
        """
        print(self.value, "of", self.color)


# -----------------------------------------------------------------------------------------------------------------------
class Deck():
    """
    Esta classe é criada para criar o deck de cartas.
    Cada deck é uma string the objectos Card.
    Diferentes instancias desta classe significa diferentes decks.
    """

    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """
        Used only for internal building of the deck
        """
        for c in ["Spades", "Clubs", "Diamonds", "Hearts"]:
            for v in range(2, 11):
                self.cards.append(Card(v, c))
            for v in ["Ace", "King", "Queen", "Jack"]:
                self.cards.append(Card(v, c))

    def shuffle(self):
        """
        Shuffles the deck, what did you expect?
        """
        import random
        random.shuffle(self.cards)

    def deal_card(self):
        """
        As a normal deck, the function takes out the top card (last item in the list),
        efectivelly drawing a card and eliminating the possibility of drawing it again.
        """
        return self.cards.pop()

    def show(self):
        """
        Shows the entire deck using the Cards method show(), mainly for debug.
        """
        for c in self.cards:
            c.show()


# -----------------------------------------------------------------------------------------------------------------------
class Player():
    def __init__(self):
        print("What's your name?")
        self.name = input()
        print("What's your balance?")
        self.balance = input_int_sanitize()
        self.playerbet = 0
        self.playerhand = []
        self.victory = False

    def hand_show(self):
        """
        Shows the player's hand.
        """
        for c in self.playerhand:
            c.show()

    def hand_draw(self):
        """
        Draw's a card from the deck to the palyer's hand.
        Do twice at turn's beginning and once per player Hit input.
        Requires a Deck() instance named >deck<
        """
        self.playerhand.append(deck.deal_card())

    def hand_reset(self):
        """
        Reset's a player's hand
        """
        self.playerhand = []

    def hand_worth(self):
        """
        Sums the worth of a player's hand, checks for hand bust and Ace save.
        Returns worth if hand does not bust, else returns 0
        It's a bit wonky, may repeat prints...
        """
        worth = 0
        for c in self.playerhand:
            if c.value == "King" or c.value == "Queen" or c.value == "Jack":
                worth += 10
            elif c.value == "Ace":
                worth += 11
            else:
                worth += int(c.value)
        for c in self.playerhand:
            if c.value == "Ace" and worth > 21:
                worth -= 10
                print("Hand bust saved by an Ace!")
        if worth > 21:
            print("Hand went kaboom, you lose!")
            return 0
        elif worth == 21:
            print("Blackjack!")
            return worth
        else:
            return worth

    def move_bet(self):
        """
        Asks the user for a valid bet amount, removes that amount from the player's balance,
        sets current playerbet and currentbetamount for immediate usage of dealer.bet_recieve afterwards.
        Requires global variable named >currentbetamount<
        """
        print("How much will you be betting,", self.name, "?")
        amount = input_int_sanitize()
        while self.balance < amount:
            print("We don't give out loans here! You only have", self.balance, "dollars, buddy!")
            amount = input_int_sanitize()
        else:
            if self.balance == amount:
                print("All in, baby!")
            else:
                print(self.name, "has bet", amount, "dollars.")
        self.balance -= amount
        self.playerbet = amount
        global currentbetamount
        currentbetamount = amount

    def move_ddown(self):
        """
        Requests another valid bet from the user, removes that amount from the player's balance,
        sets current playerbet and currentbetamount for immediate usage of dealer.bet_recieve afterwards.
        Requires global variable named >currentbetamount<
        """
        if self.balance != 0:
            print("How much will you be raising your bet by,", self.name, "?")
            amount = input_int_sanitize()
            while amount > self.balance:
                print("We don't give out loans here! You only have", self.balance, "dollars, buddy!")
                amount = input_int_sanitize()
            else:
                while self.playerbet < amount:
                    print("You cannot bet more than your original bet!")
                    amount = input_int_sanitize()
                else:
                    self.balance -= amount
                    self.playerbet = amount
                    global currentbetamount
                    currentbetamount = amount
                    self.playerhand.append(deck.deal_card())
        else:
            print("No,", self.name, ",we don't accept other kinds of payment here, you got no money to bet!")
            currentbetamount = 0

    def move_surrender(self):
        """
        To be paired with dealer.bet_player_surrender.
        Returns half of the bet amount to the player's balance. Resets the hand.
        """
        self.balance += int(self.playerbet / 2)
        self.hand_reset()


# -----------------------------------------------------------------------------------------------------------------------
class Dealer():
    def __init__(self):
        self.dealerhand = []
        self.bettingpool = 0

    def deal_hand_show(self):
        """
        Shows the dealer's hand.
        Careful to only draw one card at the beginning, and the second after all player moves are done,
        as per game's rules.
        """
        for c in self.dealerhand:
            c.show()

    def deal_hand_draw(self):
        """
        Draw's a card to the dealer's hand.
        Do ONCE at game's start, proceed with deal_hand_show.
        """
        self.dealerhand.append(deck.deal_card())

    def deal_hand_worth(self):
        """
        Sums the worth of the dealer's hand, checks for hand bust and Ace save.
        Returns worth if hand does not bust, else returns 0
        Forces draw if worth is below 17, as per game's rules.
        This one is veeeeeeeeeeeeeeeeeeeery wonky....
        """
        deal_worth = 0
        for c in self.dealerhand:
            if c.value == "King" or c.value == "Queen" or c.value == "Jack":
                deal_worth += 10
            elif c.value == "Ace":
                deal_worth += 11
            else:
                deal_worth += int(c.value)
        for c in self.dealerhand:
            if c.value == "Ace" and deal_worth > 21:
                deal_worth -= 10
                print("Dealer's hand bust was saved by an Ace!")
        if deal_worth > 21:
            print("Dealer's hand went kaboom, everyone wins!!")
            deal_worth = -1
        elif deal_worth == 21:
            print("Home Blackjack!")
        return deal_worth

    def deal_hit(self):
        """
        Dealer hits until hand is worth more 17 or more or busts.
        Bit wonky with Aces....
        """
        print("The dealer's initial card is:")
        self.deal_hand_show()
        while self.deal_hand_worth() < 17 and not self.deal_hand_worth() == -1:
            self.deal_hand_draw()
            print("The dealer draws a card!")
            self.deal_hand_show()
            time.sleep(2)

    def deal_hand_reset(self):
        """
        Reset's a player's hand
        """
        self.dealerhand = []

    def bet_recieve(self):
        """
        The dealer recieves the current player's bet. Requires a global variable named >currentbetamount<.
        """
        global currentbetamount
        if currentbetamount == 0:
            print("The dealer is sad and got nothing...")
        else:
            print("The dealer has recieved", currentbetamount, "dollars!")
            self.bettingpool += currentbetamount

    def bet_player_surrender(self):
        """
        To be paired with player.move_surrender.
        The dealer's betting pool dimishes by half of currentbetamount.
        Requires a global variable named >currentbetamount<.
        """
        global currentbetamount
        self.bettingpool -= int(currentbetamount / 2)

    def bet_reset(self):
        """
        Resets the betting pool.
        """
        self.bettingpool = 0


# --------------------------------------------------PROGRAM-------------------------------------------------
from IPython.display import clear_output
import time
print_banner()
player_dict = {}
end_turn = False
time.sleep(1)
game_start_number_players()
clear_output()
print_banner()
player_status()
player_begin_game()
blackjack()
restart_game_check()