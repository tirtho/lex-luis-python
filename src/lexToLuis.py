########### lexToLuis.py #############
# Reads Intents and utterences from Lex for a bot
# and writes corresponding Intents and utterences 
# to LUIS App
# Code Tested with Python 3.9
######################################
from lex import *
from luis import *
from utils import *
import os

# Start checking input arguments
# get the name of the bot 
# and name of the file where to save the bot details
if needHelp():
    exit()
# Get the bot name
status, optionVal = getArgumentValue('-e', '--lex-bot-name')
if status:
    inputBotName = optionVal
else:
    print("Lex V2 Bot name not passed in commandline.")
    print("{}".format(getHelpText()))
    exit()
# Get the name of file where the bot information 
# will be dumped
status, optionVal = getArgumentValue('-u', '--luis-app-name')
if status:
    appName = optionVal
else:
    print("LUIS App Name not passed in commandline.")
    print("{}".format(getHelpText()))
    exit()

# Connect with LUIS using the 
# authoring endpoint and the authoring key
# which is read from the ~/..azure/credentials file
# in the local machine
LUIS_AUTHORING_ENDPOINT = getConfigParameters(os.path.join(os.path.expanduser("~"), '.azure', 'credentials'), "luisAuthoringEndPoint")
LUIS_AUTHORING_KEY = getConfigParameters(os.path.join(os.path.expanduser("~"), '.azure', 'credentials'), 'luisAuthoringKey')
status, theLuisClient = getLuisAuthoringClient(LUIS_AUTHORING_ENDPOINT, LUIS_AUTHORING_KEY)
if status == False:
    print("Luis Client connection could not be obtained")
    exit()

# Now connect with Lex V2
# using the credentials from the ~/.aws/credentials file
# and configuration from the ~/.aws/config file
status, theLexV2Client = getLexV2Client()
if status == False:
    print("Not Found the Lex V2 Client")
    exit()

print("Connected to Lex V2 Client")
foundBot = False
status, returnedBotList = getLexV2Bot(theLexV2Client, inputBotName)
if status:
    for aBot in returnedBotList['botSummaries']:            
        if aBot["botName"] == inputBotName:
            foundBot = True
            theLexV2Bot = aBot
            break
if foundBot == False:
    print("Not Found Bot {}".format(inputBotName))
    exit()

print("Bot {}, with bot id = {} and status = {}"
    .format(theLexV2Bot["botName"], 
        theLexV2Bot["botId"],
        theLexV2Bot["botStatus"]
        )
    )

# Find the latest version of the Bot
status, latestAvailableVersionOfTheBot = getLexV2BotLatestAvailableVersion(theLexV2Client, theLexV2Bot["botId"])
if status == False:
    print("Not Found the latest version of the Lex V2 Bot {}, with status as 'Available'".format(theLexV2Bot["botName"]))
    exit()

print("Bot {} latest 'Available' version is {}"
    .format(theLexV2Bot["botName"], latestAvailableVersionOfTheBot))
# Find the list of locales for the latest version of the Bot
status, localeList = getLexV2BotLocales(theLexV2Client, theLexV2Bot["botId"], latestAvailableVersionOfTheBot)
if status == False:
    print("Not found the list of locales for the version {} of the Bot {}"
        .format(theLexV2Bot["botName"], latestAvailableVersionOfTheBot))
    exit()

# For each locale, get the list of intents 
# and for each intent in the list
# get the details of the Intent
for localeId in localeList:
    
    appCulture = lexLocaleToLuisCulture(localeId)
    print("\tFor Lex locale Id {}, LUIS culture {}"
        .format(localeId, appCulture))

    # Difference between Lex and LUIS
    # In Lex each App can have multiple locales
    # In LUIS each App has one locale, i.e. referred to as culture
    # Also, App name has to be unique in both Lex and LUIS
    # So, we will create the name of App in LUIS as 
    # AppName-<appCulture>
    # Create the LUIS App for the given Lex Locale (i.e. LUIS culture)
    # Create an App
    # Check if the LUIS app is already there
    fullAppName = appName + "-" + appCulture
    status, theLuisApp = getLuisApp(theLuisClient, fullAppName)
    if status:
        print("\tLuis App {} already exists. Exiting.".format(fullAppName))
        continue
    versionId = latestAvailableVersionOfTheBot

    status, appId = createLuisApp(theLuisClient, fullAppName, appCulture, versionId)
    if status == False:
        print("\tCould not create App {}. Exiting.".format(fullAppName))
        continue
    
    status, intentIdList = getLexV2BotIntents(theLexV2Client, 
                                theLexV2Bot["botId"],
                                latestAvailableVersionOfTheBot,
                                localeId)
    if status == False:
        print("\t\tNot found list of Intents")
        continue
    for intentId in intentIdList:
        status, intentDetails = getLexV2BotIntentDetails(theLexV2Client, 
                                    theLexV2Bot["botId"], 
                                    latestAvailableVersionOfTheBot, 
                                    localeId, 
                                    intentId)
        if status == False:
            print("\t\tNot found details for Intent Id {}".format(intentId))
            continue
        print("\t\tFor Intent {} with Id {}".format(intentDetails["intentName"], intentId))

        # Check if Intent is present in LUIS
        # If not create the Intent
        # Create an Intent
        intentName = intentDetails["intentName"]
        status, intentId = createLuisAppIntent(theLuisClient, appId, versionId, intentName)
        if status == False:
            print("\t\tCould not create Intent {} for App {}. Exiting.".format(intentName, fullAppName))
            continue
        if "sampleUtterances" not in intentDetails:
            print("\t\tNo utterences present")
            continue
        # Add utterances
        sampleUtterances = intentDetails["sampleUtterances"]
        for lexSampleUtterance in sampleUtterances:
            status, labeledExampleResponse = addLuisAppIntentUtterance(theLuisClient, appId, versionId, intentName, lexSampleUtterance["utterance"])
            if status == False:
                print("\t\tCould not add utterance {} for Intent {}, in App {}. Exiting.".format(lexSampleUtterance["utterance"], intentName, fullAppName))
                continue
            print("\t\t\tUtterence - {}".format(labeledExampleResponse))

