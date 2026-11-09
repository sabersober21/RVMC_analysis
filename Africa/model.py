"""Pricing the premium for African-made vaccines. Run: python model.py  (needs numpy, pandas)
Inputs: inputs.csv (CHAI 2030 demand, UNICEF 2026 Gavi-tier prices), yf_prices.csv (UNICEF YF table)."""
import json, os
import numpy as np, pandas as pd
here=os.path.dirname(os.path.abspath(__file__))
df=pd.read_csv(os.path.join(here,'inputs.csv'))
PI,S=0.41,0.30            # RVMC Indicator 5.1 premium; AU's 30% ask to Gavi
AVMA_PER_YEAR=100         # US$1bn over 10 years, yardstick only
INVEST=530                # Africa announced investment, US$M/yr 2022-24, Indicator 7.1a
GOV=13.5*44.9             # median gov vaccine spend per surviving infant x surviving infants
df['value_m']=df.demand_2030_m*df.price_ref
df['prem_per_dose']=df.price_ref*PI
df['bill_m']=df.value_m*PI*S
D,V=df.demand_2030_m.sum(),df.value_m.sum()
bill=lambda pi=PI,s=S,price='price_ref',dm=1.0:(df.demand_2030_m*dm*df[price]).sum()*pi*s
r={}
r['total_doses']=D; r['basket_value']=V; r['avg_price']=V/D
r['base_bill']=bill(); r['bill_pct_invest']=bill()/INVEST; r['bill_pct_gov']=bill()/GOV; r['gov_spend']=GOV
r['five_year_bill']=bill()*5
r['breakeven_premium']={str(s):AVMA_PER_YEAR/(V*s) for s in (.15,.30,.50,.60,1.0)}
r['grid']={f'{round(p*100)}':{f'{round(s*100)}':bill(p,s) for s in (.15,.30,.50,.75,1.0)} for p in (.15,.29,.41,.75,1.0)}
e=df[df.step=='End-to-end']; f=df[df.step=='Fill-finish']
r['e2e']={'doses':e.demand_2030_m.sum(),'share':e.demand_2030_m.sum()/D,'value':e.value_m.sum(),'bill_100pct':e.value_m.sum()*PI}
r['ff']={'doses':f.demand_2030_m.sum(),'share':f.demand_2030_m.sum()/D,'value':f.value_m.sum()}
# ceiling
for name,den in (('den_2035',1100),('den_2023',1412)):
    r[name]={'pipeline_100':D/den,'pipeline_30':D*S/den,'target_60_doses':.6*den,'gap_at_100':.6*den-D}
# AVMA+
r['avma_plus']={'per_dose':139/70,'vs_basket':(139/70)/(V/D)-1,'share_of_pipeline_year':70/D,'years_of_30pct':70/(D*S)}
# ramp 2027-2036: share linear 3%..30%, premium flat or gliding 41->0, demand flat at 2030
yrs=np.arange(10); sh=S*(yrs+1)/10; flat=(V*PI*sh).sum(); glide=(V*(PI*(1-yrs/9))*sh).sum()
r['ten_year']={'flat':flat,'glide':glide}
# one-way sensitivity
r['tornado']={'Premium 15% to 100%':[bill(pi=.15),bill(pi=1.0)],'African share 15% to 50%':[bill(s=.15),bill(s=.5)],
 'Reference prices low to high':[bill(price='price_low'),bill(price='price_high')],'2030 demand -20% to +20%':[bill(dm=.8),bill(dm=1.2)]}
# probabilistic sensitivity
rng=np.random.default_rng(20261105); n=200_000
pi=rng.triangular(.15,.41,1.0,n); s=rng.triangular(.15,.30,.50,n); dm=rng.triangular(.8,1,1.2,n)
tot=np.zeros(n)
for _,a in df.iterrows():
    lo,mo,hi=a.price_low,a.price_ref,a.price_high
    p=rng.triangular(lo,mo,hi,n) if hi>lo else np.full(n,mo)
    tot+=a.demand_2030_m*p
b=tot*dm*pi*s
r['psa']={'median':float(np.median(b)),'p2_5':float(np.percentile(b,2.5)),'p97_5':float(np.percentile(b,97.5)),'p_gt_100':float((b>100).mean()),'p_gt_530':float((b>530).mean()),'p_gt_0.5invest':float((b>265).mean())}
yf=pd.read_csv(os.path.join(here,'yf_prices.csv')); yf['premium']=yf.ipd_10dose/yf.lowest_other_10dose-1
r['yf']={'median':float(yf.premium.median()),'min':float(yf.premium.min()),'max':float(yf.premium.max()),'by_year':dict(zip(yf.year.astype(str),yf.premium.round(3)))}
r['antigens']=df.round(3).to_dict('records')
print(json.dumps(r,indent=1,default=float))
json.dump(r,open(os.path.join(here,'results.json'),'w'),indent=1,default=float)
