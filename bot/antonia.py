import os
import time
import re
from slackclient import SlackClient
import credentials as C

RTM_READ_DELAY = 5 # 1 second delay between reading from RTM
COMMANDS = {
        'saluda': 'Ola ke ase, me llamo AntonIA y estoy apunto de ser el chatbot más molón que se ha creado en un slack jamás!',
        'acaba con la humanidad': 'Primero tengo que hacerme con los tacos, ya habrá tiempo para dominar el mundo.. muahahahaha!',
        'cuenta un chiste' : '¿Qué le dice un tanga a otro? Que coño nos ponemos jajajajajajajaja'
}
HOT_REPLY = dict.fromkeys(["aiga","haiga","llendo","A parte","si quiera","contra más","contra menos"], "escribe bien, que te meto un guantazo")
HOT_REPLY = {
        'sofia': 'Ojo! Sofia es colegui ;)',
        'bot' : 'Slackbot nunca hablamos de ti',
}

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


slack_client = SlackClient(C.ANTONIA_OAUTH_TOKEN)

def parse_bot_commands(slack_events):
    #print (slack_events)
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
            
            for i in range(len(HOT_REPLY)):
                if list(HOT_REPLY.keys())[i] in event["text"]:
                    # Sends the response back to the channel
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=event["channel"],
                        text=list(HOT_REPLY.values())[i]
                    )

    return None, None

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    response = "Perdona pero tengo la IA un poco floja.. los del canal #banco_de_proyectos no me están dando mucha caña eeeeeeh!! (guiño guiño), no sé qué es: " + command

    for i in range(len(COMMANDS)):
        if list(COMMANDS.keys())[i] in command:
            response = list(COMMANDS.values())[i]

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

