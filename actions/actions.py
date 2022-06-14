# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import pymongo


class ActionSaveId(Action):

    def name(self) -> Text:
        return "action_save_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_id = next(tracker.get_latest_entity_values("id"),None)

        # dispatcher.utter_message(text="Hello World!")

        return [SlotSet("emp_id",current_id)]

# class Action_Display_Id(Action):

#     def name(self) -> Text:
#         return "action_display_id"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         id_to_display = tracker.get_slot("emp_id")
        
#         msg = f"Your Employee ID is {id_to_display}"

#         dispatcher.utter_message(text=msg)

#         return []

class Action_Display_Emp_Details(Action):

    def name(self) -> Text:
        return "action_display_emp_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        id_to_display = tracker.get_slot("emp_id")

        client = pymongo.MongoClient("mongodb+srv://hrbot:hrbot123@cluster0.2c1m9.mongodb.net/?retryWrites=true&w=majority")
        hrbot_db = client["hrbot"]
        emp_detail_collection=hrbot_db['emp_detail']

        query={"emp_id":id_to_display}
        
        emp_details = [emp_details for emp_details in emp_detail_collection.find(query)]

        if emp_details:
            emp_id = emp_details[0]["emp_id"]
            name = emp_details[0]["name"]
            location = emp_details[0]["location"]
            msg = f"Your details are as follows:- Employee ID: {emp_id}, Name: {name}, Location : {location}"
        else:
            msg = "Sorry, your Employee ID is not present in our Database."

        dispatcher.utter_message(text=msg)

        return []