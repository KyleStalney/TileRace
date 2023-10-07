import json
import random
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

_tiers = ['Mechanical', 'Minigames', 'Skilling', 'Early Game', 'Mid Game', 'Late Game', 'End Game', 'MYSTERY']
_paths = {
    'start': [3, 1, 2, 4, 2, 7, 5, 0, 2, 5, 5, 1, 6, 0, 4, 1, 2, 7, 4, 5, 2, 0, 5],
    'long': [7, 0, 6, 5, 1, 2, 5, 3, 4, 2, 1, 7, 4, 3, 0],
    'short': [2, 1, 5, 6, 5, 0, 1, 7, 6, 5],
    'end': [5, 7, 1, 3, 1, 6, 0, 3, 4, 5, 6, 0, 5, 4, 2, 7]
}


def get_tier(path, tile):
    return _tiers[_paths[path][tile]]


def dice_roll() -> int:
    return random.randint(1, 5)


class TileRace:
    teams = {}
    signups = []
    challenges = {}

    def __init__(self):
        with open('tilerace.json') as f:
            data = json.load(f)
        if not data:
            raise Exception('Failed to load data from tilerace.json')
        self.teams = data.get('teams', None)
        self.signups = data.get('signups', None)
        self.challenges = data.get('challenges', None)

    def setup_challenges(self, team):
        current_challenges = self.challenges[team["tile_tier"]].copy()
        # pick 3 random challenges from challenge list, put in new list, save them to teams challenges
        new_challenges = []
        ranger = range(3)
        if team['tile_tier'] == 'MYSTERY':
            ranger = range(1)
        for i in ranger:
            roll = random.randint(0, len(current_challenges) - 1)
            new_challenges.append(current_challenges.pop(roll))
        team["challenges"] = new_challenges

    def save(self):
        data = {
            "teams": self.teams,
            'signups': self.signups,
            'challenges': self.challenges
        }

        with open('tilerace.json', 'w') as f:
            f.write(json.dumps(data))

    async def choice(self, message):
        team_name = self.get_team(str(message.author))
        team = self.teams[team_name]
        temp = message.content.split(" ")
        path = temp[1].lower()
        if path == 'short' or path == 'long':
            team['path'] = path
            message.reply(
                f"{team_name} has chosen the {path.title()} path."
            )

    def get_team(self, user):
        for team in self.teams:
            if str(user) in self.teams[team]['members']: return team

    async def signup(self, message):
        if message.author not in self.signups:
            self.signups.append(str(message.author))
        kyle = await message.guild.fetch_emoji(1160014756040687626)
        await message.add_reaction(kyle)
        self.save()
        log.info(f'signup,{message.author},added to signups')

    async def list(self, message):
        mod_role = message.guild.get_role(1160016095428739122)
        if mod_role not in message.author.roles:
            return
        await message.reply('\n'.join(self.signups))

    async def get_challenges(self, message):
        team = self.teams[self.get_team(message.author)]
        challenges = [x["description"] for x in team["challenges"]]
        for i in range(len(challenges)):
            challenges[i] = f"{i + 1}. {challenges[i]}"
        await message.reply("## Current Challenges\n" + '\n'.join(challenges))

    async def roll_back(self, message):
        team_name = self.get_team(str(message.author))
        team = self.teams[team_name]
        dice = random.randint(1, 3)
        cur_path = _paths[team['path']]
        new_pos = team['tile'] - dice
        if new_pos < 0:
            new_pos = 0

        team['tile'] = new_pos
        team['tile_tier'] = get_tier(team['path'], team['tile'])
        a = 'a'
        self.setup_challenges(team)
        challenges = [x["description"] for x in team["challenges"]]
        for i in range(len(challenges)):
            challenges[i] = f"{i + 1}. {challenges[i]}"

        if team['tile_tier'][0] == 'E':
            a = 'an'
        await message.reply(
            f"You have rolled a {dice}.\n"
            f"This brings you back to position **{new_pos + 1}** on the {team['path'].title()} path, which is {a} **{team['tile_tier']} tile**.\n"
            f"## Current Challenges\n" + '\n'.join(challenges)
        )
        self.teams[team_name] = team
        self.save()

    async def roll(self, message):
        team_name = self.get_team(str(message.author))
        team = self.teams[team_name]
        if not team['can_roll']:
            return
        dice = dice_roll()
        team['can_roll'] = False
        cur_path = _paths[team['path']]
        new_pos = team['tile'] + dice
        if new_pos + 1 > len(cur_path):
            if team['path'] == 'start':
                team['tile'] = new_pos - len(cur_path)

                await message.reply(
                    f"You have rolled a {dice}.\n"
                    f"**{team_name}** have reached the fork. Now you must make a `!choice` on which [path](<https://google.com>) to take.\n"
                    "Type `!choice long` for the long path, and `!choice short` for the short path.\n"
                    f"You will land on position {team['tile']}."
                )

            if team['path'] == 'end':
                new_pos = len(cur_path)
                team['tile'] = new_pos
                team['tile_tier'] = get_tier(team['path'], team['tile'])
                self.setup_challenges(team)
                await message.reply(
                    f"You rolled a {dice}!\nMoving **{team_name}** to position **{new_pos + 1}** on **the {team['path'].title()} path**")

            if team['path'] == 'long' or team['path'] == 'short':
                team['tile'] = new_pos - len(cur_path)
                team['path'] = 'end'
                await message.reply(
                    f"You have rolled a {dice}.\n"
                    f"**{team_name}** have reached the end of the fork. You are now on **the end path** at position {team['tile']}."
                )


        else:

            team['tile'] = new_pos
            team['tile_tier'] = get_tier(team['path'], team['tile'])
            await message.reply(
                f"You rolled a {dice}!\nMoving **{team_name}** to position {new_pos + 1}, which is a {team['tile_tier']} tile.\n"
                f""
            )
        self.setup_challenges(team)
        self.teams[team_name] = team
        self.save()

    async def complete(self, message, reaction, user):
        # get user team
        team_name = self.get_team(str(message.author))
        team = self.teams[team_name]
        if team["challenges"] == []:
            return
        # check if there are challenges currently
        # make sure message format
        messages = message.content.split(' ')
        if (messages[1] not in '123'
                or messages[0].lower() != '!complete'):
            return
        challenge = team["challenges"][int(messages[1]) - 1]["description"]
        if str(user) in team["members"]:
            return
        team["challenges"] = []
        team["can_roll"] = True
        if team['path'] == 'end' and team['tile'] == len(_paths['end']):
            await message.reply(
                f"{team_name} wins yay."
            )
            return

        await message.reply(
            f"**{team_name}** has completed: *{challenge}*\nThe team has been granted a `!roll`"
        )
        self.teams[team_name] = team
        self.save()
