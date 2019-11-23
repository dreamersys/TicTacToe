import math
import copy

player = ['X', 'O']
startState = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


def playMove(state, whoTurn, whichBlock):
    if whichBlock < 1 or whichBlock > 9:
        whichBlock = int(input("Chosen block is not valid. Choose an empty block between 1 to 9!: "))
        playMove(state, whoTurn, whichBlock)
    elif state[int((whichBlock - 1) / 3)][int((whichBlock - 1) % 3)] == ' ':
        state[int((whichBlock - 1) / 3)][int((whichBlock - 1) % 3)] = whoTurn
    else:
        whichBlock = int(input("Chosen block is taken. Choose an empty block between 1 to 9!: "))
        playMove(state, whoTurn, whichBlock)


def checkCurState(state):
    # Output winner, stillPlaying
    # Horizontal and Vertical
    for k in range(3):
        if state[k][0] == state[k][1] and state[k][1] == state[k][2] and state[k][0] != ' ':
            return state[k][0], False
        if state[0][k] == state[1][k] and state[1][k] == state[2][k] and state[0][k] != ' ':
            return state[0][k], False
    # Diagonals
    if state[0][0] == state[1][1] and state[1][1] == state[2][2] and state[0][0] != ' ':
        return state[0][0], False
    if state[2][0] == state[1][1] and state[1][1] == state[0][2] and state[2][0] != ' ':
        return state[2][0], False

    # Check for draw
    isDraw = True
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                isDraw = False
    if isDraw:
        return None, False

    return None, True


def printBoard(state):
    print('-------------')
    print('| ' + str(state[0][0]) + ' | ' + str(state[0][1]) + ' | ' + str(state[0][2]) + ' |')
    print('-------------')
    print('| ' + str(state[1][0]) + ' | ' + str(state[1][1]) + ' | ' + str(state[1][2]) + ' |')
    print('-------------')
    print('| ' + str(state[2][0]) + ' | ' + str(state[2][1]) + ' | ' + str(state[2][2]) + ' |')
    print('-------------')


def minMax(state, depth, isMax):
    winner, notDone = checkCurState(state)
    if winner == 'O' and notDone is False:
        return 10 - depth
    elif winner == 'X' and notDone is False:
        return -10 + depth
    elif winner is None and notDone is False:
        return 0

    if isMax:
        best = -1000
    else:
        best = 1000
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                if isMax:
                    playMove(state, player[1], (i*3) + j + 1)
                    best = max(best, minMax(state, depth + 1, not isMax))
                else:
                    playMove(state, player[0], (i*3) + j + 1)
                    best = min(best, minMax(state, depth + 1, not isMax))
                state[i][j] = ' '

    return best


def getBestMove(state, whoPlays):
    bestVal = -1000
    bestMove = None
    freeCells = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                freeCells.append(i*3 + (j+1))
                playMove(state, player[1], (i*3) + j + 1)
                moveVal = minMax(state, 0, False)
                if moveVal > bestVal:
                    bestVal = moveVal
                    bestMove = i*3 + j + 1
                state[i][j] = ' '
    return bestMove


def main():
    startNewGame = 'Y'
    while startNewGame == 'Y' or startNewGame == 'y':
        gameState = copy.deepcopy(startState)
        stillPlaying = True
        print("New Game!")
        printBoard(gameState)
        winner = None
        whoPlays = -1
        while whoPlays == -1:
            playerChoose = input("Choose who goes first! X (You) or O (CPU): ")
            if playerChoose == 'X' or playerChoose == 'x':
                whoPlays = 0
            elif playerChoose == 'O' or playerChoose == 'o':
                whoPlays = 1
            else:
                print("Invalid selection! Please try again!")
        while stillPlaying:
            if whoPlays == 0:
                whichBlock = int(input("Choose where to place your move (1 to 9)!: "))
                playMove(gameState, player[whoPlays], whichBlock)
            else:
                whichBlock = getBestMove(gameState, player[whoPlays])
                playMove(gameState, player[whoPlays], whichBlock)
                print("CPU plays move at " + str(whichBlock))
            printBoard(gameState)
            winner, stillPlaying = checkCurState(gameState)
            if winner is not None:
                print(str(winner) + " won the game!")
            elif stillPlaying is False:
                print("Game ends in a draw!")
            else:
                whoPlays = (whoPlays + 1) % 2

        startNewGame = input("Play again? (Y or N): ")
        if startNewGame != 'Y' or startNewGame != 'y':
            print("It was fun!")


main()
