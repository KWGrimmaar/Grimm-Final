import random

def createDeck():
    suits = []
    ranks=[]
    deck={}
    try:
        cardsfile=open("CardSuitesandRanks.csv", "r")
        for line in cardsfile:
            line=line.strip()
            row=line.split(",")
            suits.append(row[0])
            for i in range(1,len(row)):
                ranks.append(row[i])
        cardsfile.close()
        #print (suits)
        #print(ranks)
    except FileNotFoundError:
        print("File doesn't exist")
    for suit in suits:
        for rank in ranks:
            value = 0
            if rank == "Ten" or rank == "Jack" or rank == "Queen" or rank == "King": value = 10
            elif rank == "Ace": value = 1
            elif rank == "Two": value = 2
            elif rank == "Three": value = 3
            elif rank == "Four": value = 4
            elif rank == "Five": value = 5
            elif rank == "Six": value = 6
            elif rank == "Seven": value = 7
            elif rank == "Eight": value = 8
            elif rank == "Nine": value = 9
            deck[rank + " of " + suit] = value 
    
    return deck

def startMenu():
    print("This is a card guessing game. You will need to guess the value of randomly selected cards.")
    menuSelect =str(input("Make your selection \n1. Play \n2. Leaderboards \n3. Exit \n---------------------\n"))
    menuSelect = menuSelect.lower()
    menuSelect = menuSelect.replace(" ", "")
    menuSelect = menuSelect.replace(".", "")
    #print(menuSelect) #confirms menuSelect has been stripped and lowered
    while True:
        if menuSelect == "1" or menuSelect == "play" or menuSelect == "1play":
            guessingGame()
            break
        elif menuSelect == "2" or menuSelect == "leaderboards" or menuSelect == "2leaderboards":
            print("\nLeaderboards \nPlayer | Score\n-------------")
            try:
                leaderboard=open("leaderboard.csv", "r")
                #print(leaderboard)
                for line in leaderboard:
                    line=line.strip()
                    row=line.split(",")
                    initials = row [0]
                    score = row [1]
                    #print(len(row), len(line))
                    print(initials,"   |", str(score))
                    #suits.append(row[0])
                    #for i in range(1,len(row)):
                        #ranks.append(row[i])
                    
            except FileNotFoundError:
                   print("File doesn't exist")     
            menuSelect =str(input("\nReturning to menu. \nMake your selection \n1. Play \n 2. Leaderboards \n 3. Exit \n---------------------\n"))    
        elif menuSelect == "3" or menuSelect == "exit" or menuSelect == "3exit":
            print("Exiting")
            break    
        else:
            print("Invalid choice.")
            menuSelect =input("Make your selection \n1. Play \n 2. Leaderboards \n 3. Exit \n---------------------\n")

def initialsGather():
    while True:
        try:
            initials= input("Please enter your initials. ")
            initials = initials.upper()
            initials = initials[0:3]
            while initials[0] == " " or initials[1] == " " or initials[2] == " ":
                print("You didn't enter three characters. Try again")
                initials= input("Please enter your initials. ")
                initials = initials.upper()
                initials = initials[0:3]
                
        except IndexError:
            print("You didn't enter three characters. Try again")
            continue # https://stackoverflow.com/questions/2083987/how-to-retry-after-exception
        print("Your initals are", initials)
        break
    return initials

def guessingGame():
    #print("Guessing game", initials)
    startGame = input("Press Enter to begin or type stop to end: ")
    startGame = startGame.lower()
    startGame = startGame.replace(" ", "")
    if startGame == "stop":
            print ("Game Over")
            quit()
    count=1
    score = 0
    deck = createDeck()
    remainingCards=len(deck)
    #print(len(deck))
    initials = initialsGather()
    if startGame == "":
        for card in range(52):
            points = 20
            card_value = 0 
            card = {} 
            if len(deck) == 0:
                print("Congratulations. You've guessed every card!")
                try:
                    print("Your score was", score, "after", count, "cards\n")
                    uploadScore=input("Upload scores?\n Yes \n No \n -----\n")
                    uploadScore=uploadScore.strip()
                    uploadScore=uploadScore.lower()
                    if uploadScore == "y" or uploadScore == "yes":
                        print("Uploading")
                        leaderboard=open("leaderboard.csv","a")
                        leaderboard.write(initials+","+str(score)+"\n")
                        leaderboard.close()
                    if uploadScore == "n" or uploadScore == "no":
                        print("Thanks for playing!")
                        quit()
                except:
                    print("Invalid entry. \n")
            random_card = random.choice(list(deck.keys()))
            val = deck[random_card]
            card_value += val
            card[random_card] = val
            #print(random_card) # For testing card is correctly drawn and comparison to value
            #print(card_value) # For testing value is correct and compare to card drawn
            print("Card", str(count) + ".", str(remainingCards - 1), "cards remain." )       
            try:
                guess=input("\nGuess the value of the card. \n")
                if guess == "stop":
                    if score == 0:
                        print("Score is not high enough to submit.")
                    if score != 0:
                        try:
                            print("Your score was", score, "after", count, "cards\n")
                            uploadScore=input("Upload scores?\n Yes \n No \n -----\n")
                            uploadScore=uploadScore.strip()
                            uploadScore=uploadScore.lower()
                            if uploadScore == "y" or uploadScore == "yes":
                                print("Uploading")
                                leaderboard=open("leaderboard.csv","a")
                                leaderboard.write(initials+","+str(score)+"\n")
                                leaderboard.close()
                                #endGame(initials, score)
                            if uploadScore == "n" or uploadScore == "no":
                                print("Thanks for playing!")
                                quit()
                        except:
                            print("Invalid entry. \n")
                            continue
                    break
                guess= int(guess)
            except ValueError:
                print("Numerical guesses only. Try again.")
                guess=(input("Guess the value of the card. "))
            while guess != int(card_value):
                if int(guess) < int(card_value):
                    if points < 0:
                        points = 0
                    print("Higher")
                    points -=2
                    #print("Lost 2 points", points)
                    try:
                        guess=int(input("Guess the value of the card. "))
                    except ValueError:
                        print("Numerical guesses only. Try again.")
                        guess=int(input("Guess the value of the card. "))
                elif int(guess) > int(card_value):
                    print("Lower")
                    points -=2
                    #print("Lost 2 points", points)
                    if points < 0:
                        points = 0
                    try:
                        guess=int(input("Guess the value of the card. "))
                    except ValueError:
                        print("Numerical guesses only. Try again.")
                        guess=int(input("Guess the value of the card. ")) 
            if guess == "int(card_value)":
                count +=1
                deck.pop(random_card)
                print("\nCorrect!", "Your card was the", random_card)
                print("You gained",points,"points.")
                score += points
                print("Your total score is",score)
            remainingCards-=1   
    else:
        print("Invalid Entry. Press Enter to begin or type stop to end: ")
        startGame = input("Press Enter to begin or type stop to end: ")
    
                        
startMenu()
