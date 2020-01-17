import random

greet = [
    "Hi there!",
    "*nods*",
    "Heya!"
]
stop = [
    "Bye!",
    "See you!",
    "Goodbye!"
]
# search = [
#     "I'm on it",
#     "I'm searching the best hotel for you"
# ]
assist = [
    "I am doing my best to help you",
    "My purpose is to assist you",
    "I'l always willing to help"
]
thank = [
    "Welcome!",
    "Anytime!",
    "No problem!"
]


def getResponseForIntent(intent):
    # if intent == "ssist":
    #     return getRand(assist)
    if intent == "thank":
        return getRand(thank)
    if intent == "greet":
        return getRand(greet)
    if intent == "stop":
        return getRand(stop)
    # if intent == "task.search":
    #     return getRand(search)
    return "I didn't get that"


def getRand(responses):
    return random.choice(responses)
