"""How far can a vaccine approved by a Latin American regulator travel through national reliance pathways?
Inputs: reliance.csv (Duran et al. 2021, updated for Brazil 2024, Argentina 2025, Mexico 2026), births_2023_worldbank.json."""
import csv,json,os
h=os.path.dirname(os.path.abspath(__file__))
rows=list(csv.DictReader(open(os.path.join(h,'reliance.csv'))))
B={k:v['births'] for k,v in json.load(open(os.path.join(h,'births_2023_worldbank.json'))).items()}
T=sum(B.values())
origins={'FDA or EMA':None,'ANVISA (Brazil)':'BRA','COFEPRIS (Mexico)':'MEX','ANMAT (Argentina)':'ARG','CECMED (Cuba)':'CUB'}
code={'ANVISA (Brazil)':'ANVISA','COFEPRIS (Mexico)':'COFEPRIS','ANMAT (Argentina)':'ANMAT','CECMED (Cuba)':'CECMED'}
def reach(o,home,crs_lac=False,amend=False):
    got=[]
    for r in rows:
        c=r['iso3']
        if c==home: continue
        any_=r['reliance_any']=='1'
        if o=='FDA or EMA': ok=any_
        else:
            ok=r['recognises_paho_reference']=='1' or code[o] in r['lac_partial'].split(',')
            if amend and any_: ok=True
        if ok: got.append(c)
    den=T-(B[home] if home else 0)
    return {'births_m':sum(B[c] for c in got)/1e6,'share':sum(B[c] for c in got)/den,'countries':len(got),'list':got}
res={'total_births_m':T/1e6}
for o,home in origins.items():
    res[o]={'base':reach(o,home),'crs_trusts_lac':reach(o,home,crs_lac=True),'amend_lists':reach(o,home,amend=True)}
grp=lambda k:sum(B[r['iso3']] for r in rows if k(r))/T
res['births_share']={'no_reliance':grp(lambda r:r['reliance_any']=='0'),'reliance_non_lac_only':grp(lambda r:r['reliance_any']=='1' and r['recognises_paho_reference']=='0' and r['crs_member']=='0'),
 'recognise_lac':grp(lambda r:r['recognises_paho_reference']=='1' and r['crs_member']=='0'),'crs':grp(lambda r:r['crs_member']=='1'),'bra_mex':(B['BRA']+B['MEX'])/T,'outside_bra_mex':1-(B['BRA']+B['MEX'])/T}
res['producers_no_lac']=[r['country'] for r in rows if r['iso3'] in('BRA','ARG','MEX','CUB','COL','CHL')]
print(json.dumps({k:(v if k!='FDA or EMA' else v) for k,v in res.items()},indent=1,default=float)[:4000])
json.dump(res,open(os.path.join(h,'reach_results.json'),'w'),indent=1)
