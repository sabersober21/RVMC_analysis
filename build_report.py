import json,sys,os,html
outdir,target=sys.argv[1],sys.argv[2]
r=json.load(open(outdir+'/analysis/results.json'))
A=r['antigens']
W=720
def esc(s): return html.escape(str(s))
def fig_ceiling():
    rows=[("Supplied by African manufacturers, 2023",12,"12M"),("30% of the eight pipeline vaccines, 2030 demand",150,"150M"),("100% of the eight pipeline vaccines, 2030 demand",500,"500M"),("60% target, on 1.1bn doses projected for 2035",660,"660M")]
    x0,xm=20,W-70; sc=lambda v:x0+(xm-x0)*v/700; o=[];y=8
    for i,(l,v,t) in enumerate(rows):
        o.append(f'<text x="{x0}" y="{y+12}" class="lab">{esc(l)}</text>')
        cls='m1' if i<3 else 'mt'
        o.append(f'<g><title>{esc(l)}: {t} doses</title><rect x="{x0}" y="{y+18}" width="{max(sc(v)-x0,3):.1f}" height="16" rx="4" class="{cls}"/></g>')
        o.append(f'<text x="{sc(v)+8:.1f}" y="{y+31}" class="val">{t}</text>'); y+=48
    return f'<svg viewBox="0 0 {W} {y+4}" role="img" aria-label="Doses: 12 million supplied in 2023, 150 million at 30 percent of pipeline, 500 million at 100 percent, against a 660 million target">{"".join(o)}</svg>'
def fig_antigen():
    a=sorted(A,key=lambda d:-d['bill_m']); x0,xm=150,W-70; mx=30; sc=lambda v:x0+(xm-x0)*v/mx; o=[]; y=6
    for d in a:
        c='m1' if d['step']=='Fill-finish' else 'm2'
        o.append(f'<text x="{x0-10}" y="{y+14}" text-anchor="end" class="lab">{esc(d["antigen"])}</text>')
        o.append(f'<g><title>{esc(d["antigen"])}: US${d["bill_m"]:.1f}M a year; {d["demand_2030_m"]:.0f}M doses; premium US${d["prem_per_dose"]:.2f} per dose</title><rect x="{x0}" y="{y+2}" width="{max(sc(d["bill_m"])-x0,3):.1f}" height="16" rx="4" class="{c}"/></g>')
        o.append(f'<text x="{sc(d["bill_m"])+8:.1f}" y="{y+15}" class="val">${d["bill_m"]:.1f}M</text>'); y+=28
    return f'<svg viewBox="0 0 {W} {y+2}" role="img" aria-label="Annual premium cost by vaccine at 41 percent premium and 30 percent African share">{"".join(o)}</svg>'
def fig_yf():
    d=[(2014,1.132,.84),(2015,1.132,.84),(2016,1.189,.84),(2017,1.189,.88),(2018,1.248,.97),(2019,1.31,.97),(2020,1.31,.97),(2021,1.46,.97),(2022,1.46,.97),(2023,1.533,1.15),(2024,1.533,1.15),(2025,1.533,1.15)]
    x0,xm,y0,ym=44,W-250,210,14; sx=lambda t:x0+(xm-x0)*(t-2014)/11; sy=lambda v:y0-(y0-ym)*(v-0.5)/1.25; o=[]
    for v in (.5,1,1.5):
        o.append(f'<line x1="{x0}" x2="{xm}" y1="{sy(v):.1f}" y2="{sy(v):.1f}" class="grid"/><text x="{x0-8}" y="{sy(v)+4:.1f}" text-anchor="end" class="tick">${v:.2f}</text>')
    for t in (2014,2017,2020,2023,2025):
        o.append(f'<text x="{sx(t):.1f}" y="{y0+20}" text-anchor="middle" class="tick">{t}</text>')
    for idx,cl in ((1,'s2'),(2,'s1')):
        p=' '.join(f'{sx(q[0]):.1f},{sy(q[idx]):.1f}' for q in d)
        o.append(f'<polyline points="{p}" class="{cl}" fill="none"/>')
        for q in d:
            prem=q[1]/q[2]-1
            o.append(f'<circle cx="{sx(q[0]):.1f}" cy="{sy(q[idx]):.1f}" r="4" class="d{cl}"><title>{q[0]}: Institut Pasteur de Dakar ${q[1]:.3f}; lowest other ${q[2]:.2f}; premium {prem:.0%}</title></circle>')
    o.append(f'<text x="{xm+12}" y="{sy(1.533)+4:.1f}" class="val">Dakar $1.53</text>')
    o.append(f'<text x="{xm+12}" y="{sy(1.15)+4:.1f}" class="val">Lowest other $1.15</text>')
    return f'<svg viewBox="0 0 {W} 238" role="img" aria-label="Yellow fever 10-dose price per dose, 2014 to 2025, Institut Pasteur de Dakar against lowest other UNICEF supplier">{"".join(o)}</svg>'
def fig_tornado():
    t=r['tornado']; base=r['base_bill']; x0,xm=210,W-60; sc=lambda v:x0+(xm-x0)*v/250; o=[];y=22
    items=sorted(t.items(),key=lambda kv:-(kv[1][1]-kv[1][0]))
    o.append(f'<line x1="{sc(base):.1f}" x2="{sc(base):.1f}" y1="16" y2="{22+len(items)*34}" class="refl"/><text x="{sc(base):.1f}" y="11" text-anchor="middle" class="tick">Base ${base:.0f}M</text>')
    for k,(lo,hi) in items:
        o.append(f'<text x="{x0-12}" y="{y+13}" text-anchor="end" class="lab">{esc(k)}</text>')
        o.append(f'<g><title>{esc(k)}: US${lo:.0f}M to US${hi:.0f}M a year</title><rect x="{sc(lo):.1f}" y="{y}" width="{sc(hi)-sc(lo):.1f}" height="18" rx="4" class="m1"/></g>')
        o.append(f'<text x="{sc(lo)-6:.1f}" y="{y+13}" text-anchor="end" class="val">${lo:.0f}M</text><text x="{sc(hi)+6:.1f}" y="{y+13}" class="val">${hi:.0f}M</text>'); y+=34
    return f'<svg viewBox="0 0 {W} {y+2}" role="img" aria-label="One-way sensitivity of the annual premium cost">{"".join(o)}</svg>'
def heat():
    g=r['grid']; ps=['15','29','41','75','100']; ss=['15','30','50','75','100']
    def bin(v):
        return 1 if v<=50 else 2 if v<=100 else 3 if v<=200 else 4 if v<=400 else 5
    h='<div class="scroll"><table class="heat"><thead><tr><th scope="col">Premium</th>'+''.join(f'<th scope="col">{s}% share</th>' for s in ss)+'</tr></thead><tbody>'
    for p in ps:
        tag={'29':'29%: RVMC vs PAHO','41':'41%: RVMC vs UNICEF'}.get(p,p+'%')
        h+=f'<tr><th scope="row">{tag}</th>'
        for s in ss:
            v=g[p][s]; base=' base' if p=='41' and s=='30' else ''
            h+=f'<td class="h{bin(v)}{base}">${v:.0f}M</td>'
        h+='</tr>'
    return h+'</tbody></table></div>'
def t_antigen():
    h='<div class="scroll"><table><thead><tr><th scope="col">Vaccine</th><th scope="col">African manufacturer</th><th scope="col">Step in Africa</th><th scope="col" class="n">2030 demand</th><th scope="col" class="n">Reference price</th><th scope="col" class="n">Premium per dose</th><th scope="col" class="n">Annual cost</th></tr></thead><tbody>'
    for d in sorted(A,key=lambda d:-d['demand_2030_m']):
        h+=f'<tr><td>{esc(d["antigen"])}</td><td>{esc(d["african_manufacturers"])}</td><td class="nw">{esc(d["step"])}</td><td class="n">{d["demand_2030_m"]:.0f}M</td><td class="n">${d["price_ref"]:.2f}</td><td class="n">${d["prem_per_dose"]:.2f}</td><td class="n">${d["bill_m"]:.1f}M</td></tr>'
    h+=f'<tr class="tot"><td colspan="3">Total</td><td class="n">{r["total_doses"]:.0f}M</td><td class="n">${r["avg_price"]:.2f} avg</td><td class="n">${r["avg_price"]*.41:.2f} avg</td><td class="n">${r["base_bill"]:.1f}M</td></tr></tbody></table></div>'
    return h
def t_prices():
    h='<div class="scroll"><table><thead><tr><th scope="col">Vaccine</th><th scope="col" class="n">Low</th><th scope="col" class="n">Reference</th><th scope="col" class="n">High</th><th scope="col">Basis (UNICEF awarded prices, FCA)</th></tr></thead><tbody>'
    for d in A:
        h+=f'<tr><td>{esc(d["antigen"])}</td><td class="n">${d["price_low"]:.2f}</td><td class="n">${d["price_ref"]:.2f}</td><td class="n">${d["price_high"]:.2f}</td><td>{esc(d["price_basis"])}</td></tr>'
    return h+'</tbody></table></div>'
body=open(sys.argv[3]).read()
for k,v in {'{{FIG_CEILING}}':fig_ceiling(),'{{FIG_ANTIGEN}}':fig_antigen(),'{{FIG_YF}}':fig_yf(),'{{FIG_TORNADO}}':fig_tornado(),'{{HEAT}}':heat(),'{{T_ANTIGEN}}':t_antigen(),'{{T_PRICES}}':t_prices()}.items():
    assert k in body,k; body=body.replace(k,v)
open(target,'w').write(body)
