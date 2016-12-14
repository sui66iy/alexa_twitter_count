
from __future__ import print_function
import json

from celebrity import Celebrinator

app_id = ''

def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    if (event['session']['application']['applicationId'] != app_id):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

    return

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

    return

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    return

def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    return get_welcome_response()

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == 'NumFollowers':
        return num_followers(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return help()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def get_welcome_response():
    session_attributes = {}

    card_title = "Welcome to My Test" 
    speech_output = "Welcome to My Test. " \
      "I can help you count the number of followers of your favorite celebrities! " \
      "You can say, how many followers does Michael Higgins have?"
    reprompt_text = "Try saying, how many people follow Donald Trump?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def help():
    session_attributes = {}

    card_title = "My Test Help" 
    speech_output = \
      "I can help you count the number of followers of your favorite celebrities! " \
      "You can say, how many followers does Michael Higgins have?"
    reprompt_text = "Try saying, how many people follow Donald Trump?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Thanks!"
    speech_output = "Check back soon for the latest Twitter counts!"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def num_followers(intent, session):
    card_title = "Followers"
    session_attributes = session.get('attributes', {})
    should_end_session = True

    if 'Celebrity' in intent['slots']:
        celebrity = intent['slots']['Celebrity'].get('value')
    else:
        celebrity = None

    if celebrity is None:
        speech_output = "I need to know which celebrity you are curious about. " \
          "Try saying, how many followers does Hillary Clinton have?"
        should_end_session = False
    else:
        celebrinator = Celebrinator()
        try:
            speech_output = celebrinator.followers(celebrity)
            should_end_session = True
        except ValueError as e:
            speech_output = "I'm afraid I don't know that celebrity.  Try another one!"
            should_end_session = False

    reprompt_text = "You can ask me, how many people follow Kanye West?"

    return build_response(session_attributes,
                          build_speechlet_response(card_title,
                                                   speech_output,
                                                   reprompt_text,
                                                   should_end_session))    

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Standard',
            'title': title,
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    
