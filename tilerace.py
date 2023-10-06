import discord
from discord import Client
import responses
import random


entrants = ["brando2277","trevor6396","samw1se","imkoch","detox_.","zaq6136","greekfr3ak.","joosii69","drpat34","andrewxc","red_rascal","thurison","prosups","n.o.r.s.e","diblydoobly","Matsoe/Chubou#7052","bosspross","SteelTiiTan#2864","muovvi","shook_em","iclicked","vorpeo","pondscum4954","Benjamin#4104","rigidryan","odors","pandorite","fespoof","sicknez","dillon4579","robbrec","dirtydimsum","tranbearpig","iblake","mir4culous","atlasstoned","deathking13","yawp.","nerds3378","shwoopgodlordking","creedmoor1049","montaro","Muzzle#3031","giganticowl","bobarctor","thecabe","ivar__","milftastic","Sweaty Nasty#8061","themightykake","elbomb","Matt777#9811","Ward Fe#9736","Brother Shame#1426","kingkurask","wethenorth","xploh","athief",".hellpup","brenden39","motozzi","gilfrid_eggs"]

team_id = 1
captain_bool = True
discord_name = 'kyle'
dice_bool = True
position = 0
tile = 'easy'
x = 0
tile_list_a = ['easy', 'medium', 'hard', 'medium', 'hard', 'medium', 'hard', 'easy', 'medium', 'hard', 'medium', 'hard',
               'medium', 'hard', 'easy', 'medium', 'hard', 'medium', 'hard', 'medium', 'hard']
listy = tile_list_a

user1 = [team_id, captain_bool, discord_name]
user2 = [2, True, 'Clockster']
dice_dict = {'easy': [0, 3], 'medium': [1, 4], 'hard': [2, 5]}
dice_type = dice_dict["hard"]

team_one_list = [0, dice_type, dice_bool, position, tile, listy]
team_two_list = [1, dice_type, dice_bool, position, tile, listy]
team_three_list = [2, dice_type, dice_bool, position, tile, listy]
teams = [team_one_list, team_two_list, team_three_list]

dice_dict = {'easy': [0, 3], 'medium': [1, 4], 'hard': [2, 5]}

easy = {'1': [[True, True, True, True, True], "Kill a rat"], '2': [[True, True, True, True, True], "Kill a Chicken"],
        '3': [[True, True, True, True, True], "Kill a Cow"]}
medium = {'1': [[True, True, True, True, True], "Kill a rat"], '2': [[True, True, True, True, True], "Kill a Chicken"],
          '3': [[True, True, True, True, True], "Kill a Cow"]}
hard = {'1': [[True, True, True, True, True], "Kill a rat"], '2': [[True, True, True, True, True], "Kill a Chicken"],
        '3': [[True, True, True, True, True], "Kill a Cow"]}
tile_dict = {'easy': easy, 'medium': medium, 'hard': hard}

challenge_list = [easy, medium, hard]

y = 0
'''
team_one_list = []
team_two_list = []
team_three_list = []
team_four_list = []
team_five_list = []
'''

rsn_list = []

@client.event
async def on_message(message):

    user_var = message.author
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    guild = message.guild
    guild_name = message.guild


    if user_message == 'f412313251sdafjdasfup235198upj':
        for i in guild.members:
            if str(i) in entrants:
                discord_name = entrants[entrants.index(str(i))]
                if str(i.nick) == 'None':
                    rsn_list.append([discord_name, discord_name])
                else:
                    rsn_list.append([discord_name, str(i.nick)])


        print(rsn_list)
        print(channel)
    print(rsn_list)
    for i in range(len(rsn_list)):
        print(rsn_list[i][1])
def show_challenges(user):
    current_team = teams[user[0]]
    if current_team[4] == 'easy':
        for i in easy:
            if easy[i][0][current_team[0]]:
                print(str(i) + ": " + str(easy[i][1]))

def dice_roll(user, message):
    current_team = teams[user[0]]
    if current_team[2] and message == '!roll':
        dice = random.randint(dice_dict[current_team[4]][0], dice_dict[current_team[4]][1])
        new_sum = current_team[3] + dice
        if new_sum + 1 >= len(tile_list_a):
            print('exceeds bound')
            current_team[3] = new_sum % len(tile_list_a)
        else:
            current_team[3] += dice
            print("You rolled a " + str(dice) + ", moving you to position " + str(
                current_team[3]) + ", which is a " + str(tile_list_a[new_sum + 1]) + " tile")

        current_team[2] = False
        current_team[3] = new_sum % len(tile_list_a)
    if message == 'no':
        x += 1
    if "!complete" in message:
        complete_tile(user, message, 'checkmark', user2)
    if message == "!challenges":
        show_challenges(user)
    teams[user[0]] = current_team


client.run(TOKEN)


team_id = 1
captain_bool = True
discord_name = 'kyle'
dice_bool = True
position = 0
tile = 'easy'
x = 0
tile_list_a = ['easy', 'medium', 'hard', 'medium', 'hard', 'medium', 'hard', 'easy', 'medium', 'hard', 'medium', 'hard',
               'medium', 'hard', 'easy', 'medium', 'hard', 'medium', 'hard', 'medium', 'hard']
listy = tile_list_a

user1 = [team_id, captain_bool, discord_name]
user2 = [2, True, 'Clockster']
dice_dict = {'easy': [0, 3], 'medium': [1, 4], 'hard': [2, 5]}
dice_type = dice_dict["hard"]

team_one_list = [0, dice_type, dice_bool, position, tile, listy]
team_two_list = [1, dice_type, dice_bool, position, tile, listy]
team_three_list = [2, dice_type, dice_bool, position, tile, listy]
teams = [team_one_list, team_two_list, team_three_list]

dice_dict = {'easy': [0, 3], 'medium': [1, 4], 'hard': [2, 5]}

easy = {'1': [[True, True, True, True, True], "Kill a rat"], '2': [[True, True, True, True, True], "Kill a Chicken"],
        '3': [[True, True, True, True, True], "Kill a Cow"]}
medium = {'1': [[True, True, True, True, True], "Kill a rat"], '2': [[True, True, True, True, True], "Kill a Chicken"],
          '3': [[True, True, True, True, True], "Kill a Cow"]}
hard = {'1': [[True, True, True, True, True], "Kill a rat"], '2': [[True, True, True, True, True], "Kill a Chicken"],
        '3': [[True, True, True, True, True], "Kill a Cow"]}
tile_dict = {'easy': easy, 'medium': medium, 'hard': hard}

challenge_list = [easy, medium, hard]

y = 0

'''
def complete_tile(user, message, reaction, reaction_user):
    current_team = teams[user[0]]
    if reaction_user[0] != user[0] and reaction_user[1] and reaction == 'checkmark':
        teams[user[0]][2] = True
        if message[-1] in tile_dict[current_team[4]]:
            if tile_dict[current_team[4][int(message[-1])]][user[0]] == True:
                print("Challenge " + str(message[-1]) + " has been completed. Removing from challenges for team " + str(
                    user[0]))
                tile_dict[current_team[4]][int(message[-1])][user[0]] = False
                print("Team " + str(user[0]) + " has been awarded a dice roll")
        else:
            print("invalid completion, please try again")




'''
'''
y = ''
while y != 'no':
    y = input("Please type an input: ")
    dice_roll(user1, y)
'''

