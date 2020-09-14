from quantulum3 import parser
import requests
def main(seed):
    response = requests.get('https://api.mymemory.translated.net/get?q='+seed+'&langpair=ar|en')
    t=response.json()['responseData']['translatedText']
    print(t)
    quants = parser.parse(t)
    print(quants)
main('أنيس له دائرة قطرها 100 متر')
