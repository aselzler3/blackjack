# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 14:46:58 2018

@author: Andrew Selzler
"""
import random
import matplotlib.pyplot as plt
import numpy as np

def create_deck(n_decks):
    D=[]
    for _ in range(n_decks):
        for i in range(2,10):
            for j in range(4):
                D.append(i)
        for i in range(16):
            D.append(10)
        for i in range(4):
            D.append(11)
    return D

def reduce(l):
    c=l.copy()
    if 11 in c:
        for i in range(len(c)):
            if c[i]==11:
                c[i]=1
                break
    return c

def player_hand_make(deck, dealer_hand, player_hand, split=False):
    double=False
    first_draw=True
    while True:
        #Special case if you are dealt 2 aces
        if first_draw:
            if player_hand[0]==11 and player_hand[1]==11 and not split:
                print('Dealer Hand')
                print('{} {}'.format(dealer_hand[0], 'X'))
                print()
                print('Player Hand')
                print(' '.join([str(player_hand[i]) for i in range(len(player_hand))]))
                print()
                X=input('H, S, D, or Split?')
                if X=='H':
                    player_hand.append(deck.pop())
                    first_draw=False
                elif X=='S':
                    player_hand=reduce(player_hand)
                    return (player_hand, double)
                elif X=='D':
                    player_hand.append(deck.pop())
                    while sum(player_hand)>21:
                        if 11 in player_hand:
                            player_hand=reduce(player_hand)
                        else:
                            print(' '.join([str(player_hand[i]) for i in range(len(player_hand))]))
                            return (player_hand, double)
                        
                    print(' '.join([str(player_hand[i]) for i in range(len(player_hand))]))
                    double=True
                    return (player_hand, double)
                elif X=='Split':
                    hand_1=player_hand_make(deck, dealer_hand, [player_hand[0], deck.pop()],split=True)
                    #print(hand_1)
                    hand_2=player_hand_make(deck, dealer_hand, [player_hand[1], deck.pop()], split=True)
                    #print(hand_2)
                    return [hand_1,hand_2]
                else:
                    print('not valid command')
        #All other cases
        while sum(player_hand)>21:
            if 11 in player_hand:
                player_hand=reduce(player_hand)
            else:
                print(' '.join([str(player_hand[i]) for i in range(len(player_hand))]))
                return (player_hand, double)
        print('Dealer Hand')
        print('{} {}'.format(dealer_hand[0], 'X'))
        print()
        print('Player Hand')
        print(' '.join([str(player_hand[i]) for i in range(len(player_hand))]))
        print()
        if first_draw:
            if (player_hand[0]!=player_hand[1] or split):
                X=input('H, S, or D? ')
                if X=='H':
                    player_hand.append(deck.pop())
                    first_draw=False
                elif X=='S':
                    return (player_hand, double)
                elif X=='D':
                    player_hand.append(deck.pop())
                    print(' '.join([str(player_hand[i]) for i in range(len(player_hand))]))
                    double=True
                    return (player_hand, double)
                else:
                    print('not valid command')
            else:
                X=input('H, S, D, or Split?')
                if X=='H':
                    player_hand.append(deck.pop())
                    first_draw=False
                elif X=='S':
                    return (player_hand, double)
                elif X=='D':
                    player_hand.append(deck.pop())
                    print(' '.join([str(player_hand[i]) for i in range(len(player_hand))]))
                    double=True
                    return (player_hand, double)
                elif X=='Split':
                    hand_1=player_hand_make(deck, dealer_hand, [player_hand[0], deck.pop()],split=True)
                    #print(hand_1)
                    hand_2=player_hand_make(deck, dealer_hand, [player_hand[1], deck.pop()], split=True)
                    #print(hand_2)
                    return [hand_1,hand_2]
                else:
                    print('not valid command')
        else:
            X=input('H or S? ')
            if X=='H':
                player_hand.append(deck.pop())
            elif X=='S':
                return player_hand, double

def dealer_hand_make(deck, dealer_hand):
    while True:
        print()
        print('Dealer Hand')
        print(' '.join([str(dealer_hand[i]) for i in range(len(dealer_hand))]))
        while sum(dealer_hand)>21:
            if 11 not in dealer_hand:
                return dealer_hand
            else:
                dealer_hand=reduce(dealer_hand)
        if sum(dealer_hand)<17:
            dealer_hand.append(deck.pop())
        else:
            return dealer_hand
        
def interactive_hand(deck, dealer_hand, player_hand):
    #Check for blackjacks and dealer 21's
    if sum(player_hand)==21:
        return("blackjack, you win")
    if sum(dealer_hand)==21:
        return('dealer 21, you lose')
    player_hands=player_hand_make(deck, dealer_hand, player_hand)
    # If player busts, dealer should not draw cards
    if type(player_hands[0][0])==list:
        if sum(player_hands[0][0])>21 and sum(player_hands[1][0])>21:
            return ['you lose', 'you lose']
    elif sum(player_hands[0])>21:
        return 'you lose'
    #Outcome for split hands
    dealer_hand=dealer_hand_make(deck, dealer_hand)
    if type(player_hands[0][0])==list:
        result=[]
        i=1
        for P in player_hands:
            hand=P[0]
            DD=P[1]
            print()
            print('hand '+str(i))
            print()
            print('Player Total: '+str(sum(hand)))
            print()
            print('Dealer Total: '+str(sum(dealer_hand)))
            if DD:
                if sum(hand)<=21:
                    if sum(hand)>sum(dealer_hand) or sum(dealer_hand)>21:
                        result.append('you win double')
                    elif sum(dealer_hand)>sum(hand):
                        result.append('you lose double')
                    else:
                        result.append('push')
                else:
                    result.append('you lose double')
            else:
                if sum(hand)<=21:
                    if sum(hand)>sum(dealer_hand) or sum(dealer_hand)>21:
                        result.append('you win')
                    elif sum(dealer_hand)>sum(hand):
                        result.append('you lose')
                    else:
                        result.append('push')
                else:
                    result.append('you lose')
            i+=1
        return result
    #Outcome for individual hands
    else:
        DD=player_hands[1]
        hand=player_hands[0]
        print()
        print('Player Total: '+str(sum(hand)))
        print()
        print('Dealer Total: '+str(sum(dealer_hand)))
        if DD:
            if sum(hand)>21:
                return('you lose double')
            if sum(hand)>sum(dealer_hand) or sum(dealer_hand)>21:
                return('you win double')
            elif sum(dealer_hand)>sum(hand):
                return('you lose double')
            else:
                return('push')
        else:
            if sum(hand)>21:
                return('you lose')
            if sum(hand)>sum(dealer_hand) or sum(dealer_hand)>21:
                return('you win')
            elif sum(dealer_hand)>sum(hand):
                return('you lose')
            else:
                return('push')
        
def interactive_session(n_decks, account):
    deck=create_deck(n_decks)
    random.shuffle(deck)
    print('Welcome to Blackjack')
    K='y'
    while K=='y':
        print('Account Value: '+str(account))
        bet=int(input('Bet size? '))
        player_hand=[deck.pop(), deck.pop()]
        dealer_hand=[deck.pop(), deck.pop()]     
        hand=interactive_hand(deck, dealer_hand, player_hand)
        print(hand)
        if type(hand)==list:
            for x in hand:
                if x=='you win':
                    account+=bet
                elif x=='you lose':
                    account-=bet
                elif x=='you win double':
                    account+=bet*2
                elif x=='you lose double':
                    account-=bet*2
        else:
            if hand=='you win':
                account+=bet
            elif hand=='you lose':
                account-=bet
            elif hand=='you win double':
                account+=bet*2
            elif hand=='you lose double':
                account-=bet*2
            elif hand=='blackjack, you win':
                account+=bet*1.5
            elif hand=='dealer 21, you lose':
                account-=bet
        K=input('Play again? (y/n) ')
        
def test_hand(player_hand, dealer_hand):
    account=0
    bet=10
    deck=create_deck(2)
    random.shuffle(deck)
    hand=interactive_hand(deck, dealer_hand, player_hand)
    print(hand)
    if type(hand)==list:
        for x in hand:
            if x=='you win':
                account+=bet
            elif x=='you lose':
                account-=bet
            elif x=='you win double':
                account+=bet*2
            elif x=='you lose double':
                account-=bet*2
    else:
        if hand=='you win':
            account+=bet
        elif hand=='you lose':
            account-=bet
        elif hand=='you win double':
            account+=bet*2
        elif hand=='you lose double':
            account-=bet*2
        elif hand=='blackjack, you win':
            account+=bet*1.5
        elif hand=='dealer 21, you lose':
            account-=bet
    return account



        
        
    