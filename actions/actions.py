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


class ActionSaveId(Action):                             # Custom action to save the ID given by Employee from Entity 'id' to Slot 'emp_id'

    def name(self) -> Text:
        return "action_save_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_id = next(tracker.get_latest_entity_values("id"),None)  # Fetching the latest value stored in entity "id"

        # dispatcher.utter_message(text="Hello World!")

        return [SlotSet("emp_id",current_id)]                           # Store the latest value of entity "id" to slot "emp_id"

# class Action_Display_Id(Action):                     # Custom action to display the ID which is saved in Slot 'emp_id'

#     def name(self) -> Text:
#         return "action_display_id"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         id_to_display = tracker.get_slot("emp_id")
        
#         msg = f"Your Employee ID is {id_to_display}"

#         dispatcher.utter_message(text=msg)

#         return []

class Action_Display_Emp_Details(Action):                # Custom action to display the Employee Detials based on ID which is saved in Slot 'emp_id'

    def name(self) -> Text:
        return "action_display_emp_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        id_to_display = tracker.get_slot("emp_id")      #Fetching the "emp_id" slot value

        client = pymongo.MongoClient("mongodb+srv://hrbot:hrbot123@cluster0.2c1m9.mongodb.net/?retryWrites=true&w=majority")    # creating  a MongoClient to the Mongo Atlass
        hrbot_db = client["hrbot"]                      #Getting hrbot Database
        emp_detail_collection=hrbot_db['emp_detail']    #Getting emp_detail Collection

        query={"emp_id":id_to_display}                  #our query to find Emp details based on emp_id
        
        emp_details = [emp_details for emp_details in emp_detail_collection.find(query)]  #Running the query

        if emp_details:
            emp_id = emp_details[0]["emp_id"]
            name = emp_details[0]["name"]
            location = emp_details[0]["location"]
            msg = f"Your details are as follows:- Employee ID: {emp_id}, Name: {name}, Location : {location}"
        else:
            msg = "Sorry, your Employee ID is not present in our Database."

        dispatcher.utter_message(text=msg)

        return []