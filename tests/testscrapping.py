import sys
from bs4 import BeautifulSoup
import requests
import re
import json
import pytest


class YouTubeVideo :
    
    def __init__(self,videoId):
        self.videoId=videoId
        self.url = 'https://www.youtube.com/watch?v=' + str(self.videoId)
        
    def init(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = re.search("var ytInitialData = ({.*?});", soup.prettify()).group(1)
        data_json = json.loads(data)
        videoData = self.getData(data_json,soup)
        return videoData
    
    def getUrl(self):
        return self.url
    
    def getVideoId(self):
        return self.videoId
    
    def getDescription(self,data):
        videoSecondaryInfoRenderer = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
        description = videoSecondaryInfoRenderer['description']['runs']
        fullDescription=""
        for k in description:
            fullDescription += str(k['text'])+"\n"
        return fullDescription
    
    def getLinks(self,data):
        videoSecondaryInfoRenderer = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
        timestamps = videoSecondaryInfoRenderer['description']['runs']
        links = {}
        for k in range(0,len(timestamps)):
            try:
                if str(timestamps[k]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url']).startswith("https://www.youtube.com"):
                   links["value" + str(k)] = str(timestamps[k]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])+"\n"
                else :
                    links["value" + str(k)] ="https://www.youtube.com" +str(timestamps[k]['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])+"\n"
            except KeyError:
                "nothing happened"
        return links
    
    
    
    def getData(self,data,soup):
        videoPrimaryInfoRenderer = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
        result={
        "title": soup.find("meta", itemprop="name")['content'],
        "name":soup.find("span", itemprop="author").next.next['content'],
        "videoId" : self.getVideoId(),
        "vues" :videoPrimaryInfoRenderer["viewCount"]["videoViewCountRenderer"]["viewCount"]["simpleText"],
        "likes" : videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['simpleText'],
        "description" : self.getDescription(data),
        "links" : self.getLinks(data)}
        return result


def test_answer():
    videoTest = YouTubeVideo("fmsoym8I-3o")
    response = requests.get(videoTest.url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = re.search("var ytInitialData = ({.*?});", soup.prettify()).group(1)
    data_json = json.loads(data)
    # Test de getVideoId
    assert videoTest.getVideoId() == "fmsoym8I-3o"
    assert videoTest.getVideoId() != "fmsoym8I-3"
    # Test de getUrl
    assert videoTest.getUrl() == "https://www.youtube.com/watch?v=fmsoym8I-3o"
    assert videoTest.getUrl() != "/watch?v=fmsoym8I-3o"
    # Test on vérifie qu'on obtient bien une description
    assert videoTest.getDescription(data_json) == "🍿 L'acteur Pierre Niney est dans L’interview face cachée ! Ces prochains mois, le format revient plus fort avec des artistes, sportifs, etc.\n🔔 Abonnez-vous pour ne manquer aucune vidéo.\n\nInterview réalisée à l’occasion de la sortie du film « Mascarade » réalisé par Nicolas Bedos, le 1er novembre 2022 au cinéma. Avec Pierre Niney, Isabelle Adjani, François Cluzet, Marine Vacth.\n\nChaleureux remerciements au cinéma mk2 Bibliothèque pour son accueil.\n\n—\n\n\n00:00\n Intro\n\n00:22\n 1\n\n03:32\n 2\n\n10:11\n 3\n\n14:09\n 4\n\n17:28\n 5\n\n20:10\n 6\n\n23:13\n 7\n\n39:22\n 8\n\n—\n\nPrésenté par Hugo Travers\n\nRéalisateur : Julien Potié\nJournalistes : Benjamin Aleberteau, Blanche Vathonne\n\nChargée de production déléguée : Romane Meissonnier\nAssistant de production déléguée : Clément Chaulet\nChargée de production exécutive : Marie Delvallée\n\nChef OPV : Lucas Stoll\nOPV : Pierre Amilhat, Vanon Borget\nElectricien : Alex Henry\nChef OPS : Victor Arnaud\nStagiaire image : Magali Faizeau\n\nMaquilleuse : Kim Desnoyers\nPhotographe plateau : Erwann Tanguy\n\nMonteur-étalonneur : Stan Duplan\nMixeuse : Romane Meissonnier\n\nCheffe de projets partenariats : Mathilde Rousseau\nAssistante cheffe de projets partenariats : Manon Montoriol\n\n—\n\n© HugoDécrypte / 2022\n"
    assert videoTest.getDescription(data_json) != ""
    assert videoTest.getDescription(data_json) != "https://www.youtube.com/watch?v=fmsoym8I-3o"
    # Test on vérifie qu'on arrive a obtenir un dictionnaire de liens
    assert videoTest.getLinks(data_json) == {
            "value1": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=0s\n",
            "value3": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=22s\n",
            "value5": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=212s\n",
            "value7": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=611s\n",
            "value9": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=849s\n",
            "value11": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=1048s\n",
            "value13": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=1210s\n",
            "value15": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=1393s\n",
            "value17": "https://www.youtube.com/watch?v=fmsoym8I-3o&t=2362s\n"
        }
    assert videoTest.getLinks(data_json) != "https://www.youtube.com/watch?v=fmsoym8I-3o"
    assert videoTest.getLinks(data_json) != ""
    assert type(videoTest.getLinks(data_json)) == type({})
    # Test on vérifie qu'on a bien les données voulues dans un dictionnaire 
    assert type(videoTest.getData(data_json,soup)) == type({})
    
    
    
    
   
