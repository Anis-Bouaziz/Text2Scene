import stanza
import requests  
def main(seed,lang): 
    nlp = stanza.Pipeline(str(lang),use_gpu=False,processors='tokenize,pos,lemma') # This sets up a default neural pipeline in English
    #doc = nlp("There were 16 children on the school bus.8 children got off at the first stop.How many children were on the bus then?")
    #doc=nlp("Karima has 3 bananas .")
    #doc=nlp("Il y avait 16 enfants dans le bus scolaire. 8 enfants sont descendus au premier arrêt. Combien d'enfants étaient dans le bus?")
    #doc=nlp("كان هناك 16 طفلاً في حافلة المدرسة. نزل 8 أطفال في المحطة الأولى. كم عدد الأطفال الذين كانوا في الحافلة؟")
    #print(*[f'word: {word.text+" "}\tlemma: {word.lemma}\txpos: {word.upos}' for sent in doc.sentences for word in sent.words], sep='\n')
    doc=nlp(seed)
    res=[]
    for sent in doc.sentences :
        for word in sent.words:
            res.append([word.lemma,word.upos,word.text])

    i=0
    for w in res:
        w.append(i)
        i=0
        if w[1]=='NUM':
            i= int(w[0])
    for i,w in enumerate(res):
        if w[1]=='NOUN':
            if i<len(res)-1 :
                if res[i+1][1]=='NOUN':
                    w[0]=w[0]+' '+res[i+1][0]
                    w[2]=w[2]+' '+res[i+1][2]
                    del res[i+1]
    for w in res:
            if w[1]=='NOUN':
                url = "https://api.giphy.com/v1/stickers/search?api_key=iidRVNv0y0mmMUNhYrwlVFufRdIeFLJP&q="+w[0]+"&limit=1&offset=1"
                response = requests.get(url)
                w[0]=response.json()['data'][0]['images']['downsized']['url']
            if w[1]=='PROPN' or w[1]=='X':
                r2=requests.get("https://api.genderize.io?name="+w[0])
                gender=r2.json()['gender']
                if gender=='female':
                    w[0]='https://media.giphy.com/media/ifMNaJBQEJPDuUxF6n/giphy.gif'
                else :
                    w[0]='https://media.giphy.com/media/TiC9sYLY9nilNnwMLq/giphy.gif'   
    
    return res




