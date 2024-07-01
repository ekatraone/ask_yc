# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
import WATI as wa
import operations as op
import openai
import pymongo
from dotenv import load_dotenv
import os
import mongoDB as mdb
load_dotenv()

openai.organization = os.environ['org']
openai.api_key = os.environ['api_key']


# print("openai.organization ", openai.organization)

# Flask constructor takes the name of
# current module (__name__) as argument.
# run_with_ngrok(app)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
# st.title("Ekatra QnA")

app = Flask(__name__)


# @app.route('/')
# def hello():
#     return 'Webhooks with Python'

def init_mongo():
    client = pymongo.MongoClient(
        "mongodb+srv://root:root@cluster0.m3gwy.mongodb.net/?retryWrites=true&w=majority")
    db = client["trained_documents"]
    collection = db["yc_summ_embedds"]


@app.route('/yc', methods=['POST', 'GET'])
def githubIssue():
    # if bool(data):

    data = request.json

    print(data)
    senderID = data['waId']
    name = data['senderName']
    # if (data['text'] == 'hi'):
    #     wa.sendText("Hello", senderID)
    if data['text'] != None:
        if data['text'] == 'Ask YC':

            existing_record = mdb.find_user(senderID)
            if existing_record:
                print("1. existing_record ", existing_record)
                mdb.update_chat_status(senderID, "open")
                wa.sendText("""Welcome to Ask YC! Whether you're a seasoned entrepreneur or just starting out on your business journey, I'm here to help you succeed.

As an AI assistant trained on YC's YouTube videos (thanks to Alex, Eightify.app) I'm here to help provide answers and insights for any questions you might have related to entrepreneurship, startups, or anything else related to Y-Combinator's knowledge base.

Simply type in your question and I'll do my best to provide you with a helpful response. Let's get started!""", senderID)

                wa.sendText("""Here are a few sample questions related to entrepreneurship and startups that you can ask me:

1. How do I come up with a business idea?
2. How can I validate my startup idea?
3. What are some best practices for fundraising?
4. How do I build a strong team for my startup?
5. How can I effectively market my product or service?
6. What are some common mistakes to avoid as an entrepreneur?
7. How can I stay motivated while building""", senderID)

            else:
                print("2. existing_record ", existing_record)
                record_created = mdb.create_record(senderID, name)
                print("record_created ", record_created)

                if record_created == "Success":

                    wa.sendText("""Welcome to Ask YC! Whether you're a seasoned entrepreneur or just starting out on your business journey, I'm here to help you succeed.

As an AI assistant trained on YC's YouTube videos (thanks to Alex, Eightify.app) I'm here to help provide answers and insights for any questions you might have related to entrepreneurship, startups, or anything else related to Y-Combinator's knowledge base.

Simply type in your question and I'll do my best to provide you with a helpful response. Let's get started!""", senderID)

                wa.sendText("""Here are a few sample questions related to entrepreneurship and startups that you can ask me:

1. How do I come up with a business idea?
2. How can I validate my startup idea?
3. What are some best practices for fundraising?
4. How do I build a strong team for my startup?
5. How can I effectively market my product or service?
6. What are some common mistakes to avoid as an entrepreneur?
7. How can I stay motivated while building""", senderID)

        else:
            options = ["Start Day", "Let's Begin", "Yes, Next", "Continue", "Next", "Skip", "Ste-by-Step", "Start Now", "No, give me sometime", "Remind me later", "Yes, I would", "No, I’ll pass", "Okay, Next", "WomenWill", "Start WomenWill", "I am ready.", "No, I am not ready.", "WomenWill Program", "शुरू करें", "Track Registration", "Event Updates", "Invite your friends", "Yes, I have", "IT Track", "Social Track", "Education Track", "Yes", "No", "Ok", "Ekatra QnA Bot", "Hi", 'Hello, tell me about Ekatra QnA Bot', ".", "Hi", "Hello", "Hey", "Learn with ekatra", "ekatra demo", "?", "!", "?*", "!*",
                       "Neo update 2023", "Tell me more", "Good News!", "Start Upscale", "It's correct", "Yes, I would like to", "Yes, Update", "Start Course", "No, I'll pass.", "Chat with an AI", "Hello, tell me about ekatra", "MDLZ Next", "Knowledge Base", "MDLZ Mobius Chat", "Start MDLZ", "Mondelēz", "Yes, Let's do this!", "No, I'll pass.", "English", "Hindi", "Climate Change", "Entrepreneurship", "Day 1", "Start Course!", "What's New?", "Yes, Tell me!", "No, Not Interested", "Join the waitlist!", "That's exciting!", "Generate Course", "30 minutes", "1 hour", "2 hour", "About Mondelēz", "About Mondelez", "Ask Catalyst", "Hello, tell me about \"Financial Literacy Course\"", "Hi, I'm interested in the Bachelor of Design program. Can you tell me more about it?", "Yes, Please.", "Sounds interesting", "Career Opportunities", "🙏🏻 How to apply?", "Ask TPH", "Financial Literacy", "Ekatra, Generate Course", "ask kernel", "Hello, Tell me about FutureX Program"]

            keyword = data['text']
            keyword = keyword.lower()
            print(keyword, "Ask Catalyst" in keyword,
                  "Hey ekatra,\nTell me about Ask YC!" == keyword)
            match = 0
            # or "tell me about ask yc!" in keyword
            for option in options:
                if option.lower() == keyword or "Track" in keyword or "Invite" in keyword or "GNS" in keyword or "vnit" in keyword or "Global Nagpur Summit" in keyword or "Track" in keyword or len(keyword) == 1 or "hello, tell me about ekatra" in keyword:
                    match += 1
                    # print(type(senderID))
                    mdb.update_chat_status(senderID, "Closed")

            print("matched ", match)
            if (match == 0):

                status = mdb.check_status(senderID)
                print(status)

                if status == "open":
                    query = data['text']
                    content_embeddings = mdb.retrieve_npy_file()

                    # print(content_embeddings)
                    concat_list = mdb.retrieve_list()

                    ans = op.process_main(
                        senderID, query, content_embeddings, concat_list)
                    wa.sendText(ans, senderID)
                    mdb.chat_log(senderID, query, ans)

    return data


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=6000)
    # app.run(debug=True, port=4000)
