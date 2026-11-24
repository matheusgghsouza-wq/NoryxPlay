import json, re, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro('kokoro-v1.0.onnx','voices-v1.0.bin')
# (texto falado, texto da legenda, pausa depois em s)
frases=[("Ai, gente, olha só essa novelinha!","Ai, gente, olha só essa novelinha!",0.25),
("Sabe aquele dorama que você começa dizendo: só um episódio?","Sabe aquele dorama que você começa dizendo ‘só um episódio’?",0.2),
("Pois é...","Pois é…",0.15),
("Já coloca na sua lista.","Já coloca na sua lista.",0.25),
("Quer ver qual é?","Quer ver qual é?",0.15),
("Clique no botão abaixo!","Clique no botão abaixo!",0.0)]
sr=24000; t=0.3; out=[np.zeros(int(sr*0.3))]; caps=[]
def trim(x):
    idx=np.where(np.abs(x)>0.01)[0]; return x[max(0,idx[0]-240):idx[-1]+480]
for fala,leg,pausa in frases:
    s,sr=k.create(fala,voice='pf_dora',speed=1.08,lang='pt-br'); s=trim(np.asarray(s))
    dur=len(s)/sr; words=leg.split(' ')
    w=[max(1,len(re.findall(r'[aeiouáéíóúâêôãõà]',x,re.I))) for x in words]; tot=sum(w); acc=t
    for i,(x,wi) in enumerate(zip(words,w)):
        d=dur*wi/tot; st=acc; acc+=d
        caps.append(dict(text=(' ' if i else '')+x,startMs=round(st*1000),endMs=round(acc*1000),timestampMs=round((st+d/2)*1000),confidence=None))
    caps[-1]['pageBreakAfter']=True
    out+= [s, np.zeros(int(sr*pausa))]; t+=dur+pausa
x=np.concatenate(out); x=x/np.abs(x).max()*0.9
sf.write('voz.wav',x,sr); print('total',round(len(x)/sr,2))
# envelope de abertura da boca por frame (30 fps)
fps=30; hop=sr//fps; env=[float(np.sqrt((x[i*hop:(i+1)*hop]**2).mean())) for i in range(int(np.ceil(len(x)/hop)))]
m=np.percentile(env,95); env=[round(min(1,e/m),3) for e in env]
json.dump(dict(legendas=caps,boca=env),open('dados-voz.json','w'),ensure_ascii=False)
for c in caps: print(c['text'],c['startMs'],c['endMs'],'|' if c.get('pageBreakAfter') else '')
