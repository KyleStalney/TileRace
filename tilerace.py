import json
import random

import discord
from discord import Client

_tiers = ['Mechanical', 'Minigames', 'Skilling', 'Early Game', 'Mid Game', 'Late Game', 'End Game', 'MYSTERY']
_paths = {
    'start': [3,1,2,4,2,7,5,0,2,5,6,1,6,0,4,1,2,7,4,5,2,0,5],
    'long': [],
    'short': [],
    'end': [],
}

def get_tier(path, tile):
    return _tiers[_paths[path][tile]]

class TileRace():
    self.teams = {}
    self.signups = []
    self.challenges = {}

    def __init__(self):
        with open('tilerace.json') as f:
            data = json.load(f)
        if not data:
            raise Exception('Failed to load data from tilerace.json')
        self.teams = data.get('teams', None)
        self.signups = data.get('teams', None)
        self.challenges = data.get('challenges', None)
        self.setup_teams()

    def setup_teams(self):
        for team in self.teams:
            for tier in team['challenges']:
                if not tier:
                    team['challenges'][tier] = self.challenges[tier]
            if (
                not team['path']
                or not team['tile']
                or not team['tile_tier']
            ):
                team['tile'] = 0
                team['path'] = 'start'
                team['tile_tier'] = _tiers[_paths['start'][0]]

    def save(self):
        data = []
        data['teams'] = self.teams
        data['signups'] = self.signups
        data['challenges'] = self.challenges
        with open('tilerace.json', 'w') as f:
            f.write(json.dumps(data))

    def get_team(self, user):
        for name, team in self.teams:
            if user in team['members']: return name

    async def signup(self, message):
        if message.author not in self.signups:
            self.signups.append(message.author)
        await message.add_reaction('\U00002705')
        self.save()
        log.info(f'signup,{message.author},added to signups')

    async def list(self, message):
        mod_role = message.guild.get_role(690247456587382805)
        if mod_role not in message.author.roles:
            return
        await message.reply(self.signups.join('\n'))

    async def challenges(self, message):
        team = self.teams[self.get_team(message.author)]
        tier = get_tier(team['path'], team['tile'])
        challenges = [x['description'] for x in team['challenges'][tier]]
        await message.reply(challenges.join('\n'))

    async def roll(self, message):
        team_name = self.get_team(message.author)
        team = self.teams[team_name]
        if message.author != team['captain']:
            return
        if not team['can_roll']:
            return
        dice = dice_roll(team['path'])
        team['can_roll'] = False
        cur_path = _paths[team['path']]
        new_pos = team['tile'] + dice
        if new_pos + 1 >= len(cur_path):
            if team['path'] == 'start':
                # Prompt for path choice
                choice = ''
                team['path'] = choice
                team['tile'] = new_pos - len(cur_path)
                team['tile_tier'] = get_tier(team['path'], team['tile'])
                await message.reply(f'{team_name} has entered the **{team[choice]} path**!')
        else:
            team['tile'] = new_pos
            team['tile_tier'] = get_tier(team['path'], team['tile'])
            print(f"You rolled a {dice}!\nMoving **{team_name}** to position {new_pos}, which is a {team['tile_tier']} tile.")
        self.teams[team_name] = team
        self.save()

    async def complete(message):
        pass

    def dice_roll(dice_type: str) -> int:
        if dice_type == 'easy':
            return random.randint(0, 3)
        if dice_type == 'medium':
            return random.randint(1, 4)
        if dice_type == 'hard':
            return random.randint(2, 5)

'''
def complete_tile(user, message, reaction, reaction_user):
    team = teams[user[0]]
    if reaction_user[0] != user[0] and reaction_user[1] and reaction == 'checkmark':
        teams[user[0]][2] = True
        if message[-1] in tile_dict[team[4]]:
            if tile_dict[team[4][int(message[-1])]][user[0]] == True:
                print("Challenge " + str(message[-1]) + " has been completed. Removing from challenges for team " + str(
                    user[0]))
                tile_dict[team[4]][int(message[-1])][user[0]] = False
                print("Team " + str(user[0]) + " has been awarded a dice roll")
        else:
            print("invalid completion, please try again")
'''

'''
DATA EXAMPLE
{
	"teams": {
		"Team 1": {
			"tile": 0,
			"tile_tier": "Mechanical",
			"can_roll": false,
			"path": "start",
			"captain": "kylestanley",
			"members": ["rudes", "kylestanley"],
			"challenges": {
				"Mechanical": [],
				"Minigames": [],
				"Skilling": [],
				"Early Game": [],
				"Mid Game": [],
				"Late Game": [],
				"End Game": [],
				"MYSTERY": [],
			}
		}
	},
	"challenges": {
		"Mechanical": [],
		"Minigames": [],
		"Skilling": [],
		"Early Game": [],
		"Mid Game": [],
		"Late Game": [],
		"End Game": [],
		"MYSTERY": [],
	},
	"signups": ["kylestanley"],
}
'''
