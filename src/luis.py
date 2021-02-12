########### luis.py #################
# Azure LUIS Functions
# Code Tested with Python 3.9
#####################################
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from functools import reduce

import json, time

def getLuisAuthoringClient(authoringEndpoint, authoringKey):
    try:
        client = LUISAuthoringClient(authoringEndpoint, CognitiveServicesCredentials(authoringKey))
        return True, client
    except Exception as err:
        print("Error getting LUIS Authoring Client. {}".format(err))
    return False

def getLuisApp(luisClient, appName):
    try:
        appInfoResponses = luisClient.apps.list()
        for aResponse in appInfoResponses:
            if aResponse.name == appName:
                return True, aResponse
        return False, ''
    except Exception as err:
        print("Error getting app {}.\n{}".format(appName, err))
    return False, ''

# Example of culture is 'en-us'
def createLuisApp(luisClient, appName, appCulture, appInitialVersion):
    appDefinition = {
        "name": appName,
        "initial_version_id": appInitialVersion,
        "culture": appCulture
    }
    # Create app
    try:
        appId = luisClient.apps.add(appDefinition)
        return True, appId
    except Exception as err:
        print("Error creating app {} with initial version {} and culture {}.\n{}".format(appName, appInitialVersion, appCulture, err))
    return False, ''

# Create intent for the app
def createLuisAppIntent(luisClient, appId, versionId, intentName):
    try:
        intentId = luisClient.model.add_intent(appId, versionId, name=intentName, raw=False)
        return True, intentId
    except Exception as err:
        print("Error creating Intent {} with initial version {} for app id {}.\n{}".format(intentName, versionId, appId, err))
    return False, ''

# Add example utterance to intent
def addLuisAppIntentUtterance(luisClient, appId, versionId, intentName, utteranceText):
    try:
        labeledExampleUtterance = {
            "text": utteranceText,
            "intentName": intentName
        }
        labeledExampleResponse = luisClient.examples.add(appId, versionId, labeledExampleUtterance, {'enableNestedChildren': True}, raw=False)
        return True, labeledExampleResponse
    except Exception as err:
        print("Error adding utterance '{}', to Intent {} with initial version {} for app id {}.\n{}".format(utteranceText, intentName, versionId, appId, err))
    return False, ''

# locale id value from Lex V2 is converted 
# to the value for the format of culture
# in LUIS
def lexLocaleToLuisCulture(lexLocaleId):
    return lexLocaleId.lower().replace('_', '-')
    