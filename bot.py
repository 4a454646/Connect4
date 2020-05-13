import random
import sys
import math
import asyncio
import discord
from discord.ext import commands as cmds
bot = cmds.Bot(command_prefix='.', activity=discord.Game(".conn"))

emoji_dict = {0:":o:", 1:":cd:", 2:":dvd:", 3:":gear:"}
grid = [[0 for i in range(16)] for j in range(10)] 
started = False
players = []
cur_moving = 0
cur_game = None

class Game:
    def __init__(self, emoji_dict, grid, started, players, cur_moving, cur_gamer):
        self.emoji_dict = emoji_dict
        self.grid = grid
        self.started = started
        self.players = players
        self.cur_moving = cur_moving
        self.cur_gamer = cur_gamer

    def convert_row(self, n):
        return "".join((self.emoji_dict[i] for i in self.grid[n]))

    def win_check(self, row, col, check_num):
        try: # 3 up
            if (self.grid[row][col+1] == check_num and self.grid[row][col+2] == check_num and self.grid[row][col+3] == check_num): return True
        except: pass
        try: # 2 up 1 down
            if (self.grid[row][col+1] == check_num and self.grid[row][col+2] == check_num and self.grid[row][col-1] == check_num): return True
        except: pass
        try: # 2 down 1 up
            if (self.grid[row][col+1] == check_num and self.grid[row][col-1] == check_num and self.grid[row][col-2] == check_num): return True
        except: pass
        try: # 3 down
            if (self.grid[row][col-1] == check_num and self.grid[row][col-2] == check_num and self.grid[row][col-3] == check_num): return True
        except: pass
        try: # 3 right
            if (self.grid[row+1][col] == check_num and self.grid[row+2][col] == check_num and self.grid[row+3][col] == check_num): return True
        except: pass
        try: # 2 right 1 left
            if (self.grid[row+1][col] == check_num and self.grid[row+2][col] == check_num and self.grid[row-1][col] == check_num): return True
        except: pass
        try: # 2 left 1 right
            if (self.grid[row+1][col] == check_num and self.grid[row-1][col] == check_num and self.grid[row-2][col] == check_num): return True
        except: pass
        try: # 3 left
            if (self.grid[row-1][col] == check_num and self.grid[row-2][col] == check_num and self.grid[row-3][col] == check_num): return True
        except: pass
        try: # 3 up 3 right
            if (self.grid[row+1][col+1] == check_num and self.grid[row+2][col+2] == check_num and self.grid[row+3][col+3] == check_num): return True
        except: pass
        try: # 2 up 2 right
            if (self.grid[row-1][col-1] == check_num and self.grid[row+1][col+1] == check_num and self.grid[row+2][col+2] == check_num): return True
        except: pass
        try: # 2 down 2 left
            if (self.grid[row-2][col-2] == check_num and self.grid[row-1][col-1] == check_num and self.grid[row+1][col+1] == check_num): return True
        except: pass
        try: # 3 down 3 left
            if (self.grid[row-3][col-3] == check_num and self.grid[row-2][col-2] == check_num and self.grid[row-1][col-1] == check_num): return True
        except: pass
        try: # 3 up 3 left
            if (self.grid[row-1][col+1] == check_num and self.grid[row-2][col+2] == check_num and self.grid[row-3][col+3] == check_num): return True
        except: pass
        try: # 2 up 2 left
            if (self.grid[row+1][col-1] == check_num and self.grid[row-1][col+1] == check_num and self.grid[row-2][col+2] == check_num): return True
        except: pass
        try: # 2 down 2 right
            if (self.grid[row+2][col-2] == check_num and self.grid[row+1][col-1] == check_num and self.grid[row-1][col+1] == check_num): return True
        except: pass
        try: # 3 down 3 right
            if (self.grid[row+3][col-3] == check_num and self.grid[row+2][col-2] == check_num and self.grid[row+1][col-1] == check_num): return True
        except: pass
        return False

    def place_into(self, num, col):
        for i in range(10):
            if self.grid[i][col] == 0:
                self.grid[i][col] = num
                return (True, self.win_check(i, col, num))
        return (False, False)
        # returns (placed_successfully, is_won)
        
    def gen_embed(self, user, has_won=False):
        created = None
        if (cur_moving == 0): created = discord.Embed(color=0x8899a6)
        elif (cur_moving == 1): created = discord.Embed(color=0xffd983)
        else: created = discord.Embed(color=0x66757f)
        if (has_won):
            created.set_image(url=user.avatar_url)
            created.add_field(name=f"Connect 4", value=f"**{self.players[cur_moving].name}** ({emoji_dict[cur_moving+1]}) **has won the game!**", inline=False)
        else: 
            created.set_thumbnail(url=user.avatar_url)
            created.add_field(name=f"Connect 4", value=f"Current move: **{self.players[cur_moving].name}** ({emoji_dict[cur_moving+1]})", inline=False)
        created.add_field(name=":zero::one::two::three::four::five::six::seven::eight::nine::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f:", value=f"{self.convert_row(9)}\n{self.convert_row(8)}\n{self.convert_row(7)}\n{self.convert_row(6)}\n{self.convert_row(5)}\n{self.convert_row(4)}\n{self.convert_row(3)}\n{self.convert_row(2)}\n{self.convert_row(1)}\n{self.convert_row(0)}", inline=False)
        created.add_field(name=f"Players: {self.players[0].name} ({emoji_dict[1]}), {self.players[1].name} ({emoji_dict[2]}), {self.players[2].name} ({emoji_dict[3]})", value="᠎", inline=False)
        if (has_won):
            asyncio.sleep(0.5)
            self.players.clear()
            self.started = False
            self.cur_game = None
            self.grid = [[0 for i in range(16)] for j in range(10)] 
        return created

gameInstance = Game(emoji_dict, grid, started, players, cur_moving, cur_game)

async def take_move(user, num):
    taken_move = gameInstance.place_into(gameInstance.cur_moving + 1, num)
    if taken_move[1]:
        await gameInstance.cur_game.clear_reactions()
        await gameInstance.cur_game.edit(embed=gameInstance.gen_embed(user, True))
    elif (taken_move[0]):
        gameInstance.cur_moving += 1
        if gameInstance.cur_moving > 2: gameInstance.cur_moving = 0
        await gameInstance.cur_game.edit(embed=gameInstance.gen_embed(user))
    else: pass

@bot.event
async def on_ready():
    print(f"Successful log in as {bot.user}.")


@bot.event
async def on_reaction_add(reaction, user):
    global cur_moving
    global cur_game
    if (user.id != 709849577045360711):
        if (user.id == players[cur_moving].id):
            if reaction.emoji == "0️⃣":
                await take_move(user, 0)
            elif reaction.emoji == "1️⃣":
                await take_move(user, 1)
            elif reaction.emoji == "2️⃣":
                await take_move(user, 2)
            elif reaction.emoji == "3️⃣":
                await take_move(user, 3)
            elif reaction.emoji == "4️⃣":
                await take_move(user, 4)
            elif reaction.emoji == "5️⃣":
                await take_move(user, 5)
            elif reaction.emoji == "6️⃣":
                await take_move(user, 6)
            elif reaction.emoji == "7️⃣":
                await take_move(user, 7)
            elif reaction.emoji == "8️⃣":
                await take_move(user, 8)
            elif reaction.emoji == "9️⃣":
                await take_move(user, 9)
            elif reaction.emoji == "🇦":
                await take_move(user, 10)
            elif reaction.emoji == "🇧":
                await take_move(user, 11)
            elif reaction.emoji == "🇨":
                await take_move(user, 12)
            elif reaction.emoji == "🇩":
                await take_move(user, 13)
            elif reaction.emoji == "🇪":
                await take_move(user, 14)
            elif reaction.emoji == "🇫":
                await take_move(user, 15)
        await reaction.remove(user)

@bot.command(aliases=["connect4", "play"])
async def conn(ctx):
    if (gameInstance.started):
        if (len(gameInstance.players) < 2):
            gameInstance.players.append(ctx.message.author)
            await ctx.send(f"{ctx.message.author.name} has joined... now at {len(gameInstance.players)}/3 players.")
        elif (len(gameInstance.players) == 2):
            gameInstance.players.append(ctx.message.author)
            await ctx.send(f"{ctx.message.author.name} has joined... starting game!")
            gameInstance.cur_game = await ctx.send(embed=gameInstance.gen_embed(ctx.message.author))
            await gameInstance.cur_game.add_reaction("0️⃣")
            await gameInstance.cur_game.add_reaction("1️⃣")
            await gameInstance.cur_game.add_reaction("2️⃣")
            await gameInstance.cur_game.add_reaction("3️⃣")
            await gameInstance.cur_game.add_reaction("4️⃣")
            await gameInstance.cur_game.add_reaction("5️⃣")
            await gameInstance.cur_game.add_reaction("6️⃣")
            await gameInstance.cur_game.add_reaction("7️⃣")
            await gameInstance.cur_game.add_reaction("8️⃣")
            await gameInstance.cur_game.add_reaction("9️⃣")
            await gameInstance.cur_game.add_reaction("🇦")
            await gameInstance.cur_game.add_reaction("🇧")
            await gameInstance.cur_game.add_reaction("🇨")
            await gameInstance.cur_game.add_reaction("🇩")
            await gameInstance.cur_game.add_reaction("🇪")
            await gameInstance.cur_game.add_reaction("🇫")
        else: 
            await ctx.send("The game has already gameInstance.started.")
    else:
        gameInstance.started = True
        gameInstance.players.clear()
        gameInstance.players.append(ctx.message.author)
        await ctx.send(f"{ctx.message.author.name} has created a game. Use '.conn' to join!")

@bot.command(aliases=["stop"])
async def abort(ctx):
    gameInstance.players.clear()
    gameInstance.started = False
    for reaction in gameInstance.cur_game.reactions:
        reaction.remove(gameInstance.cur_game.author)
    gameInstance.cur_game = None
    gameInstance.grid = [[0 for i in range(16)] for j in range(10)] 
    await ctx.send("The game has been stopped.")

bot.run("bot_token")
