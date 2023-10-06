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
"Mechanical" = [{
        "description": "complete a 500+ toa",
        "active": False},
    {
        "description": "have 3 teammates win an LMS game",
        "active": False},
    {
        "description": "Kill any 3 awakened bosses. You can do the same boss multiple times.",
        "active": False},
    {
        "description": "Punch/Kick Jad to death",
        "active": False},
    {
        "description" : "Get 5 Phosani kc in 1 trip",
        "active": False
    }, {
        "description" : "Get back-to-back sub 7-minute completions of the Corrupted Gauntlet",
        "active" : False
    }]

"Skilling" = [{
        "description": "Get a Tome of Fire",
        "active": False},
    {
        "description": "Get any Tempoross Unique. Pages that replace unique count",
        "active": False},
    {
        "description": "Get an Abyssal Dye from Guardians of the Rift",
        "active": False},
    {
        "description": "Acquire a Golden Tench",
        "active": False},
    {
        "description" : "Acquire a Ring of Endurance",
        "active": False},
    {
        "description" : "Make a Colossal Blade from scratch",
        "active" : False},
    {
        "description": "Get that stupid pirate hook thing from the Brimhaven Agility Course",
        "active": False},
    {
        "description": "Pickpocket 6 Blood Shards",
        "active" : False}]

"Ugh Daddy I'm Clogging" = [{
        "description": "Obtain a Bryophyta's Essence",
        "active": False},
    {
        "description": "Get a Black Tourmaline Core",
        "active": False},
    {
        "description": "Get any boot drop from a medium clue",
        "active": False},
    {
        "description": "Get any Revenant Weapon",
        "active": False},
    {
        "description" : "Get a Champion Scroll",
        "active": False},
    {
        "description" : "Obtain a complete barb assault outfit(except torso)(you can pick the hat) ",
        "active" : False},
    {
        "description": "Get a Pharaoh's Sceptre",
        "active": False},
    {
        "description": "Any 1 player earn 34 castle wars tickets(enough for a decorative armor set)",
        "active" : False}]

"Early Game" = [{
        "description": "Obtain 3 Bandos Uniques",
        "active": False},
    {
        "description": "Get a Barrows Double Chest",
        "active": False},
    {
        "description": "Get 5 DKS rings",
        "active": False},
    {
        "description": "Get any GWD Hilt",
        "active": False},
    {
        "description" : "Get all Zammy uniques",
        "active": False},
    {
        "description" : "Get a Dragon Pickaxe Drop",
        "active" : False},
    {
        "description": "Get 3 Zenytes",
        "active": False},
    {
        "description": "Get a Sarachnis Cudgel",
        "active": False},
    {
        "description": "Complete a Barrows Set",
        "active": False}]

"Mid Game" = [{
        "description": "Obtain a Voidwaker Piece",
        "active": False},
    {
        "description": "Get 3 zulrah drops or a mutagen",
        "active": False},
    {
        "description": "Get 5 Venator Shards. If you get one from a cache, complete the tile",
        "active": False},
    {
        "description": "Get 4 Cerberus Uniques. Pegasian Crystal counts for 2.",
        "active": False},
    {
        "description" : "Get that Thermy staff",
        "active": False},
    {
        "description" : "Complete an Abyssal Bludgeon(as a team, specific parts don't matter)",
        "active" : False},
    {
        "description": "Get an Enhanced Weapon Seed or 4 Armor Seeds",
        "active": False},
    {
        "description": "Any 1 player earn 34 castle wars tickets(enough for a decorative armor set)",
        "active" : False}]

"Late Game" = [{
        "description": "Get an Arcane or Dextrous Prayer Scroll",
        "active": False},
    {
        "description": "Get a Lightbearer or Osmumten's Fang",
        "active": False},
    {
        "description": "Get an Avernic Defender Hilt",
        "active": False},
    {
        "description": "Get a Hydra Claw or Hydra Leather",
        "active": False},
    {
        "description" : "Get a ToB Weapon",
        "active": False},
    {
        "description" : "Get a CoX Weapon(butt plug counts, so does Dinny B)",
        "active" : False},
    {
        "description": "Get 2 raid armor drops(Masori/Justi/Ancestral. Shields don't count)",
        "active": False},
    {
        "description": "Get a Soulreaper Axe Piece",
        "active": False},
    {
        "description": "Get 3 Chromium Ingots",
        "active": False},
    {
        "description": "Get 2 Virtus Armor drops(can be the same piece)",
        "active": False}]

"End Game" = [{
        "description": "Get an Inquisitor Drop(mace counts) or orb(staff doesn't count lmao)",
        "active": False},
    {
        "description": "Get any Mega Rare or Dragon Claws",
        "active": False},
    {
        "description": "Get 4 nex uniques. Hilt counts for 2.",
        "active": False},
    {
        "description": "Get a CM or HM Tob Kit/Dust",
        "active": False},
    {
        "description" : "Get 3 cox purples",
        "active": False},
    {
        "description" : "Get 5 ToA purples",
        "active" : False},
    {
        "description": "Get 2 Torva Drops",
        "active": False},
    {
        "description": "Get 3 ToA Purples",
        "active": False},
    {
        "description": "Get 3 ToB Purples",
        "active": False},
    {
        "description": "Complete a Virtus Robe Set",
        "active": False}]

"MYSTERY TILE" = [{
        "description": "Pay to win: Donate 50m to the clan or go backwards l m a o",
        "active": False},
    {
        "description": "Every teammate has to get a ToB kc. It's cool if people that go out of town or whatever don't do it. Noobs have to get carried though.",
        "active": False},
    {
        "description": "GRIEFER TOB: 3 members of your team must take an enemy(the enemy teams get to choose) to ToB and get a kc. The enemy must do everything they can to stop you. Literally anything goes. The same enemy cannot be chosen twice.",
        "active": False},
    {
        "description": "SHANE TRAIN: Get a deathless Trio CM CoX Kc. Only one player is allowed to click in between phases at Olm. The players must form a train by following each other.",
        "active": False},
    {
        "description": "Autocomplete this tile",
        "active": False},
    {
        "description": "go back lmao",
        "active": False},
    {
        "description": "NO PANTS INFERNOOOOOOOOOOOOOOOOOOOOOOOOO",
        "active": False}]