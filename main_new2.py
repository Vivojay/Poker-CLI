#PC HOLDEM POKER v0.2.0


#Imports#
import numpy as np
import matplotlib
import os
import json
import secrets

from tabulate import tabulate as tbl
from winner_finder import *
from compare_hands import *
from hand_ranker import *
from ascii_card_displayer import dispCards, _dispCards
from email_cards import SEND

#Changing directory#
_curDir = os.path.split(__file__)[0]
os.chdir(_curDir) #Change directory

if not os.path.exists('config.json'):
    with open('config.json', 'w') as f:
        f.write('')


#Reading config
try:
    with open('config.json', 'r') as f:
        loaded_round_info = json.load(f)
except json.decoder.JSONDecodeError:
        loaded_round_info = None


#Predefining Variables#
card_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_suits = ['C', 'S', 'H', 'D']
deck = [([j+i for j in card_ranks]) for i in card_suits] #All cards separated by suit
actions = ['fold', 'call', 'rais', 'check'] #rais is same as raise
pot = 0 #Money in the pot, starts at 0


#Printing Introduction#
with open ('res/intro.txt') as f:
    intro_banner = f.read()
print(intro_banner)

#Fucntion to display original money of each user in a tabular format
def MoneyTable():
    global all_users, money
    out = tbl(list(zip(all_users, money)), tablefmt = 'psql', headers=('Players', 'Money'))
    print('Current Money Distribution')
    print(out)

#Username inputs#
#Initializing list which will store all user_names
all_users = []

if loaded_round_info is not None: #Found saved game data
    print()
    print('We found a saved poker game')
    print()

    #Auto read blind values from last saved round
    small_blind_val = loaded_round_info[1]
    big_blind_val = small_blind_val*2

    print(f'Big Blind: {big_blind_val}')
    print(f'Small Blind: {small_blind_val}')
    print()

    #Auto read money from last saved round
    money = [ loaded_round_info[0][i][0] for i in loaded_round_info[0] ]

    #Get basic info of last saved round
    no_of_players = len(money)
    all_users = list(loaded_round_info[0].keys())

    MoneyTable()
    print()

    perm_to_continue = input('Do you want to continue this saved game? [y/n]\n(If you type [n], a new game will begin): ')
    while not perm_to_continue.lower() in ['y', 'n']:
        perm_to_continue = input('Invalid permission, continue from saved game? [y/n]: ')

    if perm_to_continue.lower() == 'n':
        all_users = []

        while True:
            try:
                small_blind_val = int((input('Enter the small blind value [between 1 and 10,000,000,000]: ')).replace(',', ''))
                if small_blind_val > 0 and small_blind_val < 10 ** 10:
                    break
                else:
                    print('Invalid blind value, please re-enter')
            except ValueError:
                print('Invalid blind value, please re-enter')

        big_blind_val = 2*small_blind_val

        init_money_val = int(input('Enter initial money amount [atleast ' + str(big_blind_val*40) + ']: '))
        while init_money_val < big_blind_val*40:
            init_money_val = input('Invalid amount, please re-enter: ').replace(',', '')

        no_of_players = input('How many players? [2 - 10]: ')
        while not int(no_of_players) in list(range(2, 11)):
            try:
                no_of_players = input('Invalid no. of players, please re enter [2 - 10]: ')
            except Exception:
                print('Invalid no. of players, please re enter [2 - 10]: ')

        money = [init_money_val for i in list(range(int(no_of_players)))] #Initial money of all users

        print()

        #Getting usernames and registering/logging them in a list named "all_users"
        for i in range(int(no_of_players)):
            if i == 0:
                suffix = 'st'
            elif i == 1:
                suffix = 'nd'
            elif i == 2:
                suffix = 'rd'
            else:
                suffix = 'th'

            #Get new user_name
            user_name = input('Please enter the '+str(i+1)+suffix+' username [case sensitive, no spaces]: ') #User Name prompt

            while (' ' in user_name or '\t' in user_name or '\n' in user_name or user_name == '' or user_name in all_users):
                if not user_name in all_users:
                    user_name = input('Invalid username, please try without spaces or tabs: ')
                elif user_name == '':
                    user_name = input('Username can\'t be empty: ')
                else:
                    user_name = input('This username is taken: ')

            else:
                #Append current user_name to all_users
                all_users.append(user_name)
                #Notify user that his user_name has been registered
                print('Username recorded\n')

        #Finally displaying all registered usernames
        print('-'*80)
        print('List of registered users:')
        for i in all_users:
            print(f'  \u2022 {i}')
        print('-'*80+'\n')

        Emails = []
        for i in all_users:
            Email = input(f'Enter Email ID of {i}: ')
            Emails.append(Email)

    else:
        Emails = []
        for i in all_users:
            Email = input(f'Enter Email ID of {i}: ')
            Emails.append(Email)

else:
    while True:
        try:
            small_blind_val = int(
                (input('Enter the small blind value [between 1 and 10,000,000,000]: ')).replace(',', ''))
            if small_blind_val > 0 and small_blind_val < 10 ** 10:
                break
            else:
                print('Invalid blind value, please re-enter')
        except ValueError:
            print('Invalid blind value, please re-enter')

    big_blind_val = 2 * small_blind_val

    init_money_val = int(input('Enter initial money amount [atleast ' + str(big_blind_val * 40) + ']: '))
    while init_money_val < big_blind_val * 40:
        init_money_val = input('Invalid amount, please re-enter: ')

    no_of_players = input('How many players? [2 - 10]: ')
    while not int(no_of_players) in list(range(2, 11)):
        no_of_players = input('Invalid no. of players, please re enter [2 - 10]: ')

    money = [init_money_val for i in list(range(int(no_of_players)))]  # Initial money of all users

    print()

    r'''
    small_blind_val = int(input('Enter the small blind value: '))
    big_blind_val = 2 * small_blind_val

    init_money_val = int(input('Enter initial money amount [atleast ' + str(big_blind_val * 40) + ']: '))
    while init_money_val < big_blind_val * 40:
        try:
            init_money_val = input('Invalid amount, please re-enter: ')
        except Exception:
            pass

    no_of_players = input('How many players? [2 - 10]: ')
    while not int(no_of_players) in list(range(2, 11)):
        try:
            no_of_players = input('Invalid no. of players, please re enter [2 - 10]: ')
        except Exception:
            pass

    money = [init_money_val for i in list(range(int(no_of_players)))]  # Initial money of all users

    print()
    '''

    # Getting usernames and registering/logging them in a list named "all_users"
    for i in range(int(no_of_players)):
        if i == 0:
            suffix = 'st'
        elif i == 1:
            suffix = 'nd'
        elif i == 2:
            suffix = 'rd'
        else:
            suffix = 'th'

        # Get new user_name
        user_name = input(
            'Please enter the ' + str(i + 1) + suffix + ' username [case sensitive, no spaces]: ')  # User Name prompt


        while (' ' in user_name or '\t' in user_name or '\n' in user_name or user_name == '' or user_name in all_users):
            if not user_name in all_users:
                user_name = input('Invalid username, please try without spaces or tabs: ')
            elif user_name == '':
                user_name = input('Username can\'t be empty: ')
            else:
                user_name = input('This username is taken: ')

        else:
            # Append current user_name to all_users
            all_users.append(user_name)
            # Notify user that his user_name has been registered
            print('Username recorded\n')

    # Finally displaying all registered usernames
    print('-' * 80)
    print('List of registered users:')
    for i in all_users:
        print(f'  \u2022 {i}')
    print('-' * 80 + '\n')

    Emails = []
    for i in all_users:
        Email = input(f'Enter Email ID of {i}: ')
        Emails.append(Email)


#Create/Overwrite Emails in file 'emails.json' in the same directory
with open('res/emails.json', 'w') as f:
    json.dump(Emails, f, indent=2)

#Randomly "shuffling" cards and dealing to the players#
all_cards = [j for i in deck for j in i]
preselected_cards = secrets.SystemRandom().sample(all_cards, int(no_of_players)*2 + 5)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

cards_on_table = preselected_cards[:5] #First 5 cards will be kept on the table when time comes
flop_cards = cards_on_table[:3]
turn_card = cards_on_table[3]
river_card = cards_on_table[4]

hole_card_pairs = list(chunks(preselected_cards[5:], 2)) #Remaining cards will be dealt as hole cards to all the users
hole_allotment = dict(zip(all_users, hole_card_pairs)) #These are allotted hole cards

#Create/Overwrite hole cards in file 'holes.json' in the same directory
with open('res/holes.json', 'w') as f:
    json.dump(hole_allotment, f, indent=2)

with open('res/emails.json') as f:
    Email_IDs = json.load(f)

SEND()

input('WARNING: Press [enter] to continue only AFTER everyone receives their cards via their email: ')


#Starting the card rounds#
#Preflop#
"""First Street of Poker"""

#Deduct blinds from first two players and add it to the pot#
money = [money[0]-small_blind_val]+ [(i-big_blind_val) for i in money[1:]]
pot += small_blind_val + big_blind_val*(len(all_users)-1)

print()

def new_street_input():
    input('Hit [enter] to proceed to the next street: ')

input('Hit [enter] to proceed to the first street: ')

print('-'*80)

print('\nFirst Street [The Preflop]')
running_amount = big_blind_val
print('Current bet amount:', running_amount)
print()
print(f'>> Pot: {pot}')
print()


print('Small blind of ', small_blind_val, ' deducted from [', all_users[0], ']', sep = '')
print('Big blind of', big_blind_val, 'deducted from all others')
print()

auto_winner = False

def s(i, j):
    global action, money, all_users, running_amount, raise_amt, old_running_amount, pot, foldedUser, k, auto_winner

    if not len(all_users) == 1:
        #Ask for action until validated
        action = input('['+j+' ('+ str(money[all_users.index(j)]) +')] > ')
        # while not action in 'f;c;r;k;a'.split(';'):
        while not action in 'c;r;a;f'.split(';'):
            action = input('['+j+'] (Invalid command) > ')

        #Raise
        if action == 'r':
            if money[all_users.index(j)] >= 2*running_amount:
                raise_amt = input('Enter new amount to raise to [Atleast '+str(2*running_amount)+']: ')

            if raise_amt == 'x':
                flag = True
            if raise_amt.strip() == '':
                flag = False
            if raise_amt.strip() != '' and type(eval(raise_amt)) == int and int(raise_amt) >= 2*int(running_amount):
                flag = True
            else:
                flag = False

            while not flag:
                try:
                    raise_amt = input('Invalid raise amount, please retry [Atleast '+str(2*running_amount)+'] [To exit raise, enter "x"]: ')
                    if raise_amt == 'x':
                        flag = True
                    elif raise_amt.strip() == '':
                        pass
                    elif raise_amt.strip() != '' and type(eval(raise_amt)) == int and int(raise_amt) >= 2*int(running_amount):
                        flag =  True
                except Exception:
                    pass


            if raise_amt != 'x':
                k += 1
                if money[all_users.index(j)] > int(raise_amt):
                    raise_amt = int(raise_amt)
                    #Increase the running_amount to raised value
                    old_running_amount = running_amount
                    running_amount = raise_amt
                    #Then, deduct this increased running_amount
                    money[all_users.index(j)] -= running_amount
                    pot += running_amount

                    print('>> [', j, ' (', money[all_users.index(j)], ')] has raised ', old_running_amount, ' to ', running_amount, sep = '')
                    print()

                else:
                    print("Not enough, you need atleast", str(raise_amt)+', you have', money[all_users.index(j)])
                    s(i, j)

                    # raise_amt = input('Invalid raise amount, please retry [Atleast '+str(2*running_amount)+']: ')
                    # raise_amt = int(raise_amt)


        elif action == 'c':
            if money[all_users.index(j)] > running_amount:
                k += 1
                # print(money[all_users.index(j)] , running_amount, money[all_users.index(j)] > running_amount)
                #Deduct running_amount from current player
                money[all_users.index(j)] -= running_amount
                pot += running_amount

                print('>> [', j, ' (', money[all_users.index(j)], ')] has called ', running_amount, sep = '')

            else:
                print('You can\'t call, go all-in or fold')
                s(i, j)

            print()
            
        #Following actions have not been implemented
        if action == 'a':
            # print('Going all-in is an unimplemented feature as of now. . .')
            foldedUser = j
            del money[all_users.index(j)]
            all_users.remove(j)

            print(f'User [{j}] went all-in and is out of the game now')

            j = all_users[k]
            s(i, j)

        elif action == 'f':
            # print('Folding is an unimplemented feature as of now. . .')
            foldedUser = j
            del money[all_users.index(j)]
            all_users.remove(j)

            print(f'User [{j}] folded and is out of the game now')

            j = all_users[k]
            s(i, j)

        elif action == 'k':
            print('Checking is an unimplemented feature as of now. . .')
            s(i, j)
    
    else:
        auto_winner = True
    
for i in range(2): #i is the user index
    k = 0
    while k < len(all_users) and not auto_winner:
        j = all_users[k]
        try:
            s(i, j)
        except Exception:
            print('Error') # Skip the folded/broke player
            raise
    else:
        if len(all_users) == 0:
            break
        else:
            k = 0

    print(('___ '*3)[:-1])
    print()


if not auto_winner:
    #Flop round#
    """Second Street of Poker"""
    print('-'*80)

    new_street_input()

    print('\nSecond Street [The Flop]\n')

    users_in_game = ', '.join(all_users)
    print('Currently playing users are: {users_in_game}')
    print()

    print('Flop cards are:')
    dispCards(*[i.replace('10', 'T') for i in flop_cards])
    print()

    print('Current bet amount:', running_amount)
    print()
    print(f'>> Pot: {pot}')
    print()

    for i in range(2): #i is the user index
        k = 0
        while k < len(all_users) and not len(all_users) == 1:
            j = all_users[k]
            try:
                s(i, j)
            except Exception:
                print('Error') # Skip the folded/broke player
                raise
        else:
            if len(all_users) == 0:
                break
            else:
                k = 0

        print(('___ '*3)[:-1])
        print()


if not auto_winner:
    #Turn round#
    """Third Street of Poker"""
    print('-'*80)

    new_street_input()

    print('Third Street [The Turn]\n')

    users_in_game = ', '.join(all_users)
    print('Currently playing users are: {users_in_game}')
    print()

    print('Community cards are:')
    dispCards(* [i.replace('10', 'T') for i in flop_cards] + [turn_card.replace('10', 'T')] )
    print()

    # print('Community cards are', ', '.join(flop_cards))
    print('Current bet amount:', running_amount)
    print()
    print(f'>> Pot: {pot}')
    print()

    for i in range(2): #i is the user index
        k = 0
        while k < len(all_users) and not len(all_users) == 1:
            j = all_users[k]
            try:
                s(i, j)
            except Exception:
                print('Error') # Skip the folded/broke player
                raise
        else:
            if len(all_users) == 0:
                break
            else:
                k = 0

        print(('___ '*3)[:-1])
        print()


if not auto_winner:
    #River round#
    """Fourth Street of Poker"""
    print('-'*80)

    new_street_input()

    print('Fourth Street [The River]\n')

    users_in_game = ', '.join(all_users)
    print('Currently playing users are: {users_in_game}')
    print()

    print('Community cards are:')
    dispCards(* [i.replace('10', 'T') for i in flop_cards] + [turn_card.replace('10', 'T')] + [river_card.replace('10', 'T')] )
    print()
    # print('Current bet amount:', running_amount)
    print()
    print(f'>> Pot: {pot}')
    print()

    for i in range(2): #i is the user index
        k = 0
        while k < len(all_users) and not len(all_users) == 1:
            j = all_users[k]
            try:
                s(i, j)
            except Exception:
                print('Error') # Skip the folded/broke player
                raise
        else:
            if len(all_users) == 0:
                break
            else:
                k = 0

        print(('___ '*3)[:-1])
        print()


#The Showdown#
print('='*80)
print('The SHOWDOWN\n')
if not auto_winner:
    users_in_game = ', '.join(all_users)
    print('Currently playing users are: {users_in_game}')
    print()

    print()
    print('Final money in the pot:', pot)
    print()

    input('Press [enter] to show cards of all players and announce the winner: ')
    print()

    for i in hole_allotment:
        print(f'Player [{i}] has hole cards: ')
        dispCards (*[i.replace("10", "T") for i in hole_allotment[i]] )
        print()

    print('\n'*2)

    input('Please hit [enter] to see the final hands of each player: ')

else:
    user_left_in_game = all_users[0]
    print(f'The only user left is: {user_left_in_game}')

    print()
    print('Final money in the pot:', pot)
    print()

    for i in hole_allotment:
        print(f'Player [{i}] has hole cards: ')
        dispCards (*[i.replace("10", "T") for i in hole_allotment[i]] )
        print()

    print('\n'*2)

#Final Calculations#
def get_best_hand_of_user(user):
    global cards
    cards = hole_allotment[user]+cards_on_table
    best_hand = get_best_hand(cards)
    return (show_cards(best_hand), evaluate_hand(best_hand))


final_hands = []
for i in all_users:
	final_hands.append(' '.join(get_best_hand_of_user(i)[0]))
final_hands = [i.replace('10', 'T') for i in final_hands]

final_hands_original = final_hands

# print(tbl(list(zip(all_users, final_hands_original)), headers=('Player', 'Cards'), tablefmt='psql'))
# print table with all cards

def narrow_winners():
    global final_hands, remaining, a

    if bool(len(final_hands) % 2):
        remaining = final_hands[-1]
    else:
        remaining = ''

    a = []

    for i in range(0, len(final_hands)-1, 2):
        if (PokerHand(final_hands[i]).compare_with(PokerHand(final_hands[i+1]))):
            a.append(final_hands[i])
        else:
            a.append(final_hands[i+1])

    a.append(remaining)
    final_hands = a

    return(final_hands)

flag = True
while flag:
    narrow_winners()
    if narrow_winners()[-1] == '' or len(narrow_winners()) == 1:
        flag = False

if len(narrow_winners()) == 1:
    winner = all_users[0]
    # auto_winner = True
else:
    winner = all_users[final_hands_original.index(final_hands[0])]


print(tbl
        (list
            (zip
                (
                    [f'Winner >> [{i}]' if i is winner else i for i in all_users],
                    final_hands_original,
                    
                    [_dispCards(*k) for k in \
                        [i.replace('10', 'T').split() for i in final_hands_original]
                    
                    ]
                )
            ),
                    
        headers = (
                    'Player',
                    'Cards',
                    ''
                  ),

        tablefmt='psql'
        
        )
    )

win_msg = f"player [{winner}] won with '{get_best_hand_of_user(winner)[1]}'\nCards are: {'['+', '.join(get_best_hand_of_user(winner)[0])+']'}"

print()
print(win_msg)
print()

print()
print(f'The pot amount of {pot} has been transferred to player [{winner}]')

money[all_users.index(winner)] += pot #Transfer pot amount to winner
pot = 0 #Empty the pot
print('~'*80)

round_info = [ dict(zip(all_users, zip(money, final_hands_original, hole_card_pairs))), small_blind_val]

try:
    with open('config.json', 'w') as f:
        json.dump(round_info, f, indent=2)

    print('The current game has been saved')

except Exception:
    print("Error saving: This game could not be saved")
