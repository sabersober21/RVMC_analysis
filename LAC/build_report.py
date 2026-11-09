import json,sys,os,html,csv
h=os.path.dirname(os.path.abspath(__file__))
R=json.load(open(h+'/reach_results.json')); B={k:v['births'] for k,v in json.load(open(h+'/births_2023_worldbank.json')).items()}
rows=list(csv.DictReader(open(h+'/reliance.csv'))); W=720; esc=lambda s:html.escape(str(s))
def hbars(items,mx,x0=230,unit='%',cls=None):
    xm=W-70; sc=lambda v:x0+(xm-x0)*v/mx; o=[]; y=4
    for lab,v,c,tip in items:
        o.append(f'<text x="{x0-12}" y="{y+15}" text-anchor="end" class="lab">{esc(lab)}</text>')
        o.append(f'<g><title>{esc(tip)}</title><rect x="{x0}" y="{y+3}" width="{max(sc(v)-x0,3):.1f}" height="17" rx="4" class="{c}"/></g>')
        o.append(f'<text x="{sc(v)+8:.1f}" y="{y+16}" class="val">{v:.0f}{unit}</text>'); y+=32
    return f'<svg viewBox="0 0 {W} {y+2}" role="img">{"".join(o)}</svg>'
def fig_reach():
    it=[]
    for o,lab in (('FDA or EMA','FDA or EMA (comparison)'),('ANVISA (Brazil)','ANVISA, Brazil'),('COFEPRIS (Mexico)','COFEPRIS, Mexico'),('ANMAT (Argentina)','ANMAT, Argentina'),('CECMED (Cuba)','CECMED, Cuba')):
        b=R[o]['base']; it.append((lab,b['share']*100,'mt' if o=='FDA or EMA' else 'm1',f'{lab}: {b["countries"]} countries, {b["births_m"]:.2f}M births a year ({b["share"]:.0%})'))
    it.insert(2,('ANVISA before October 2026',22.0,'m1','ANVISA before Mexico added it in 2026: 20 countries (22%)'))
    return hbars(it,100,x0=250)
def fig_status():
    s=R['births_share']
    it=[('Reliance on non-regional regulators only',s['reliance_non_lac_only']*100,'m1','Reliance laws name FDA, EMA and similar, but no Latin American regulator: 70% of births'),
        ('No reliance pathway (as of 2020)',s['no_reliance']*100,'m1','Bolivia, Chile, Cuba, Honduras, Nicaragua, Venezuela'),
        ('Recognise PAHO reference regulators',(s['recognise_lac']+s['crs'])*100,'m1','Dominican Republic, Ecuador, El Salvador, Guatemala, Paraguay, Uruguay and 14 Caribbean Regulatory System states')]
    return hbars(it,100,x0=300)
def fig_lever():
    x0,xm=170,W-70; sc=lambda v:x0+(xm-x0)*v/100; o=[]; y=4
    for k,lab in (('ANVISA (Brazil)','ANVISA'),('COFEPRIS (Mexico)','COFEPRIS'),('ANMAT (Argentina)','ANMAT'),('CECMED (Cuba)','CECMED')):
        a=R[k]['base']['share']*100; b=R[k]['amend_lists']['share']*100
        o.append(f'<text x="{x0-12}" y="{y+22}" text-anchor="end" class="lab">{lab}</text>')
        for v,c,dy,t in ((a,'m1',2,'Today'),(b,'m2',22,'If reliance lists added PAHO reference regulators')):
            o.append(f'<g><title>{lab}, {t}: {v:.0f}% of births</title><rect x="{x0}" y="{y+dy}" width="{max(sc(v)-x0,3):.1f}" height="16" rx="4" class="{c}"/></g><text x="{sc(v)+8:.1f}" y="{y+dy+13}" class="val">{v:.0f}%</text>')
        y+=52
    return f'<svg viewBox="0 0 {W} {y}" role="img">{"".join(o)}</svg>'
def t_countries():
    g={'Recognise PAHO reference regulators':[], 'Reliance on non-regional regulators only':[], 'No reliance pathway (as of 2020)':[], 'Caribbean Regulatory System (recognises PAHO reference regulators)':[]}
    for r in rows:
        k=('Caribbean Regulatory System (recognises PAHO reference regulators)' if r['crs_member']=='1' else 'Recognise PAHO reference regulators' if r['recognises_paho_reference']=='1' else 'No reliance pathway (as of 2020)' if r['reliance_any']=='0' else 'Reliance on non-regional regulators only')
        g[k].append(r)
    h='<div class="scroll"><table><thead><tr><th scope="col">Group</th><th scope="col">Countries (births a year, thousands)</th><th scope="col" class="n">Share of LAC births</th></tr></thead><tbody>'
    for k,v in g.items():
        v=sorted(v,key=lambda r:-B[r['iso3']])
        names=', '.join(f'{r["country"]} ({B[r["iso3"]]/1e3:.0f})'+(' *' if r['lac_partial'] else '') for r in v) if not k.startswith('Caribbean') else f'{len(v)} CARICOM states ({sum(B[r["iso3"]] for r in v)/1e3:.0f} in total)'
        h+=f'<tr><td>{k}</td><td>{esc(names)}</td><td class="n">{sum(B[r["iso3"]] for r in v)/sum(B.values()):.0%}</td></tr>'
    return h+'</tbody></table></div>'
s=open(sys.argv[1]).read()
for k,v in {'{{FIG_REACH}}':fig_reach(),'{{FIG_STATUS}}':fig_status(),'{{FIG_LEVER}}':fig_lever(),'{{T_COUNTRIES}}':t_countries(),'{{CSS}}':open(sys.argv[3]).read()}.items():
    assert k in s,k; s=s.replace(k,v)
open(sys.argv[2],'w').write(s)
