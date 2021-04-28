# importing various packages for the bot creation.
import discord
from discord.ext import commands
import random

# creating the client (AKA BOT).
client = commands.Bot(command_prefix="!")

# variables.
player1 = " "
player2 = " "
turn = " "
gameOver = True

# board variable created which represents the tic-tac-toe board.
board = []

# declaring a 2-D array to store the winning conditions. 
winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]
# 1st command to create a new tic-tac-toe game, making sure that the game is played between 
@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    # if-statement to check if the game is over, and only initialize a new game. 
    if gameOver:
        # creating a 3x3 global board variable.
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        
        #initializing a turn variable.
        turn = " "

        # creating a game variable which determines that the game is on now.
        gameOver = False

        # keeping track of the score.
        count = 0

        player1 = p1
        player2 = p2

        # code to print the board.
        line = " "
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # code to determine who goes first
        # code to generate a random integer to determine player1 or player2 going first.
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish the previous game first please.")

# 2nd command to allow players to put their position/place of their marker on the tic tac toe board.
@client.command()
async def place(ctx, pos: int):

    # declaring global variables.
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    # 1st if-statement that runs the statement if the game is not over.
    if not gameOver:
        mark = " "
        # 2nd if-statement to make sure only 2 players are playing at once.
        if turn == ctx.author:

            # 3rd if-statement to determine which player's turn it is. Using the "X" and "O" emojis as markers.
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            # 4th if-statement to determine if the user's entered a valid position while making sure no position is entered twice.
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # printing the updated board after every position marked by each user.
                line = " "
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                # code to determine if there is a winner.
                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # code to switch the turns.
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")

# creating a function that will check if a user has won the game. 
def checkWinner(winningConditions, mark):
    global gameOver

    # coding a for-loop that will run if the winning conditions are met. 
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

# ----CODING ERROR HANDLERS----
# creating the error handler function that will manage an error that a user creates where they do not enter the "@" of the user's playing the game or forgets to mention 2 players.
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)

    # if-statement to check if the error is of a certain type. (ex. discord error).
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@somebody's ID>).")

# creating the error handler function that will manage an error that a user creates where the user does not enter an argument or enters a bad argument.
@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

client.run("TOKEN")