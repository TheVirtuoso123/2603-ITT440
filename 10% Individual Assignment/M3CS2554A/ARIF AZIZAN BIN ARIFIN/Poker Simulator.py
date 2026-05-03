# Poker Game Simulator

# Modules for the poker game
# random module to shuffle the deck and draw cards
import random
# combinations from itertools to evaluate the best hand
from itertools import combinations
# Counter from collections to count the occurrences of ranks and suits
from collections import Counter

# Modules for the simulation of sequential and parallel techniques
# os module to check if log file exists
import os
# threading module for concurrent technique (threading)
import threading
# multiprocessing module to work for parallel technique
# multiprocessing module to get the number of CPU cores
import multiprocessing
# time module to measure the execution time of techniques
import time
# tqdm module to create a progress bar for the simulations
from tqdm import tqdm

#concurrent tech (threading) done
#parallel tech (multiprocessing) done
#sequential (benchmarking) done
 
# Constant data and files
# Log file to store the results of poker hand from simulations
logFile = "poker_simulation.log"
# Get the number of CPU cores for parallel technique
numCores = multiprocessing.cpu_count()

# Class to play a poker game
class pokerGame:
    def __init__(self, numPlayer):
        # Get is the number of players in the game (excluding the dealer)
        self.numPlayer = numPlayer - 1
        # Create a deck and shuffle it
        self.deck = self.createDeck()
        # Set the order of card drawn
        self.cardIndex = 0
        # Array to store user's hand, other players' hands, and dealer's cards
        self.userHand = []
        self.playersHands = []
        self.dealerCards = []

    # Create a standard 52-card deck
    def createDeck(self):
        suits = ['spades', 'hearts', 'clubs', 'diamonds']
        deck = [(value, suit) for value in range(2, 15) for suit in suits]
        # Shuffle the deck to randomize the order of cards
        random.shuffle(deck)
        return deck
    
    # Draw a card from the deck to determine the order of card drawn
    # When a card is drawn, the card index will increase by 1
    def drawCard(self):
        card = self.deck[self.cardIndex]
        self.cardIndex += 1
        return card

    # Deal cards to all players and dealer
    def dealCards(self):
        # User draws 2 cards
        self.userHand = [self.drawCard() for _ in range(2)]

        # Each other player draws 2 cards
        for _ in range(self.numPlayer):
            playerHand = [self.drawCard() for _ in range(2)]
            self.playersHands.append(playerHand)
        
        # Dealer draws 5 cards
        self.dealerCards = [self.drawCard() for _ in range(5)]

    # Check if the hand is a straight (5 cards in sequence)
    def isStraight(self, rankList):
        # Sort the ranks
        sortedRanks = sorted(rankList)

        # Check for regular straight (e.g., 5-6-7-8-9)
        # First check difference between highest and lowest rank is 4
        # Then check all ranks are unique (to avoid cases like 4-6-6-7-8)
        if sortedRanks[-1] - sortedRanks[0] == 4 and len(set(sortedRanks)) == 5:
            return True
        
        # Check for Ace-low straight (A-2-3-4-5)
        # Ace can be low (1) or high (14)
        if sortedRanks == [2, 3, 4, 5, 14]:  
            return True
        
        # If neither condition is met, it's not a straight
        return False

    # Evaluate the combinations of the 5 card
    # This function give values for the combinations to be ranked
    # Also included tie breaker by compariong the suits
    def evaluateHand(self, availableCards):
        # Ranks:
        # 10: Royal Flush
        # 9: Straight Flush
        # 8: Four of a Kind
        # 7: Full House
        # 6: Flush
        # 5: Straight
        # 4: Three of a Kind
        # 3: Two Pair
        # 2: One Pair
        # 1: High Card

        # Get ranks list
        rankList = [card[0] for card in availableCards]
        # Get suits list
        suitList = [card[1] for card in availableCards]

        # Count how many times each rank occurs
        rankCounts = Counter(rankList)

        # Sort the list of counts of each ranks
        # Reverse to have the highest count first
        countsList = sorted(rankCounts.values(), reverse=True)

        # Get unique ranks for tie breaker
        # Reverse to have the highest count first
        uniqueRanks = sorted(rankCounts.keys(), reverse=True)

        # Check for flush (all cards have the same suit)
        isFlush = (len(set(suitList)) == 1)
        # Check for straight (5 cards in sequence)
        isStraight = self.isStraight(sorted(rankList))

        #check ther rank of straight (for tie breaker)
        if isStraight:
            highRank = max(rankList)
            # Check for Ace-low straight (A-2-3-4-5)
            if set(rankList) == {14, 5, 4, 3, 2}:
                highRank = 5
            straightRank = highRank
        else:
            straightRank = 0

        # Check the hand type
        # Check for Straight Flush
        if (isFlush and isStraight):
            # Royal Flush
            if set(rankList) == {10, 11, 12, 13, 14}:
                return (9, straightRank), "Royal Flush"
            # Straight Flush
            return (8, straightRank), "Straight Flush"
        # Check for Four of a Kind
        elif countsList == [4, 1]:
            # quadRank and kickerRank for tie breaker
            quadRank = [rank for rank, count in rankCounts.items() if count == 4][0]
            kickerRank = [rank for rank, count in rankCounts.items() if count == 1][0]
            return (7, quadRank, kickerRank), "Four of a Kind"
        # Check for Full House
        elif countsList == [3, 2]:
            # tripRank and pairRank for tie breaker
            tripRank = [rank for rank, count in rankCounts.items() if count == 3][0]
            pairRank = [rank for rank, count in rankCounts.items() if count == 2][0]
            return (6, tripRank, pairRank), "Full House"
        # Check for Flush
        elif isFlush:
            return (5, tuple(sorted(uniqueRanks, reverse=True))), "Flush"
        # Check for Straight
        elif isStraight:
            return (4, straightRank), "Straight"
        # Check for Three of a Kind
        elif countsList == [3, 1, 1]:
            tripRank = [rank for rank, count in rankCounts.items() if count == 3][0]
            kickerRanks = tuple(sorted([rank for rank, count in rankCounts.items() if count == 1], reverse=True))
            return (3, tripRank, kickerRanks), "Three of a Kind"
        # Check for Two Pair
        elif countsList == [2, 2, 1]:
            pairRanks = sorted([rank for rank, count in rankCounts.items() if count == 2], reverse=True)
            kickerRank = [rank for rank, count in rankCounts.items() if count == 1][0]
            return (2, pairRanks[0], pairRanks[1], kickerRank), "Two Pair"
        # Check for One Pair
        elif countsList == [2, 1, 1, 1]:
            pairRank = [rank for rank, count in rankCounts.items() if count == 2][0]
            kickerRanks = tuple(sorted([rank for rank, count in rankCounts.items() if count == 1], reverse=True))
            return (1, pairRank, kickerRanks), "One Pair"
        # High Card        
        else:
            return (0, tuple(sorted(uniqueRanks, reverse=True))), "High Card"

    # Find the best 5-card poker hand from the 7 cards (user's + dealer's cards)
    def findBestHand(self, availableCards):
        bestHand = None
        bestRank = None
        bestPokerHand = None

        # Find all possible 5-card combinations from the available cards
        for combo in combinations(availableCards, 5):
            # Evaluate the rank of the current combination
            rank, pokerHand = self.evaluateHand(combo)

            # Compare and update best hand and rank
            if bestRank is None or rank > bestRank:
                bestRank = rank
                bestHand = combo
                bestPokerHand = pokerHand

        return bestHand, bestRank, bestPokerHand

    # Check the hand of the user and determine the best hand and ranking
    def checkHand(self):
        # Combine user's hand and dealer's cards
        availableCards = self.userHand + self.dealerCards

        # Find the best hand and its ranking from available cards
        bestHand, bestRank, pokerHand  = self.findBestHand(availableCards)

        return bestHand, bestRank, pokerHand

    # Function to Play the game and display the results
    def playGame(self):
        # Deal the cards
        self.dealCards()

        # Show the user's and dealer's hands
        print("\n[๑╹ᆺ╹] Your hand:", self.userHand)
        time.sleep(1)
        print("[๑╹ᆺ╹] Dealer's cards:", self.dealerCards)
        time.sleep(1)
        
        # Check the user's best hand and its rank
        bestHand, bestRank, pokerHand = self.checkHand()
        
        # Display the best hand and its rank
        print("\n[๑╹ᆺ╹] Your best hand:", bestHand)
        time.sleep(1)
        print("[๑╹ᆺ╹] Your poker hand:", pokerHand)
        time.sleep(1)

# Run Simulation an store data in log file
"""
Function to run the poker game for a set number of times
All results of poker hand will be stored in log file
"""
def runPokerSimulations(numSimulations, numPlayers):
    with open(logFile, "w") as f:
        for i in range(numSimulations):
            game = pokerGame(numPlayers)
            game.dealCards()
            bestHand, bestRank, pokerHand = game.checkHand()
            f.write(f"Simulation {i+1}: Best Hand: {bestHand}, Poker Hand: {pokerHand}\n")
    print(f"\n[๑╹ᆺ╹] Completed {numSimulations} simulations. Results saved to {logFile}.")

# Concurrent technique (threading) to read the log file
"""
Function to read the log file using threading
This function will read the log file and store data in pokerHandsLog
"""
def concurrentReader(logFile):
    print(f"\n[๑╹ᆺ╹] Starting concurrent reader for {logFile}...")
    pokerHandsLog = []

    def threadWorker():
        with open(logFile, "r") as f:
            pokerHandsLog.extend(f.readlines())

    thread = threading.Thread(target=threadWorker)
    thread.start()
    thread.join()

    print(f"\n[๑╹ᆺ╹] Concurrent reading completed.")
    return pokerHandsLog

# Worker function for sequential and parallel techniques
"""
Function that acts as work for sequential and parallel techniques
Each poker hand will be ranked and stored in a dictonary for each technique
"""
def findPokerHands(lines):
    # List of keyword to finds
    royalFlush = "Royal Flush"
    straightFlush = "Straight Flush"
    fourOfAKind = "Four of a Kind"
    fullHouse = "Full House"
    flush = "Flush"
    straight = "Straight"
    threeOfAKind = "Three of a Kind"
    twoPair = "Two Pair"
    onePair = "One Pair"
    highCard = "High Card"

    handResults = {
        royalFlush: 0,
        straightFlush: 0,
        fourOfAKind: 0,
        fullHouse: 0,
        flush: 0,
        straight: 0,
        threeOfAKind: 0,
        twoPair: 0,
        onePair: 0,
        highCard: 0
    }

    for line in lines:
        if "Poker Hand:" in line:
            handType = line.split("Poker Hand:")[1].strip()
            if handType in handResults:
                handResults[handType] += 1

    return handResults

# Parallel technique (multiprocessing) to read the log file
"""
Function to read the log file using multiprocessing
"""
def parallelTech(pokerHandsLog):
    print(f"\n[๑╹ᆺ╹] Starting parallel reading...")
    time.sleep(1)

    # divide the log file into chunks for each cores
    chunkSize = len(pokerHandsLog) // numCores
    chunks = [pokerHandsLog[i:i + chunkSize] for i in range(0, len(pokerHandsLog), chunkSize)]

    # Create` a pool of processes equal to the number of CPU cores
    with multiprocessing.Pool(processes=numCores) as pool:
        # Map the findPokerHands function to each chunk
        results = list(tqdm(pool.map(findPokerHands, chunks), total=len(chunks), desc="\n[๑╹ᆺ╹] Using Parallel technique..."))

    # Start the timer
    startTime = time.perf_counter()

    # Combine the results from all processes
    handResults = Counter()
    for result in results:
        handResults.update(result)

    # End the timer
    endTime = time.perf_counter()
    duration = endTime - startTime
    time.sleep(1)
    print(f"\n[๑╹ᆺ╹] Parallel reading completed.")
    return duration, handResults

# Sequential technique to read the log file
"""
Function to read the log file sequentially
Acts as a benchmark to be compared with parallel techniques
"""
def sequentialTech(pokerHandsLog):
    print(f"\n[๑╹ᆺ╹] Starting sequential reading...\n")
    time.sleep(1)

    # Start the timer
    startTime = time.perf_counter()

    handResults = Counter()
    for line in tqdm(pokerHandsLog, desc="[๑╹ᆺ╹] Using Sequential Technique..."):
        handResults.update(findPokerHands([line]))

    # End the timer
    endTime = time.perf_counter()
    duration = endTime - startTime
    time.sleep(1)
    print(f"\n[๑╹ᆺ╹] Sequential reading completed.")
    return duration, handResults

# Function to start doing simulations and for comparing techniques
def simulationRun():
    # check if log file already exists and ask user if they want to overwrite it
    if os.path.exists(logFile):
        print(f"\n[๑╹ᆺ╹] Log file '{logFile}' already exists. Do you want to overwrite it? (yes/no): ")
        response = input("\n>>> ").lower()
        if response in ['yes', 'y']:
            # Ask user for number of simulations and number of players
            # Checks if invalid input is entered for number of simulations and number of players
            while True:                
                try:
                    print("\n[๑╹ᆺ╹] Enter number of simulations to run.")
                    numSimulations = int(input("\n>>> "))
                    break
                except ValueError:
                    print("\n[๑╹ᆺ╹] Please enter valid numbers!")
            while True:
                try:
                    print("\n[๑╹ᆺ╹] Enter number of players for each simulation (2-22).")
                    numPlayers = int(input("\n>>> "))
                    if numPlayers < 2 or numPlayers > 22:
                        print("\n[๑╹ᆺ╹] Please enter a number between 2 and 22.")
                        continue
                    break
                except ValueError:
                    print("\n[๑╹ᆺ╹] Please enter valid numbers!")

            # Run the poker simulations and store results in log file
            runPokerSimulations(numSimulations, numPlayers)
        else:
            print("\n[๑╹ᆺ╹] Reading existing log file.")
    
    # Read the log file using concurrent technique (threading)
    pokerHandsLog = concurrentReader(logFile)
    time.sleep(1)
    
    # Run sequential technique to set a benchmark for comparison
    timeSequential, resultSequential = sequentialTech(pokerHandsLog)
    time.sleep(1)

    # Run parallel technique to compare with sequential technique
    timeParallel, resultParallel = parallelTech(pokerHandsLog)
    time.sleep(1)

    # Print report on the results of both techniques and their comparison
    reportResult(timeSequential, timeParallel, resultParallel)

# Function to run the program a single time
def singleGame():
    
    print("\n\t======================")
    print("\t POKER GAME SIMULATOR ")
    print("\t======================")

    # User enter number of players
    print("[๑╹ᆺ╹] Enter number of players.")
    print("[๑╹ᆺ╹] (Excluding the dealer, maximum 22 players including user)")

    # Checks if invalid input is entered
    while True:
        try:
            numPlayer = int(input("\n>>> "))
            if numPlayer < 2 or numPlayer > 22:
                print("\n[๑╹ᆺ╹] Please enter a number between 2 and 22.")
                continue
            break
        except ValueError:
            print("\n[๑╹ᆺ╹] Please enter a valid number!")

    # Initialize the poker game with the number of players
    game = pokerGame(numPlayer)

    # Play the game
    game.playGame()

    while True:
        # Ask user if they want to play again
        print("\n[๑╹ᆺ╹] Do you want to play again? (yes/no) ")
        playAgain = input("\n>>> ").lower()
        if playAgain in ['yes', 'y']:
            game = pokerGame(numPlayer)
            game.playGame()
        elif playAgain in ['no', 'n']:
            print("\n[๑╹ᆺ╹] Thanks for playing!\n")
            break
        else:
            print("\n[๑╹ᆺ╹] Please enter 'yes' or 'no'.")

# Function to report the results of the simulations and techniques
def reportResult(timeSequential, timeParallel, resultParallel):
    print("\n[๑╹ᆺ╹] Generating report...\n")
    time.sleep(1)
    print("\n=============================================")
    print(" REPORT ON SIMULATION RESULTS AND TECHNIQUES ")
    print("=============================================\n")
    print("Poker hand results:\n")
    print("\tRoyal Flush: " + str(resultParallel["Royal Flush"]))
    print("\tStraight Flush: " + str(resultParallel["Straight Flush"]))
    print("\tFour of a Kind: " + str(resultParallel["Four of a Kind"]))
    print("\tFull House: " + str(resultParallel["Full House"]))
    print("\tFlush: " + str(resultParallel["Flush"]))
    print("\tStraight: " + str(resultParallel["Straight"]))
    print("\tThree of a Kind: " + str(resultParallel["Three of a Kind"]))
    print("\tTwo Pair: " + str(resultParallel["Two Pair"]))
    print("\tOne Pair: " + str(resultParallel["One Pair"]))
    print("\tHigh Card: " + str(resultParallel["High Card"]))
    print("\n==============================================\n")
    print("Performance Comparison:\n")
    print(f"\tSequential Time: {timeSequential:.2f} seconds")
    print(f"\tParallel Time: {timeParallel:.2f} seconds")
    print(f"\tImprovement: {timeSequential / timeParallel:.2f}x faster")
    print("\n==============================================\n")
    print("[๑╹ᆺ╹] Report generation completed.\n")

# Main function to run the program
if __name__ == "__main__":
    # Display welcome message
    print("\t====================================")
    print("\tWelcome to the Poker Game Simulator!")
    print("\t====================================")
    print("[๑╹ᆺ╹] This programs allows you to simulate poker games and shows the results of your hand.")

    # Ask if user wants to do single test or run simulations
    print("\n[๑╹ᆺ╹] Do you want to run a single game or run a simulations?")
    print("[๑╹ᆺ╹] Enter 'single' for single game or 'simulations' for running simulations.")
    
    while True:
        choice = input("\n>>> ").lower()
        if choice in ['single', 's']:
            singleGame()
            break
        elif choice in ['simulations', 'sim', 'simu']:
            simulationRun()
            break
        else:
            print("\n[๑╹ᆺ╹] Please enter 'single' or 'simulations'.")