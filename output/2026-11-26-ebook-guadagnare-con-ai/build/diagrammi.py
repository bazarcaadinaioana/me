"""Genera i diagrammi SVG (IT/EN) usati nei libri. Uso: python3 diagrammi.py <cartella_immagini>"""
import sys, os
OUT = sys.argv[1]
INK="#1d2433"; ACC="#b8893b"; SOFT="#f3efe6"; MUTE="#6b7280"; LINE="#d9d2c3"
FONT="font-family:Inter,Helvetica,Arial,sans-serif"

def svg(w,h,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" style="{FONT}">{body}</svg>'
def box(x,y,w,h,fill=SOFT,stroke=LINE,r=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
def text(x,y,t,size=15,weight=400,fill=INK,anchor="middle"):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{t}</text>'
def arrow(x1,y1,x2,y2,c=ACC):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="2"/>'
            f'<polygon points="{x2},{y2} {x2-9},{y2-5} {x2-9},{y2+5}" fill="{c}"/>')

T = {
 "it": dict(
   tok_ctx="Contesto", tok_ctx2="«Il modo migliore per", tok_ctx3="iniziare è…»",
   tok_calc="Il modello calcola", tok_calc2="le probabilità",
   tok_opts=[("partire",.41),("scegliere",.22),("provare",.17),("…",.20)],
   tok_out="Sceglie un token", tok_out2="e ripete il ciclo",
   tok_loop="un token alla volta, finché la risposta è completa",
   pr=[("R","Ruolo","Chi deve essere l'AI"),("C","Contesto","La situazione"),("O","Obiettivo","Il risultato voluto"),("F","Formato","Forma e lunghezza"),("E","Esempi e vincoli","Cosa imitare ed evitare")],
   mx_x="Tempo per i primi incassi →", mx_y="Scalabilità →",
   mx_srv="SERVIZI", mx_prd="PRODOTTI",
   mx_items=[("Copywriting",.12,.18),("Gestione social",.2,.28),("Video promo",.35,.22),("Siti web",.42,.42),("Agenzia AI",.3,.5),("Immagini",.5,.52),("Etsy",.55,.7),("Prodotti digitali",.68,.8),("Ebook",.75,.75),("Corsi",.72,.88),("Amazon KDP",.86,.72),("Contenuti social",.92,.93)],
   fn=[("Scoperta","Ti conoscono"),("Interesse","Ti seguono"),("Fiducia","Si iscrivono"),("Acquisto","Comprano"),("Fedeltà","Tornano e consigliano")],
   w30=[("Settimana 1","Scegliere","Idea, nicchia,","concorrenza"),("Settimana 2","Costruire","Interviste,","versione minima"),("Settimana 3","Presentare","Prezzo, pagina,","lista email"),("Settimana 4","Testare","Contatti, lancio,","analisi")],
 ),
 "en": dict(
   tok_ctx="Context", tok_ctx2="“The best way to", tok_ctx3="get started is…”",
   tok_calc="The model calculates", tok_calc2="probabilities",
   tok_opts=[("to",.41),("simply",.22),("by",.17),("…",.20)],
   tok_out="It picks a token", tok_out2="and repeats the cycle",
   tok_loop="one token at a time, until the answer is complete",
   pr=[("R","Role","Who the AI should be"),("C","Context","The situation"),("O","Objective","The result you want"),("F","Format","Shape and length"),("E","Examples & limits","What to imitate and avoid")],
   mx_x="Time to first income →", mx_y="Scalability →",
   mx_srv="SERVICES", mx_prd="PRODUCTS",
   mx_items=[("Copywriting",.12,.18),("Social management",.2,.28),("Promo videos",.35,.22),("Websites",.42,.42),("AI agency",.3,.5),("Images",.5,.52),("Etsy",.55,.7),("Digital products",.68,.8),("Ebooks",.75,.75),("Courses",.72,.88),("Amazon KDP",.86,.72),("Social content",.92,.93)],
   fn=[("Discovery","They find you"),("Interest","They follow you"),("Trust","They subscribe"),("Purchase","They buy"),("Loyalty","They return and refer")],
   w30=[("Week 1","Choose","Idea, niche,","competition"),("Week 2","Build","Interviews,","minimum version"),("Week 3","Present","Price, page,","email list"),("Week 4","Test","Outreach, launch,","analysis")],
 )}

for lang,t in T.items():
    # token diagram
    b = box(10,40,190,120)+text(105,75,t["tok_ctx"],16,700)+text(105,105,t["tok_ctx2"],13,400,MUTE)+text(105,125,t["tok_ctx3"],13,400,MUTE)
    b += arrow(205,100,250,100)
    b += box(255,20,240,160,"#ffffff")+text(375,45,t["tok_calc"],14,700)+text(375,63,t["tok_calc2"],14,700)
    for i,(w,p) in enumerate(t["tok_opts"]):
        y=85+i*23
        b+=text(275,y+12,w,13,400,INK,"start")+f'<rect x="355" y="{y}" width="{p*280:.0f}" height="15" rx="3" fill="{ACC if i==0 else LINE}"/>'+text(470,y+12,f"{int(p*100)}%",12,600,MUTE,"end")
    b += arrow(500,100,545,100)
    b += box(550,40,180,120,INK,INK)+text(640,92,t["tok_out"],15,700,"#fff")+text(640,115,t["tok_out2"],13,400,"#e9e3d6")
    b += f'<path d="M640 165 C640 215, 105 215, 105 165" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="6 5"/>'+text(372,232,t["tok_loop"],13,400,MUTE)
    open(f"{OUT}/diagramma-token-{lang}.svg","w").write(svg(740,245,b))
    # prompt RCOFE
    b=""
    for i,(l,n,d) in enumerate(t["pr"]):
        x=10+i*146
        b+=box(x,20,134,170,"#fff")+f'<circle cx="{x+67}" cy="70" r="30" fill="{INK}"/>'+text(x+67,80,l,28,800,"#fff")
        b+=text(x+67,130,n,15,700)+text(x+67,155,d,11.5,400,MUTE)
        if i<4: b+=arrow(x+136,105,x+144,105)
    open(f"{OUT}/diagramma-prompt-{lang}.svg","w").write(svg(740,205,b))
    # matrix
    W,H,L,B=740,430,70,370
    b=f'<rect x="{L}" y="20" width="{W-L-20}" height="{B-20}" fill="#fff" stroke="{LINE}"/>'
    b+=f'<rect x="{L}" y="20" width="{(W-L-20)/2}" height="{B-20}" fill="{SOFT}"/>'
    b+=text(L+(W-L-20)/4,45,t["mx_srv"],13,800,MUTE)+text(L+3*(W-L-20)/4,45,t["mx_prd"],13,800,MUTE)
    b+=arrow(L,B+25,W-20,B+25,INK)+text((L+W)/2,B+50,t["mx_x"],13,600,INK)
    b+=f'<g transform="translate(35,{(B+20)/2}) rotate(-90)">'+text(0,0,t["mx_y"],13,600,INK)+'</g>'
    for n,x,y in t["mx_items"]:
        cx=L+20+x*(W-L-80); cy=B-15-y*(B-70)
        b+=f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="7" fill="{ACC}"/>'+text(cx+11,cy+5,n,12.5,600,INK,"start")
    open(f"{OUT}/diagramma-matrice-{lang}.svg","w").write(svg(W,H,b))
    # funnel
    b=""
    for i,(n,d) in enumerate(t["fn"]):
        w=700-i*110; x=(740-w)/2; y=10+i*52
        b+=f'<rect x="{x}" y="{y}" width="{w}" height="44" rx="8" fill="{INK if i==3 else ("#3a4357" if i<3 else ACC)}" opacity="{1-i*0.08 if i<3 else 1}"/>'
        b+=text(370,y+20,n,15,700,"#fff")+text(370,y+37,d,12,400,"#e9e3d6")
    open(f"{OUT}/diagramma-funnel-{lang}.svg","w").write(svg(740,275,b))
    # 30 days
    b=f'<line x1="40" y1="60" x2="700" y2="60" stroke="{LINE}" stroke-width="4"/>'
    for i,(w,v,d1,d2) in enumerate(t["w30"]):
        cx=95+i*183
        b+=f'<circle cx="{cx}" cy="60" r="22" fill="{ACC if i==3 else INK}"/>'+text(cx,67,str(i+1),18,800,"#fff")
        b+=text(cx,20,w,12,600,MUTE)+text(cx,112,v,17,800)+text(cx,135,d1,12,400,MUTE)+text(cx,152,d2,12,400,MUTE)
    open(f"{OUT}/diagramma-30giorni-{lang}.svg","w").write(svg(740,170,b))
print("ok")
