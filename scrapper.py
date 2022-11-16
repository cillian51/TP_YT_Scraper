from bs4 import BeautifulSoup
import requests
import re
import json
import argparse



class YouTubeVideo :
    
    def __init__(self,videoId):
        """Constructeur de notre classe

        Args:
            videoId (string): Id de notre vidéo
        """
        self.videoId=videoId
        self.url = 'https://www.youtube.com/watch?v=' + str(self.videoId)
        
    def init(self):
        """Fonction qui va créer notre dictionnaire de données de la vidéos voulues

        Returns:
            dict: données recherchées dans l'url de la vidéo
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = re.search("var ytInitialData = ({.*?});", soup.prettify()).group(1)
        data_json = json.loads(data)
        videoData = self.getData(data_json,soup)
        return videoData
    
    def getUrl(self):
        """Return Url de la vidéo

        Returns:
            str: url de la vidéo
        """
        return self.url
    
    def getVideoId(self):
        """return Id de la vidéo

        Returns:
            str: Id de la vidéo
        """
        return self.videoId
    
    def getDescription(self,data):
        """return la description de la vidéo

        Args:
            data (json file): données de l'url
        Returns:
            str: description de la vidéo
        """
        videoSecondaryInfoRenderer = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']
        description = videoSecondaryInfoRenderer['description']['runs']
        fullDescription=""
        for k in description:
            fullDescription += str(k['text'])+"\n"
        return fullDescription
    
    def getLinks(self,data):
        """return un dictionnaire des différents liens de la description de la vidéo

        Args:
            data (json file): données de l'url

        Returns:
            dict: les différents liens de la description de la vidéo
        """
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
        """return un dictionnaire contenant les données voulues de la vidéo

        Args:
            data (json file): données de l'url
            soup (Beautiful Soup)

        Returns:
            dict: les différentes données voulues de la vidéo
        """
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



parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='infile',
                    help="input file", metavar='INPUT_FILE')
parser.add_argument('--output', dest='outfile',
                    help='output file', metavar='OUTPUT_FILE')
args = parser.parse_args()

with open(args.infile, 'r') as f:
   data = json.load(f)



output ={}
for k in range(0,len(data['videos_id'])):
    output["videos_id"+str(k)] =YouTubeVideo(data['videos_id'][k]).init()



with open(args.outfile, 'w') as jsonfile:
    json.dump(output,jsonfile,ensure_ascii=False, indent=4)
