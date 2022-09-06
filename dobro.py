from os import urandom

allNaipes="0ABCD"

class Card:
    def __init__(self, naipe, rank):
        self.naipe=naipe
        self.rank=rank
    def str(self):
        #print ("I'm inside Card.str().")
        return self.naipe+str(self.rank)
    def __eq__(self, other):
        return ((self.naipe==other.naipe) and (self.rank==other.rank))
def cardFromName (name):
    naipe=name[0]
    rank = int (name[1])
    if len(name)>2:
        rank = (rank*10)+int(name[2])
    ret = Card (naipe, rank)
    return ret
class Pack:
    def __init__(self, cards=[]):
        self.cards=cards
        if len(self.cards)==0:
            n=1
            while n<5:
                r=1
                while r<14:
                    self.cards.append(Card(allNaipes[n],r))
                    r=r+1
                n=n+1
    def randomize (self):
         l = []
         while len(self.cards)>0:
                card = self.cards[int(urandom(1)[0])%len(self.cards)]
                l.append(card)
                self.cards.remove(card)
         self.cards=l
    def getHand(self):
        ret = []
        ret.append(self.cards.pop())
        ret.append(self.cards.pop())
        ret.append(self.cards.pop())
        return ret
def handStr (hand):
    ret=""
    i=0
    while i<len(hand):
        ret+=hand[i].str()
        if i<(len(hand)-1):
            ret+=", "
        i=i+1
    return ret
def handGetNOfficials(hand):
    n=0
    for card in hand:
        if card.rank>10:
            n=n+1
    return n
def handGetHighestCard (hand):
    if len(hand)==1:
        return hand[0]
    ret = hand[0]
    for card in hand:
        if card.rank>ret.rank:
            ret=card
    return ret
currentHand=0
playerPoints=0
computerPoints=0
while currentHand<12:
    print ("This is hand "+str(currentHand)+".")
    print ("I have "+str(computerPoints)+" points.")
    print ("You have "+str(playerPoints)+" points.")
    currentHandValue=1
    pack=Pack()
    pack.randomize()
    computerHand=pack.getHand()
    #print ("My hand is:", handStr(computerHand))
    playerHand=pack.getHand()
    print ("Your hand is:", handStr(playerHand))
    answer = 'y'
    while ((answer[0]=='y') or (answer[0]=='Y')) and (currentHandValue<8):
        print ("The current hand value is "+str(currentHandValue)+".")
        answer=input ("Do you want to double? Answer y or n:")
        if (answer[0]=='y') or (answer[0]=='Y'):
            currentHandValue*=2
    answer='y'
    computerDesiresHandValue = 2**handGetNOfficials(computerHand)
    while ((answer[0]=='y') or (answer[0]=='Y')) and (currentHandValue<computerDesiresHandValue):
        print ("The current hand value is "+str(currentHandValue)+".")
        answer=input("I want to double. Do you accept to double?\nAnswer y or n: ")
        if (answer[0]=='y') or (answer[0]=='Y'):
            currentHandValue*=2
        elif (answer[0]=='n') or (answer[0]=='N'):
            computerPoints+=currentHandValue
        else:
            print ("Unrecognized option.")
            answer='y'
    if (answer[0]=='n') or (answer[0]=='N'):
        currentHand+=1
        continue
    intraComputerPoints=0
    intraPlayerPoints=0
    vez=0
    while (vez<3) and (intraComputerPoints<2) and (intraPlayerPoints<2):
        cardName = input("Enter the card you want to play: ")
        playerCard = cardFromName (cardName)
        if playerCard in playerHand:
            playerHand.remove(playerCard)
        else:
            print ("You don't have such card.")
            continue
        computerCard = handGetHighestCard (computerHand)
        computerHand.remove (computerCard)
        print ("I play "+computerCard.str()+".")
        if playerCard.rank>computerCard.rank:
            print ("You made an intra point.")
            intraPlayerPoints+=1
        elif computerCard.rank>playerCard.rank:
            print ("I made an intra point.")
            intraComputerPoints+=1
        else:
            print ("Our cards have the same rank.")
        vez+=1
    if intraPlayerPoints>intraComputerPoints:
        print ("You won this hand.")
        playerPoints+=currentHandValue
    elif intraComputerPoints>intraPlayerPoints:
        print ("I won this hand.")
        computerPoints+=currentHandValue
    else:
        print ("This hand had no winner.")
    currentHand = currentHand+1
print ("I made "+str(computerPoints)+" points.")
print("You made "+str(playerPoints)+" points.")
if playerPoints>computerPoints:
    print ("You won this game.")
elif computerPoints>playerPoints:
    print ("You lost. I won this game.")
else:
    print ("The game ended in a draw.")
