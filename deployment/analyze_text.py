#import stanza
#stanza.download('en')       # This downloads the English models for the neural pipeline
#nlp = stanza.Pipeline('en') # This sets up a default neural pipeline in English
#doc = nlp("There were 16 children on the school bus.8 children got off at the first stop.How many children were on the bus then?")
#print(*[f'word: {word.text+" "}\tupos: {word.upos}\txpos: {word.xpos}' for sent in doc.sentences for word in sent.words], sep='\n')

import nltk
import requests
from textblob import TextBlob
def main(seed):
    # nlp = stanza.Pipeline('en') # This sets up a default neural pipeline in English
    # doc=nlp(seed)
    # res=[]
    # eq_stuff=[]
    # doc.sentences[0].print_tokens()
    # for sent in doc.sentences:
        
    #     for i,word in enumerate (sent.words):
    #         res.append([word.text,word.upos])
    #         if word.upos=='NUM':
    #             if sent.words[i+1].upos=='NOUN':
    #                 eq_stuff.append([word.text,sent.words[i+1].lemma])
    #             elif sent.words[i-1].upos=='NOUN':
    #                 eq_stuff.append([word.text,sent.words[i-1].lemma])
            
    # return 

    ##########################################################################################################
    # sentences = nltk.sent_tokenize(seed)
    # s=nltk.word_tokenize(seed)
    # res=[]
    # WNlemma = nltk.WordNetLemmatizer()
    # s=[WNlemma.lemmatize(t) for t in s]
    # s=nltk.pos_tag(s)
    # for w in s:
    #     if w[1]=='NN':
    #         r = requests.get('https://emoji-api.com/emojis?search='+w[0]+'&access_key=a22a954a78d0459b25f31381841facd8c16be0dd')
    #         if r.json()[0]['character'] == None:
    #             r2=requests.get('https://wordsapiv1.p.mashape.com/words/'+w[0]+'/synonyms')
    #             syn=r2.json()['synonyms']
    #             i=0
    #             while r.json()[0]['character'] ==None and i<len(syn):
    #                 r = requests.get('https://emoji-api.com/emojis?search='+syn[i]+'&access_key=a22a954a78d0459b25f31381841facd8c16be0dd')
    #                 i=i+1
    #         w=list(w)
    #         w[0]=r.json()[0]['character']
    #         w=tuple(w)
    #         res.append(w)
    ####################################################################################################################

    

    res=[]
    for s in nltk.sent_tokenize(seed):
        if '?' in s:
            seed=seed.replace(s,'')
    s=nltk.word_tokenize(seed)
    WNlemma = nltk.WordNetLemmatizer()
    s=[WNlemma.lemmatize(t) for t in s]
    s=nltk.pos_tag(s)
    for i ,w in enumerate(s):
        w=list(w)
        if w[1]=='NN':
            if list(s[i+1])[1]=='NN':
                w[0]=w[0]+' '+list(s[i+1])[0]
                del s[i+1]
        res.append(w)
    for w in res:
        if w[1]=='NN':
            print(w[0])
            url = "https://api.giphy.com/v1/stickers/search?api_key=iidRVNv0y0mmMUNhYrwlVFufRdIeFLJP&q="+w[0]+"&limit=1&offset=1"
            #url="https://api.giphy.com/v1/stickers/translate?api_key=iidRVNv0y0mmMUNhYrwlVFufRdIeFLJP&s="+w[0]
            response = requests.get(url)
            #w[0]=response.json()['data']['images']['downsized']['url']
            w[0]=response.json()['data'][0]['images']['downsized']['url']
        if w[1]=='NNP':
            r2=requests.get("https://api.genderize.io?name="+w[0])
            gender=r2.json()['gender']
            if gender=='female':
                w[0]='https://media.giphy.com/media/ifMNaJBQEJPDuUxF6n/giphy.gif'
            else :
                w[0]='https://media.giphy.com/media/TiC9sYLY9nilNnwMLq/giphy.gif'
    i=0
    for w in res:
        w.append(i)
        i=0
        if w[1]=='CD':
            i= int(w[0])
    
    
            
    print(res)
    return res

    



#main("There were 16 children on the school bus . 8 children got off at the first stop . How many children were on the bus ?")
main("Karima bought 4 bananas .")