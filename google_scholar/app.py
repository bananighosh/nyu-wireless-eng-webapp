import json
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets("/Users/banani/nyu-wireless-eng-webapp/google_scholar/secrets.json", SCOPES)
  creds = tools.run_flow(flow, store)

form_service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC
)

# Request body for creating a form
NEW_FORM = {
    "info": {
        "title": "NYU Wireless Publications Categorizing form",
    }
}

def getFormQuestion(question, index):
  formQuestion = {
            "createItem": {
                "item": {
                    "title": (
                        question
                    ),
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "CHECKBOX",
                                "options": [
                                    {"value": "Wireless Communications and Sensing "},
                                    {"value": "Networking, Edge Computing, & Security"},
                                    {"value": "Circuits and Devices"},
                                    {"value": "Applications"},
                                    {"value": "AI/ML in Wireless"},
                                    {"value": "Testbeds and Prototypes"},
                                ],
                                "shuffle": True,
                            },
                            "textQuestion": {
                                "paragraph": False
                            },

                        }
                    },
                },
                "location": {"index": index},
            },
        }
  return formQuestion

result = form_service.forms().create(body=NEW_FORM).execute()


path = "/Users/banani/nyu-wireless-eng-webapp/google_scholar/author_pub_out_sorted.json"

with open(path, "r") as file:
    data = json.load(file)




title = data[0]["title"]

NEW_QUESTION = {
    "requests": []}
print(len(data))
for index, paperData in enumerate(data):
   question = paperData["title"]
   formQuestion = getFormQuestion(question, index)
   NEW_QUESTION["requests"].append(formQuestion)
   if index == 3:
      break

question_setting = (
    form_service.forms()
    .batchUpdate(formId=result["formId"], body=NEW_QUESTION)
    .execute()
)

# Prints the result to show the question has been added
get_result = form_service.forms().get(formId=result["formId"]).execute()
print(get_result["responderUri"])

