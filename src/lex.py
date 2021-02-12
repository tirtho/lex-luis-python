########### lex.py #################
# AWS Lex V2 Functions
####################################

import logging
import boto3
import botocore
from botocore.exceptions import ClientError
from botocore.config import Config

# Connect to Lex V2
def getLexV2Client():
    try:
        return True, boto3.client('lexv2-models')
    except ClientError as e:
        logging.error(e)
    return False, ''

def getLexV2Bot(lexV2Client, botName):
    try:
        bot = lexV2Client.list_bots(filters=
                    [
                        {
                            'name': 'BotName',
                            'values': [botName],
                            'operator': 'EQ'
                        }
                    ]
        )
        return True, bot
    except ClientError as e:
            logging.error(e)
    return False, ''

# Get the latest version of the Bot that is in 
# 'Available' state
def getLexV2BotLatestAvailableVersion(lexV2Client, theBotId):
    try:
        theBotVersions = lexV2Client.list_bot_versions(
            botId = theBotId,
            sortBy={
                'attribute': 'BotVersion',
                'order': 'Descending'
            }
        )
        for aVersion in theBotVersions["botVersionSummaries"]:
            if aVersion["botStatus"] == "Available":
                theLatestAvailableBotVersion = aVersion["botVersion"]
                return True, theLatestAvailableBotVersion
        return False, ''
    except ClientError as e:
            logging.error(e)
    return False, ''

# Get the list of locale Ids for a given Bot and its 
# version Id
def getLexV2BotLocales(lexV2Client, theBotId, theBotVersion):
    try:
        listOfLocatesForTheLatestAvailableVersionOfTheBot = lexV2Client.list_bot_locales(
            botId=theBotId,
            botVersion=theBotVersion
        )
        localeIds = []
        for aLocaleSummary in listOfLocatesForTheLatestAvailableVersionOfTheBot["botLocaleSummaries"]:
            aLocaleId = aLocaleSummary["localeId"]
            # If locale not built, just do not return it
            if aLocaleSummary["botLocaleStatus"] == "Built":
                localeIds.append(aLocaleId)
        return True, localeIds
    except ClientError as e:
            logging.error(e)
    return False, ''

# Given a localeId for a Bot Id and Version, get the locale name
def getLexV2BotLocalName(lexV2Client, theBotId, theBotVersion, theBotLocaleId):
    try:
        locale = lexV2Client.describe_bot_locale(botId=theBotId, botVersion=theBotVersion, localeId=theBotLocaleId)
        return True, locale["localeName"]
    except ClientError as e:
            logging.error(e)
    return False, ''



# Get the intest for a given Bot, its version and locale
def getLexV2BotIntents(lexV2Client, theBotId, theBotVersion, theBotLocaleId):
    try:
        listOfIntents = lexV2Client.list_intents(
            botId=theBotId,
            botVersion=theBotVersion,
            localeId=theBotLocaleId
        )
        intentIds = []
        for anIntentSummary in listOfIntents["intentSummaries"]:
            anIntentId = anIntentSummary["intentId"]
            intentIds.append(anIntentId)
        return True, intentIds
    except ClientError as e:
            logging.error(e)
    return False, ''

# Get the details of an Intent
def getLexV2BotIntentDetails(lexV2Client, theBotId, theBotVersion, theBotLocaleId, theBotIntentId):
    try:
        thisIntent = lexV2Client.describe_intent(
                intentId=theBotIntentId, 
                botId=theBotId,
                botVersion=theBotVersion,
                localeId=theBotLocaleId
                )
        return True, thisIntent
    except ClientError as e:
        logging.error(e)
    return False, ''