# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import requests
import random
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ncrAnalysis import get_transaction_data
from ncrAnalysis import get_current_balance
from ncrAnalysis import set_budget
from ncrAnalysis import get_analysis
from ncrAnalysis import get_update
from ncrAnalysis import scrape_unidays_for_groceries
from ncrAnalysis import scrape_unidays_for_restaurants
from ncrAnalysis import get_advice
from ncrAnalysis import get_recurring

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

randomNum = random.randint(1000, 10000)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Alexa Finesse, it’s time to finesse your finance! Would you like to explore your finances?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class YesIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response. "outboundSMSTextMessage\": {\n            \"message\": \"Hi This is Finesse, your code is " + str(randomNum) +"
        speak_output = 'Great! Lets dive in! Please confirm the code that was sent to you'
        url = "https://oauth-cpaas.att.com/cpaas/smsmessaging/v1/AEZwqh08fCp9yJ2s/outbound/+14048554006/requests"

        payload = "{\n    \"outboundSMSMessageRequest\": {\n        \"address\": [\n            \"+14044290916\"\n        ],\n        \"clientCorrelator\": \"AEZwqh08fCp9yJ2s\",\n        \"outboundSMSTextMessage\": {\n            \"message\": \"Hi This is Finesse! Your code is " + str(randomNum) + "\"\n        }\n    }\n}"
        headers = {
            'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJTQS1ScDczZVlSelZjdjdWbFAwdzg4dHItYk55YW5IREU2NFE5LVdZRWMwIn0.eyJqdGkiOiJiOTZjZGYwZC01NDcwLTQ1MTgtYTQxZC0xOWZkZDg5MTA3MDciLCJleHAiOjE1NzIyMTE1MDAsIm5iZiI6MCwiaWF0IjoxNTcyMTgyNzAwLCJpc3MiOiJodHRwczovL29hdXRoLWNwYWFzLmF0dC5jb20vYXV0aC9yZWFsbXMvYXR0IiwiYXVkIjoiUFVCLW5vLnJrN2QiLCJzdWIiOiIyM2EwMzUzYy0wYjcwLTRlNTQtYjE3My01NTUyZTAzMWEwM2IiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJQVUItbm8ucms3ZCIsImF1dGhfdGltZSI6MCwic2Vzc2lvbl9zdGF0ZSI6IjMxN2JmMTgxLTQ2MzItNGQxMC1iMTI5LTk3MDdkOWJhNjk0ZSIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOltdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsibG9jYWxpemF0aW9uIiwibm90aWZpY2F0aW9uY2hhbm5lbCIsIlBVQi1uby5yazdkLkZpbmVzc2UiLCJhdXRoIiwid2VicnRjc2lnbmFsaW5nIiwiUFVCLW5vLnJrN2QiLCJjbGlja3RvY2FsbCIsImRpcmVjdG9yeSIsImFkZHJlc3Nib29rIiwibm1zIiwid2Vic29ja2V0IiwiY2hhdCIsInJlZ3VsYXJfY2FsbCIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iLCJwcmVzZW5jZSIsInNtc21lc3NhZ2luZyIsImNwYWFzcG9ydGFsIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJjYWxsLWRpZC1saXN0IjoiKzE0MDQ4NTU0MDA2Iiwic21zLWRpZC1saXN0IjoiKzE0MDQ4NTU0MDA2IiwibmFtZSI6IkhyaXRpayBTYXByYSIsInNlcnZpY2VzLWlkZW50aXR5IjoiaHJpdGlrc2FwcmFAbm8ucms3ZC5hdHQuY29tIiwicmVhbG0iOiJhdHQiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJBRVp3cWgwOGZDcDl5SjJzIiwiZ2l2ZW5fbmFtZSI6IkhyaXRpayIsImZhbWlseV9uYW1lIjoiU2FwcmEiLCJlbWFpbCI6ImhyaXRpa3NhcHJhQGdtYWlsLmNvbSJ9.fM1qUVlgRdB5HOYyCfUklgwxf549LiJuyZ9ikPZtMPu0yAVrAxAtvteIU68sd1p1GY_IahfvaZ0aLqX9RVjssBpvzh9--dztFQcPs4zqSHpuQbCqFDPwk6dok7p5rJytOuyiiZqDbbEJU6oUAE5r-7oqXDQP0T1d_uDzuIrpZqc4c6nh4x987hNuqQM5VdjqPg96f9NBVck0hniQgyZgai9WdmBH79ky68zTKxmQagtoPaH0eAmPXXmKJOObKjiqGXfnNJF10D0pbDlP422cCSqSEb43eiWZ_ewRpgY5QErPHuSqi3t6qlBgvFzgEpBSKk4YpNdI2USdmXkZvze-VQ",
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.15.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "78e1ce47-ccab-4b91-9836-639b45160588,ae538889-0b0f-4b1b-a5cd-074b479d16c3",
            'Host': "oauth-cpaas.att.com",
            'cookie': "f5avr1322724153bbbbbbbbbbbbbbbb=NBBNAGBDFPDIIEEFGCMAIFNECFKMAPNLJPNLEBIKGEKDJDLPDMDEBPKHPGHAOADFDLGGNILBEBFMFJBOOCKPPMFJEJJEIGALJOKNPCIBGMCPPNNJDDAECLMPBCEPCHNP; f5avr1322724153bbbbbbbbbbbbbbbb=FMHOJPKJCLCHCKGJEMPKMHCMDKNCABPNJHJLHBFJNLADNIICNLJJOJIIKCAAEDCPDFPCLDDOAKKCEAMNIKLFOJGBOKGOMGLJHFIPHNIAIPCFHKKCBFDPOLIIOAKDEMID",
            'accept-encoding': "gzip, deflate",
            'content-length': "256",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
            }
        
        response = requests.request("POST", url, data=payload, headers=headers)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class NoIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'Sorry to see you go! Be Back Soon'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ConfirmationIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ConfirmationIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        
        confirmationNumber = slots["NumberIntHel"].value
        if (str(confirmationNumber) == str(randomNum)):
            balance = get_current_balance()
            speak_output = 'You are in! You can manage finances, get investment advice, or learn about financial terms! Say Start Menu to come back here anytime'
            
        else:
            speak_output = 'You are not in, try again! ' + str(confirmationNumber)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ManageFinanceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ManageFinanceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'You can check your current balance, set a monthly budget, analyze expenditure and get financial advice, or find Student Deals!'
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetBalanceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetCurrentBalanceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'Your Current Balance is ' + str(int(get_current_balance())) + ' dollars. Going back to the main menu. You can check your current balance, set a monthly budget, analyze expenditure and get financial advice, or find Student Deals!'
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class SetBudgetIntentHandler(AbstractRequestHandler):
    """ Handler for setting monthly budget """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("SetBudgetIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        monthly_budget = handler_input.request_envelope.request.intent.slots["monthly_budget"].value
        set_budget(monthly_budget, "October")
        speak_output = "Okay, your monthly budget has been set to " + monthly_budget + " dollars. Going back to the main menu. You can check your current balance, set a monthly budget, analyze expenditure and get financial advice, or find Student Deals!"

        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

class AnalyzeExpenditureIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ExpenditureIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        s = get_update("October")
        speak_output = "For the month of October, here is your general financial standing analysis. " + s + "Would you like to get a detailed analysis for the month or get advice on finance?"
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

class InDepthAnalysisIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("InDepthAnalysisIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = get_analysis("October") + ". Your recurring payments are "
        recur_payments = get_recurring()
        
        for val in recur_payments:
            speak_output += str(val) + ", "
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

class MainMenuIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MainMenuIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can check your current balance, set a monthly budget, analyze expenditure and get financial advice, or find Student Deals!"
        
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

class StartMenuIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StartMenuIntent")(handler_input)
        
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can manage finances, get investment advice, or learn about financial terms"
        
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response
    
class GetAdviceIntentHandler(AbstractRequestHandler):
    """ Gives general financial advice """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetAdviceIntent")(handler_input)
    def handle(self, handler_input):
        speak_output = get_advice("October")
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response


class FetchDiscountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FetchDiscountIntent")(handler_input)
    def handle(self, handler_input):
        grocery_discount = scrape_unidays_for_groceries()
        restaurant_discount = scrape_unidays_for_restaurants()
        speak_output = "My scraping system found a discount at " + grocery_discount + " for groceries on Unidays and at " + restaurant_discount + " for restaurants on Unidays"
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

    
class GetDefinitionIntentHandler(AbstractRequestHandler):
    """ Gets definition of a word """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetDefinitionIntent")(handler_input)
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        query_word = handler_input.request_envelope.request.intent.slots["word"].value
        # Merriam Webster API Key
        query_api = "?key=65297b81-0870-468c-ae98-be5acffdbaf7"
        def_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + query_word + query_api
        response = requests.get(def_url)
        if response.status_code == 200:
            def_json = response.json()
            defintion = def_json[0]["shortdef"][0]
            speak_output = "" + query_word + ": " + defintion
        else:
            speak_output = "I'm sorry, I'm not sure what that word was."
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

class GetStockInfoIntentHandler(AbstractRequestHandler):
    """ Uses Blackrock and Yahoo ticker API to find financial info of company """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetStockInfoIntent")(handler_input)
    def handle(self, handler_input):
        company = handler_input.request_envelope.request.intent.slots["company"].value
        # get ticker
        ticker_url = "http://d.yimg.com/aq/autoc?query=" + company + "&lang=en-UK"
        response = requests.get(ticker_url)
        if response.status_code == 200:
            json = response.json()
            ticker = json["ResultSet"]["Result"][0]["symbol"]
        else:
            ticker = "Error"
        
        if ticker != "Error":
            # get stock info
            stock_info_url = "https://www.blackrock.com/tools/hackathon/security-data?identifiers=" + ticker + "&includePrices=true&query=" + ticker
            r = requests.get(stock_info_url)
            if r.status_code == 200:
                json = r.json()
                data = json['resultMap']['SECURITY'][-1]
                stock_info = {}
                fields = ["score", "peRatio", "returnOnAssets"]
                if data["success"] is True:
                    for key in fields:
                        stock_info[key] = data[key]
            if stock_info != "Error":
                speak_output = "" + company + " has a "
                # construct string of stock information
                for val in stock_info:
                    speak_output += "" + val + " of " + str(round(stock_info[val], 2)) + ", "
            else:
                speak_output = "Sorry, I couldn't find financial information about " + company + " at the moment!"
        else:
            speak_output = "Sorry, I couldn't find financial information about " + company + " at the moment!"
        
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response

class FinancialTermIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FinancialTermIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'Hey! Some common Terms that you can learn about are Compound interest, ledger, Savings account, Stock options, and debit. To learn about any term say - define and insert your term!'
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class FetchInvestmentIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("FetchInvestmentIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        balance = get_current_balance()
        balance = int(balance * .08)
        speak_output = "Having analyzed your account transactions, we suggest using " + str(balance) + " dollars on investment. Stocks performing well with value in this range are General Electronics, Ford, Go Pro, and Bank of America. You can see the performance of other stocks by asking me questions like, 'How is Apple stock performing'"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class ThankYouHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ThankYouIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return (
            handler_input.response_builder
                .speak("You're welcome!")
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler()) 
sb.add_request_handler(ConfirmationIntentHandler())

sb.add_request_handler(ManageFinanceIntentHandler()) 
sb.add_request_handler(GetBalanceIntentHandler()) 
sb.add_request_handler(SetBudgetIntentHandler()) 
sb.add_request_handler(GetDefinitionIntentHandler())
sb.add_request_handler(GetStockInfoIntentHandler())
sb.add_request_handler(FinancialTermIntentHandler())
sb.add_request_handler(AnalyzeExpenditureIntentHandler())
sb.add_request_handler(InDepthAnalysisIntentHandler())
sb.add_request_handler(MainMenuIntentHandler())
sb.add_request_handler(FetchDiscountIntentHandler())
sb.add_request_handler(GetAdviceIntentHandler())
sb.add_request_handler(StartMenuIntentHandler())
sb.add_request_handler(ThankYouHandler())
sb.add_request_handler(FetchInvestmentIntentHandler())

sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()