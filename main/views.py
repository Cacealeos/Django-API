from sys import meta_path
from django.http.response import HttpResponse
from django.shortcuts import render
import requests
from django import forms
import dns
# import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pymongo import MongoClient
from datetime import date


# Create your views here.
    # API Auth Key - google
    # key=API_KEY
    # AIzaSyAT3tIXw3rlN27nY2KHDbpZ_pMoTL77fAI

class channelForm(forms.Form):
    channel = forms.CharField(label="channel")
    views = forms.IntegerField(label="views")
    uploads = forms.IntegerField(label="uploads")
    subs = forms.IntegerField(label="subs")


API_KEY = "AIzaSyAT3tIXw3rlN27nY2KHDbpZ_pMoTL77fAI"

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
#pw = "rRfj1UJQ1PMDbfe3"

def index(response):

    Api = requests.get("https://www.googleapis.com/youtube/v3/activities?key=" / API_KEY) 
    return render(response, "front.html", {"text": Api.text})

def main(response):
    
    db = "TestPyDB"
    PW = "rRfj1UJQ1PMDbfe3"
    # MG = MongoClient("mongodb+srv://Admin:"+ PW + ">@pycluster.ctt6i.mongodb.net/"+ db + "?retryWrites=true&w=majority")
    MG = MongoClient("mongodb+srv://Admin:rRfj1UJQ1PMDbfe3>@pycluster.ctt6i.mongodb.net/TestPyDB?retryWrites=true&w=majority")
    cl = MG[db]["TestPyCL"]
    rend = {}

    if response.method == "POST" and "Search" in response.POST: 
        
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.

        #client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
        # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
        # Get credentials and create an API client
        # flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        #     client_secrets_file, scopes)
        # credentials = flow.run_console()
        # youtube = googleapiclient.discovery.build(
        #     api_service_name, api_version, credentials=credentials)

        api_service_name = "youtube"
        api_version = "v3"
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=API_KEY)

        request = youtube.channels().list(
            part="statistics",
            forUsername=response["channel"]
        )
        siteResponse = request.execute()
        # capable of transition to and from json architype
        # JSdic = json.dumps(siteResponse)

        print(siteResponse)
        #print(JSdic)

        stats = siteResponse["items"][0]["statistics"]
        rend.update({"text": siteResponse, "TV": stats["viewCount"], "PV": stats["videoCount"], "SB": stats["subscriberCount"]})

        #return render(response, "front.html", rend)

    elif response.method == "POST" and "LogInfo" in response.POST:

        data = channelForm(response.POST)
        if data.is_valid():

            today = date.now()
            post = {"Channel": data.cleaned_data["channel"], "Views": data.cleaned_data["views"], "Uploads": data.cleaned_data["uploads"], "Subs": data.cleaned_data["subs"], "Data": today}
            cl.insert_one(post)
    
    results = cl.find({})

    rend.update(results)

    return render(response, "front.html", rend)
# if __name__ == "__main__":
#     main()