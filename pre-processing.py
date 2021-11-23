import nltk
import re
import string
import json



nltk.download("stopwords")


with open('dataset/famous_writer_raw.json', 'r', encoding='utf-8') as f:
  writer_data = json.loads(f.read())



def clean(text):

    text = re.sub("[a-zA-Z]", "", text) # remove english characters
    text ="".join([t for t in text if t not in string.punctuation]) # remove punctuations from text except fullstopsm
    text = " ".join(text.split())

    return text # replace full stop by spaces

preprocessed_output = writer_data.copy()


#இறப்பு, வயது

for ex in preprocessed_output:
  ex['வயது'] = None
  if ex['இறப்பு'] is not None:
    ex['இறப்பு'] = clean(ex['இறப்பு'])
    
    new = ex['இறப்பு'].split(' ')
    for e in range(len(new)):
      if ((new[e] == "அகவை" ) or (new[e] == "வயது")):
        ex['வயது'] = new[e+1]
        if len(ex['வயது']) > 2:
          ex['வயது'] = ex['வயது'][:2]
        ex['வயது'] = int(ex['வயது'])
        del new[e:e+2]
        break
    wen = list(reversed(new))
    dob = []
    for i in range (len(wen)):
      if (any(i.isdigit() for i in wen[i])):
        dob = wen[i:]
        break
    ex['இறப்பு'] = ' '.join(list(reversed(dob)))


#பிறப்பு, பிறந்த இடம்

for ex in preprocessed_output:
  ex['பிறந்த இடம்'] = None
  if ex['பிறப்பு'] is not None:
    ex['பிறப்பு'] = clean(ex['பிறப்பு'])
    
    new = ex['பிறப்பு'].split(' ')
    for e in range(len(new)):
      if (new[e] == "அகவை" ):
        if ex['வயது'] is None:
          ex['வயது'] = new[e+1]
        del new[e:e+2]
        break
    wen = list(reversed(new))
    dob,place = [],[]
    for i in range (len(wen)):
      if (any(i.isdigit() for i in wen[i])):
        dob = wen[i:]
        break
      else:
        place.append(wen[i])
    if len(place)==0:
      ex['பிறந்த இடம்'] = None
    else:
      ex['பிறந்த இடம்'] = ' '.join(list(reversed(place)))
    
    if len(dob)==0:
      ex['பிறப்பு'] = None
    else:
      ex['பிறப்பு'] = ' '.join(list(reversed(dob)))


#எழுதிய நூல்கள்

for ex in preprocessed_output:
  if ex['எழுதிய நூல்கள்'] is not None:
    new = []
    for i in range(len(ex['எழுதிய நூல்கள்'])):
      temp = clean(ex['எழுதிய நூல்கள்'][i])
      if temp == '↑':
        temp = ''
      new.append(temp)
    new = list(filter(None, new))
    ex['எழுதிய நூல்கள்'] = new


#அறியப்படுவது

for ex in preprocessed_output:
  if ex['அறியப்படுவது'] is not None:
    ex['அறியப்படுவது'] = ex['அறியப்படுவது'].split(',')
    new = []
    for i in range(len(ex['அறியப்படுவது'])):
      temp = clean(ex['அறியப்படுவது'][i])
      new.append(temp)
    new = list(filter(None, new))
    ex['அறியப்படுவது'] = new


#முக்கிய வார்த்தைகள்

for ex in preprocessed_output:
  if ex['முக்கிய வார்த்தைகள்'] is not None:
    new = []
    for i in range(len(ex['முக்கிய வார்த்தைகள்'])):
      temp = clean(ex['முக்கிய வார்த்தைகள்'][i])
      temp = temp.replace('பகுப்பு', '')
      new.append(temp)
    new = list(filter(None, new))
    ex['முக்கிய வார்த்தைகள்'] = new


def preprocess_fields(field):
    for ex in preprocessed_output:
        if ex[field] is not None:
            ex[field] = clean(ex[field])


common_fields = ["தேசியம்", "பட்டம்", "இருப்பிடம்", "பெயர்", "சுருக்கம்", "தகவல்"]

for i in common_fields:
    preprocess_fields(i)


#Saving cleaned data

with open('famous_writer_preprocessed.json', 'w') as f:
  json.dump(preprocessed_output, f)

