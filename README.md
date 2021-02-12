# lex-luis-python

The python code here can be used to read LEx V2 Bot Intents, Utterences and upload in Azure LUIS Apps

TODO: implement code to also migrate slots and other components

## Prerequisites ##

#### Python 3.x ###
Download and install [Python 3.x][python-home] 

#### Boto3 installation ####
Install latest Boto3 release via pip:

	> pip install boto3

Refer [Boto3 Documents][boto3-installation]

#### Azure LUIS client library ####
Install the Language Understanding (LUIS) client library for python.

	> pip install azure-cognitiveservices-language-luis

Refer [LUIS Documentation][luis-docs]

#### Lex V2 Bot ####
Create a Bot in your AWS account in a language and add few intents, utterences with slots and test it. Refer [Lex V2 Quick Start Documentation][lex-quick-start]

Also, for the python code to connect with your Lex V2 Bot, 

1. Create ~/.aws/config file with input for region, as below

![AWS Config File](/images/aws-config.jpg)

2. Create ~/.aws/credentials file with input for aws credentials, as below
![AWS Credentials File](/images/aws-credentials.jpg)

#### Azure LUIS App ####
Create a LUIS App in Azure Cognitive Service with a few Intents with utterences and test. Refer [LUIS Quick Start Documentation][luis-quick-start]

Also, for the python code to connect with your LUIS instance, create the ~/.azure/credentials file as below
![Azure Credentials File](/images/azure-credentials.jpg)

## Code ##
The source files are in [source folder][src-folder]

Run the code below to get help information - 

	> python lexToLuis.py -h

Run the code below to copy from Lex V2 Bot to LUIS - 

	> python lexToLuis.py --lex-bot-name <lex v2 bot name> -u <LUIS app name>


[python-home]: <https://www.python.org/>
[boto3-installation]: <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html>
[luis-docs]: <https://docs.microsoft.com/en-us/azure/cognitive-services/luis/client-libraries-rest-api?pivots=programming-language-python&tabs=windows>
[lex-quick-start]: <https://docs.aws.amazon.com/lexv2/latest/dg/build-create.html>
[luis-quick-start]: <https://docs.microsoft.com/en-us/azure/cognitive-services/luis/get-started-portal-build-app>
[src-folder]: <https://github.com/tirtho/lex-luis-python/src>
