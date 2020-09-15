import stanza
from quantulum3 import parser
import requests


def main(seed, lang):
    # This sets up a default neural pipeline in Lang
    if ',' in seed:
        seed=seed.replace(',',' , ')
    nlp = stanza.Pipeline(str(lang), use_gpu=False,
                          processors='tokenize,pos,lemma')
    doc = nlp(seed)
    res = {'type': None, 'data': []}
    for sent in doc.sentences:
        if lang != 'en':
            temp=sent.text.replace(',','and')
            response = requests.get(
                'https://api.mymemory.translated.net/get?q='+temp+'&langpair='+lang+'|en')
            translated_text = response.json()['responseData']['translatedText']
            print(translated_text)
            
        else:
            translated_text = sent.text

        quants = parser.parse(translated_text)
        
        for q in quants:
            
            if q.unit.entity.name == 'length' :
                
                res['data'].append([float(q.surface.split()[0]), q.surface.split()[1]])
    if len(res['data']) > 0:
        if len(res['data'])==1:
            if 'diameter' in translated_text:
                res['type'] = 'diametre'
            elif 'radius' in translated_text:
                res['type'] = 'radius'
            else:
                res['type'] = 'square'
        else:
            res['type'] = 'rectangle'
        print(res)
        del doc
        return res


    else:
        res['type'] = 'entity'

    for sent in doc.sentences:
        for word in sent.words:
            res['data'].append([word.lemma, word.upos, word.text])

    i = 0
    for w in res['data']:
        w.append(i)
        i = 0
        if w[1] == 'NUM':
            i = int(w[0])
    for i, w in enumerate(res['data']):
        if w[1] == 'NOUN':
            if i < len(res['data'])-1:
                if res['data'][i+1][1] == 'NOUN':
                    w[0] = w[0]+' '+res['data'][i+1][0]
                    w[2] = w[2]+' '+res['data'][i+1][2]
                    del res['data'][i+1]
    for w in res['data']:
        if w[1] == 'NOUN':
            if lang != 'en':
                response = requests.get(
                    'https://api.mymemory.translated.net/get?q='+w[0]+'&langpair='+lang+'|en')
                translated_word = response.json(
                )['responseData']['translatedText']
            else:
                translated_word = w[0]

            url = "https://api.giphy.com/v1/stickers/search?api_key=iidRVNv0y0mmMUNhYrwlVFufRdIeFLJP&q=" + \
                translated_word+"&limit=1&offset=1&rating=PG"
            response = requests.get(url)
            if (response.json()['data']):
                w[0] = response.json()['data'][0]['images']['downsized']['url']
            else:w[1]='NOUN_'
        if w[1] == 'PROPN' or w[1] == 'X':
            r2 = requests.get("https://api.genderize.io?name="+w[0])
            gender = r2.json()['gender']
            if gender == 'female':
                w[0] = 'https://media.giphy.com/media/ifMNaJBQEJPDuUxF6n/giphy.gif'
            else:
                w[0] = 'https://media.giphy.com/media/TiC9sYLY9nilNnwMLq/giphy.gif'
    print(res)
    del doc
    return res


#doc = nlp("There were 16 children on the school bus.8 children got off at the first stop.How many children were on the bus then?")
#doc=nlp("Karima has 3 bananas .")
#doc=nlp("Il y avait 16 enfants dans le bus scolaire. 8 enfants sont descendus au premier arrêt. Combien d'enfants étaient dans le bus?")
#doc=nlp("كان هناك 16 طفلاً في حافلة المدرسة. نزل 8 أطفال في المحطة الأولى. كم عدد الأطفال الذين كانوا في الحافلة؟")
#print(*[f'word: {word.text+" "}\tlemma: {word.lemma}\txpos: {word.upos}' for sent in doc.sentences for word in sent.words], sep='\n')
