import random


def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == '!roll':
        return str(random.randint(1, 6))


    if p_message == '!help':
        return "`This is a help message you can modify`"
    '''
    if p_message == '!help':
        return "Here is a list of commands you can use: " + "\n !signup : Enrolls you in the event " + "\n !complete : Team captains can confirm another team's tile" + "\n !roll : Rolls the dice" + "\n !hi : placeholder"
        '''