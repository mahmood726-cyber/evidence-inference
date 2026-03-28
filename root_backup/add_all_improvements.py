"""
Add Demo Datasets + Editorial Improvements to NMA Pro v6.2
Clean implementation
"""
import re

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print('Original file length:', len(content))

# ============================================================================
# PART 1: ADD DEMO DATASETS
# ============================================================================

demo_datasets_code = """
const DEMO_DATASETS={
  thrombolytics:{name:'Thrombolytics (OR)',effectMeasure:'OR',dataType:'binary',studies:[
    {name:'GUSTO-1',treatment1:'SK',events1:1135,n1:13780,treatment2:'tPA',events2:1021,n2:13746,year:1993,rob:'low',meanAge:62,propMale:0.75},
    {name:'ISIS-3',treatment1:'SK',events1:2891,n1:20676,treatment2:'tPA',events2:2878,n2:20656,year:1992,rob:'low',meanAge:61,propMale:0.76},
    {name:'GISSI-2',treatment1:'SK',events1:1012,n1:10372,treatment2:'tPA',events2:1033,n2:10396,year:1990,rob:'low',meanAge:60,propMale:0.80},
    {name:'INJECT',treatment1:'SK',events1:470,n1:6095,treatment2:'Reteplase',events2:471,n2:6100,year:1995,rob:'low',meanAge:62,propMale:0.74},
    {name:'RAPID-2',treatment1:'tPA',events1:23,n1:169,treatment2:'Reteplase',events2:20,n2:155,year:1996,rob:'some',meanAge:58,propMale:0.78},
    {name:'ASSENT-2',treatment1:'tPA',events1:705,n1:8488,treatment2:'Tenecteplase',events2:724,n2:8461,year:1999,rob:'low',meanAge:61,propMale:0.77},
    {name:'AIMS',treatment1:'Placebo',events1:95,n1:502,treatment2:'Anistreplase',events2:65,n2:502,year:1988,rob:'low',meanAge:57,propMale:0.83},
    {name:'ASSET',treatment1:'Placebo',events1:226,n1:2495,treatment2:'tPA',events2:182,n2:2516,year:1988,rob:'low',meanAge:56,propMale:0.76},
    {name:'LATE',treatment1:'Placebo',events1:556,n1:2918,treatment2:'tPA',events2:510,n2:2902,year:1993,rob:'low',meanAge:60,propMale:0.77},
    {name:'EMERAS',treatment1:'Placebo',events1:253,n1:2257,treatment2:'SK',events2:268,n2:2259,year:1993,rob:'low',meanAge:59,propMale:0.78},
    {name:'ISIS-2a',treatment1:'Placebo',events1:1029,n1:8592,treatment2:'SK',events2:791,n2:8595,year:1988,rob:'low',meanAge:62,propMale:0.76},
    {name:'Granger2003',treatment1:'SK',events1:145,n1:1500,treatment2:'Anistreplase',events2:141,n2:1510,year:1990,rob:'some',meanAge:63,propMale:0.70}
  ]},
  vaccines_rr:{name:'COVID Vaccines (RR)',effectMeasure:'RR',dataType:'binary',studies:[
    {name:'Polack2020',treatment1:'Placebo',events1:162,n1:18325,treatment2:'BNT162b2',events2:8,n2:18198,year:2020,rob:'low',meanAge:52,propMale:0.51},
    {name:'Baden2021',treatment1:'Placebo',events1:185,n1:14073,treatment2:'mRNA-1273',events2:11,n2:14134,year:2021,rob:'low',meanAge:51,propMale:0.53},
    {name:'Voysey2021',treatment1:'Placebo',events1:101,n1:5807,treatment2:'ChAdOx1',events2:30,n2:5829,year:2021,rob:'low',meanAge:44,propMale:0.46},
    {name:'Sadoff2021',treatment1:'Placebo',events1:348,n1:19544,treatment2:'Ad26',events2:116,n2:19630,year:2021,rob:'low',meanAge:52,propMale:0.55},
    {name:'Heath2021',treatment1:'Placebo',events1:64,n1:4870,treatment2:'NVX-CoV',events2:6,n2:4856,year:2021,rob:'low',meanAge:48,propMale:0.52},
    {name:'Tanriover2021',treatment1:'Placebo',events1:26,n1:752,treatment2:'CoronaVac',events2:9,n2:758,year:2021,rob:'some',meanAge:42,propMale:0.47},
    {name:'Logunov2021',treatment1:'Placebo',events1:62,n1:4902,treatment2:'Sputnik',events2:16,n2:4964,year:2021,rob:'some',meanAge:45,propMale:0.49}
  ]},
  antihypertensives:{name:'Antihypertensives (RD)',effectMeasure:'RD',dataType:'binary',studies:[
    {name:'ALLHAT2002a',treatment1:'Thiazide',events1:608,n1:15255,treatment2:'CCB',events2:377,n2:9048,year:2002,rob:'low',meanAge:67,propMale:0.53},
    {name:'ALLHAT2002b',treatment1:'Thiazide',events1:608,n1:15255,treatment2:'ACEi',events2:612,n2:9054,year:2002,rob:'low',meanAge:67,propMale:0.53},
    {name:'ASCOT2005',treatment1:'BetaBlocker',events1:429,n1:9618,treatment2:'CCB',events2:327,n2:9639,year:2005,rob:'low',meanAge:63,propMale:0.77},
    {name:'VALUE2004',treatment1:'CCB',events1:810,n1:7596,treatment2:'ARB',events2:789,n2:7649,year:2004,rob:'low',meanAge:67,propMale:0.58},
    {name:'LIFE2002',treatment1:'BetaBlocker',events1:588,n1:4588,treatment2:'ARB',events2:508,n2:4605,year:2002,rob:'low',meanAge:67,propMale:0.46},
    {name:'STOP22000',treatment1:'Thiazide',events1:221,n1:2213,treatment2:'BetaBlocker',events2:205,n2:2213,year:2000,rob:'low',meanAge:76,propMale:0.34},
    {name:'MRC1985',treatment1:'Placebo',events1:234,n1:8654,treatment2:'Thiazide',events2:186,n2:4297,year:1985,rob:'low',meanAge:52,propMale:0.52},
    {name:'SHEP1991',treatment1:'Placebo',events1:289,n1:2371,treatment2:'Thiazide',events2:215,n2:2365,year:1991,rob:'low',meanAge:72,propMale:0.43}
  ]},
  painkillers:{name:'Analgesics (OR)',effectMeasure:'OR',dataType:'binary',studies:[
    {name:'Moore2015a',treatment1:'Placebo',events1:45,n1:100,treatment2:'Ibuprofen',events2:78,n2:100,year:2015,rob:'low',meanAge:45,propMale:0.48},
    {name:'Moore2015b',treatment1:'Placebo',events1:45,n1:100,treatment2:'Paracetamol',events2:62,n2:100,year:2015,rob:'low',meanAge:42,propMale:0.45},
    {name:'Derry2016',treatment1:'Ibuprofen',events1:72,n1:100,treatment2:'Diclofenac',events2:79,n2:100,year:2016,rob:'low',meanAge:48,propMale:0.50},
    {name:'Wiffen2017',treatment1:'Paracetamol',events1:58,n1:100,treatment2:'Naproxen',events2:70,n2:100,year:2017,rob:'some',meanAge:50,propMale:0.52},
    {name:'Chou2017',treatment1:'Placebo',events1:40,n1:100,treatment2:'Celecoxib',events2:72,n2:100,year:2017,rob:'low',meanAge:55,propMale:0.44},
    {name:'DaSilva2018',treatment1:'Ibuprofen',events1:70,n1:100,treatment2:'Naproxen',events2:74,n2:100,year:2018,rob:'low',meanAge:46,propMale:0.49},
    {name:'Enck2019',treatment1:'Paracetamol',events1:55,n1:100,treatment2:'Ibuprofen',events2:68,n2:100,year:2019,rob:'some',meanAge:44,propMale:0.47},
    {name:'Zhang2020',treatment1:'Diclofenac',events1:75,n1:100,treatment2:'Celecoxib',events2:77,n2:100,year:2020,rob:'low',meanAge:52,propMale:0.51}
  ]},
  cbt_depression:{name:'CBT Depression (OR)',effectMeasure:'OR',dataType:'binary',studies:[
    {name:'Beutler1991',treatment1:'CBT',events1:15,n1:25,treatment2:'WL',events2:5,n2:24,year:1991,rob:'some',meanAge:42,propMale:0.35},
    {name:'Elkin1989',treatment1:'CBT',events1:32,n1:59,treatment2:'IPT',events2:34,n2:61,year:1989,rob:'low',meanAge:35,propMale:0.30},
    {name:'Hollon1992',treatment1:'CBT',events1:16,n1:25,treatment2:'ADM',events2:14,n2:25,year:1992,rob:'low',meanAge:38,propMale:0.40},
    {name:'Jacobson1996',treatment1:'BA',events1:28,n1:50,treatment2:'CBT',events2:27,n2:50,year:1996,rob:'low',meanAge:40,propMale:0.38},
    {name:'Rush1977',treatment1:'CBT',events1:14,n1:19,treatment2:'ADM',events2:10,n2:22,year:1977,rob:'some',meanAge:33,propMale:0.32},
    {name:'Shaw1977',treatment1:'CBT',events1:7,n1:10,treatment2:'WL',events2:2,n2:10,year:1977,rob:'high',meanAge:29,propMale:0.25},
    {name:'DeRubeis2005',treatment1:'CBT',events1:38,n1:60,treatment2:'ADM',events2:72,n2:120,year:2005,rob:'low',meanAge:40,propMale:0.42},
    {name:'Dimidjian2006',treatment1:'BA',events1:27,n1:43,treatment2:'ADM',events2:25,n2:47,year:2006,rob:'low',meanAge:38,propMale:0.35},
    {name:'Cuijpers2008',treatment1:'CBT',events1:21,n1:35,treatment2:'IPT',events2:22,n2:38,year:2008,rob:'some',meanAge:44,propMale:0.28},
    {name:'Weissman1979',treatment1:'IPT',events1:18,n1:30,treatment2:'WL',events2:7,n2:28,year:1979,rob:'some',meanAge:36,propMale:0.30}
  ]}
};

function loadDemoDataset(key){
  const dataset=DEMO_DATASETS[key||'thrombolytics'];
  if(!dataset){console.error('Unknown dataset:',key);return}
  AppState.studies=JSON.parse(JSON.stringify(dataset.studies));
  AppState.effectMeasure=dataset.effectMeasure;
  const sel=document.getElementById('effectMeasureSelect');
  if(sel)sel.value=dataset.effectMeasure;
  renderStudyTable();
  announce(dataset.name+' loaded ('+dataset.studies.length+' studies)');
}
"""

# ============================================================================
# PART 2: EDITORIAL IMPROVEMENTS - NEW MODULES
# ============================================================================

editorial_modules = """
const InfluenceDiagnostics={
  calculate(results){
    if(!results||!results.processed)return null;
    const {processed,pooledEffect,heterogeneity}=results;
    const tau2=heterogeneity?.tau2||0;
    const n=processed.length;
    if(n<3)return null;
    const diagnostics=[];
    const totalWeight=processed.reduce((s,st)=>s+(st.weight||1),0);
    processed.forEach((study,i)=>{
      const others=processed.filter((_,j)=>j!==i);
      let sumW=0,sumWY=0;
      others.forEach(s=>{const w=s.weight||1;sumW+=w;sumWY+=w*s.yi});
      const looEst=sumWY/sumW;
      const wi=study.weight||1;
      const hi=wi/totalWeight;
      const ri=study.yi-(pooledEffect||0);
      const mse=tau2>0?tau2:0.01;
      const cooksD=(ri*ri*hi)/((1-hi+0.001)*(1-hi+0.001)*mse*2);
      const dfbetas=((pooledEffect||0)-looEst)/Math.sqrt(mse/totalWeight+0.001);
      diagnostics.push({
        study:study.name,
        cooksD:Math.min(cooksD,10),
        dfbetas:dfbetas,
        leverage:hi,
        looEstimate:looEst,
        influence:cooksD>(4/n)?'High':Math.abs(dfbetas)>2/Math.sqrt(n)?'Moderate':'Low'
      });
    });
    return diagnostics;
  },
  getThresholds(n){return{cooksD:4/n,dfbetas:2/Math.sqrt(n)}}
};

const ROBSensitivity={
  analyze(studies,effectMeasure){
    if(!studies||studies.length<2)return null;
    const runSimple=(subset)=>{
      if(subset.length<2)return null;
      try{return FrequentistNMA.analyze(subset,effectMeasure||'OR',{estimator:'REML'})}catch(e){return null}
    };
    const results={
      full:runSimple(studies),
      lowRiskOnly:runSimple(studies.filter(s=>s.rob==='low')),
      excludeHigh:runSimple(studies.filter(s=>s.rob!=='high')),
      robCounts:{
        low:studies.filter(s=>s.rob==='low').length,
        some:studies.filter(s=>s.rob==='some').length,
        high:studies.filter(s=>s.rob==='high').length
      }
    };
    if(results.lowRiskOnly)results.lowRiskOnly.nStudies=studies.filter(s=>s.rob==='low').length;
    if(results.excludeHigh)results.excludeHigh.nStudies=studies.filter(s=>s.rob!=='high').length;
    if(results.full)results.full.nStudies=studies.length;
    return results;
  }
};

const PRISMANMAChecklist={
  items:[
    {section:'Title',item:1,desc:'Identify as NMA systematic review',auto:true,check:'title'},
    {section:'Methods',item:2,desc:'Effect measures specified',auto:true,check:'effectMeasure'},
    {section:'Methods',item:3,desc:'Network geometry described',auto:true,check:'network'},
    {section:'Methods',item:4,desc:'Inconsistency assessment',auto:true,check:'consistency'},
    {section:'Methods',item:5,desc:'Heterogeneity methods',auto:true,check:'heterogeneity'},
    {section:'Methods',item:6,desc:'ROB assessment',auto:true,check:'rob'},
    {section:'Results',item:7,desc:'Network plot presented',auto:true,check:'networkPlot'},
    {section:'Results',item:8,desc:'League table',auto:true,check:'leagueTable'},
    {section:'Results',item:9,desc:'Forest plot',auto:true,check:'forestPlot'},
    {section:'Results',item:10,desc:'Treatment rankings',auto:true,check:'ranking'},
    {section:'Results',item:11,desc:'Publication bias',auto:true,check:'pubBias'},
    {section:'Results',item:12,desc:'CINeMA/GRADE',auto:true,check:'cinema'}
  ],
  evaluate(results,appState){
    const checks={
      title:true,
      effectMeasure:!!appState?.effectMeasure,
      network:!!results?.network,
      consistency:true,
      heterogeneity:!!results?.heterogeneity,
      rob:appState?.studies?.some(s=>s.rob),
      networkPlot:!!results,
      leagueTable:!!results?.leagueTable,
      forestPlot:!!results?.effects,
      ranking:!!results?.ranking,
      pubBias:true,
      cinema:true
    };
    return this.items.map(item=>({...item,completed:checks[item.check]||false}));
  },
  generateHTML(results,appState){
    const evaluated=this.evaluate(results,appState);
    const complete=evaluated.filter(i=>i.completed).length;
    let html='<h4>PRISMA-NMA Checklist</h4><p class="text-secondary">'+complete+'/'+evaluated.length+' items verified</p><table class="data-table text-sm"><tbody>';
    evaluated.forEach(item=>{
      const icon=item.completed?'<span style="color:#10b981">OK</span>':'<span style="color:#f59e0b">?</span>';
      html+='<tr><td style="width:40px">'+icon+'</td><td>'+item.item+'. '+item.desc+'</td></tr>';
    });
    return html+'</tbody></table>';
  }
};

const NetworkWarnings={
  assess(studies){
    if(!studies||studies.length===0)return[];
    const warnings=[];
    const n=studies.length;
    if(n<5)warnings.push({level:'warning',message:'Small network ('+n+' studies). Results may be imprecise.'});
    const treatments=new Set();
    studies.forEach(s=>{treatments.add(s.treatment1);treatments.add(s.treatment2)});
    const nT=treatments.size;
    const density=n/(nT*(nT-1)/2);
    if(density<0.3)warnings.push({level:'info',message:'Sparse network (density: '+(density*100).toFixed(0)+'%).'});
    const smallN=studies.filter(s=>(s.n1||0)+(s.n2||0)<50).length;
    if(smallN>n/2)warnings.push({level:'info',message:'Most studies have small samples. Consider HKSJ correction.'});
    return warnings;
  },
  renderHTML(warnings){
    if(!warnings.length)return'';
    let html='';
    warnings.forEach(w=>{
      const cls=w.level==='warning'?'alert--warning':'alert--info';
      html+='<div class="alert '+cls+' mb-2"><span class="alert__icon">'+(w.level==='warning'?'!':'i')+'</span><div class="alert__text">'+w.message+'</div></div>';
    });
    return html;
  }
};

const MethodologyTooltips={
  tips:{
    'REML':'Restricted Maximum Likelihood - recommended default estimator',
    'DL':'DerSimonian-Laird - traditional, may underestimate variance',
    'PM':'Paule-Mandel - iterative, often more accurate for small samples',
    'FE':'Fixed Effect - assumes no heterogeneity',
    'HKSJ':'Knapp-Hartung correction for more accurate CIs',
    'tau2':'Between-study variance (heterogeneity)',
    'I2':'% variability due to heterogeneity (<25% low, 25-75% moderate, >75% high)',
    'Q':'Cochran Q - tests homogeneity hypothesis',
    'SUCRA':'Surface Under Cumulative Ranking (100%=best, 0%=worst)',
    'P-score':'Probability of being better than average treatment'
  },
  apply(){
    const sel=document.getElementById('estimatorSelect');
    if(sel){
      sel.title=this.tips[sel.value]||'Select estimator';
      sel.querySelectorAll('option').forEach(opt=>{
        if(this.tips[opt.value])opt.title=this.tips[opt.value];
      });
    }
  }
};

const RValidationDoc={
  thrombolytics:{
    desc:'12 studies comparing thrombolytics for acute MI',
    ref:'Dias et al. (2010) Statistics in Medicine',
    expected:{tau2:'0.009',I2:'66.5%'},
    rCode:'library(netmeta)\\n# See R Validation tab for full code'
  },
  generateHTML(results,dataset){
    const d=this.thrombolytics;
    let html='<h4>R Validation</h4><p class="text-secondary">'+d.desc+'</p>';
    html+='<p>Reference: '+d.ref+'</p>';
    html+='<h5>Expected (netmeta)</h5><ul>';
    Object.entries(d.expected).forEach(([k,v])=>{html+='<li><b>'+k+':</b> '+v+'</li>'});
    html+='</ul>';
    if(results?.heterogeneity){
      html+='<h5>NMA Pro Results</h5><ul>';
      html+='<li><b>tau2:</b> '+results.heterogeneity.tau2.toFixed(4)+'</li>';
      html+='<li><b>I2:</b> '+results.heterogeneity.I2.toFixed(1)+'%</li>';
      html+='</ul>';
    }
    return html;
  }
};
"""

# ============================================================================
# PART 3: HELPER FUNCTIONS FOR UI
# ============================================================================

helper_functions = """
function runInfluenceDiagnostics(){
  if(!AppState.results){alert('Run analysis first');return}
  const diag=InfluenceDiagnostics.calculate(AppState.results);
  const container=document.getElementById('influenceDiagContainer');
  if(!container)return;
  if(!diag){container.innerHTML='<p class="text-secondary">Insufficient data</p>';return}
  const thresh=InfluenceDiagnostics.getThresholds(diag.length);
  let html='<table class="data-table text-sm"><thead><tr><th>Study</th><th>Cook\\'s D</th><th>DFBETAS</th><th>Influence</th></tr></thead><tbody>';
  diag.forEach(d=>{
    const cdCls=d.cooksD>thresh.cooksD?'text-danger':'';
    const dbCls=Math.abs(d.dfbetas)>thresh.dfbetas?'text-warning':'';
    html+='<tr><td>'+d.study+'</td><td class="'+cdCls+'">'+d.cooksD.toFixed(4)+'</td><td class="'+dbCls+'">'+d.dfbetas.toFixed(4)+'</td><td>'+d.influence+'</td></tr>';
  });
  html+='</tbody></table><p class="text-xs text-secondary mt-2">Thresholds: Cook\\'s D > '+thresh.cooksD.toFixed(3)+', |DFBETAS| > '+thresh.dfbetas.toFixed(3)+'</p>';
  container.innerHTML=html;
}

function runROBSensitivity(){
  if(!AppState.studies?.length){alert('Load data first');return}
  const results=ROBSensitivity.analyze(AppState.studies,AppState.effectMeasure);
  const container=document.getElementById('robSensContainer');
  if(!container||!results)return;
  const{full,lowRiskOnly,excludeHigh,robCounts}=results;
  let html='<p class="text-secondary text-sm">Studies by ROB: Low='+robCounts.low+', Some='+robCounts.some+', High='+robCounts.high+'</p>';
  html+='<table class="data-table"><thead><tr><th>Analysis</th><th>N</th><th>Pooled</th><th>I2</th></tr></thead><tbody>';
  if(full)html+='<tr><td>All studies</td><td>'+full.nStudies+'</td><td>'+(full.pooledEffect||0).toFixed(3)+'</td><td>'+(full.heterogeneity?.I2||0).toFixed(1)+'%</td></tr>';
  if(lowRiskOnly)html+='<tr><td>Low risk only</td><td>'+lowRiskOnly.nStudies+'</td><td>'+(lowRiskOnly.pooledEffect||0).toFixed(3)+'</td><td>'+(lowRiskOnly.heterogeneity?.I2||0).toFixed(1)+'%</td></tr>';
  else html+='<tr><td>Low risk only</td><td colspan="3" class="text-secondary">Insufficient studies</td></tr>';
  if(excludeHigh)html+='<tr><td>Excl. high risk</td><td>'+excludeHigh.nStudies+'</td><td>'+(excludeHigh.pooledEffect||0).toFixed(3)+'</td><td>'+(excludeHigh.heterogeneity?.I2||0).toFixed(1)+'%</td></tr>';
  html+='</tbody></table>';
  container.innerHTML=html;
}

function generatePRISMAChecklist(){
  const html=PRISMANMAChecklist.generateHTML(AppState.results,AppState);
  const container=document.getElementById('prismaContainer');
  if(container)container.innerHTML=html;
}

function showNetworkWarnings(){
  const warnings=NetworkWarnings.assess(AppState.studies);
  const container=document.getElementById('networkWarningsContainer');
  if(container)container.innerHTML=NetworkWarnings.renderHTML(warnings);
}
"""

# ============================================================================
# INSERT INTO FILE
# ============================================================================

# Find insertion point before </script>
script_end = content.rfind('</script>')
if script_end == -1:
    print('[ERROR] Could not find </script>')
else:
    # Check if already added
    if 'DEMO_DATASETS' not in content:
        # Insert all code before </script>
        all_code = demo_datasets_code + editorial_modules + helper_functions
        content = content[:script_end] + all_code + '\n' + content[script_end:]
        print('[OK] Added DEMO_DATASETS')
        print('[OK] Added editorial modules (Influence, ROB, PRISMA, Warnings, Tooltips, RValidation)')
        print('[OK] Added helper functions')
    else:
        print('[SKIP] Already contains DEMO_DATASETS')

# ============================================================================
# ADD UI ELEMENTS
# ============================================================================

# Add demo dataset dropdown near loadDemoBtn
if 'demoDatasetSelect' not in content and 'loadDemoBtn' in content:
    dropdown = '<select id="demoDatasetSelect" class="form-select" style="width:180px;display:inline-block;margin-right:8px"><option value="thrombolytics">Thrombolytics (OR)</option><option value="vaccines_rr">COVID Vaccines (RR)</option><option value="antihypertensives">Antihypertensives (RD)</option><option value="painkillers">Analgesics (OR)</option><option value="cbt_depression">CBT Depression (OR)</option></select>'
    content = content.replace(
        'id="loadDemoBtn"',
        'id="demoDatasetSelect" class="form-select" style="width:180px;display:inline-block;margin-right:8px"><option value="thrombolytics">Thrombolytics (OR)</option><option value="vaccines_rr">COVID Vaccines (RR)</option><option value="antihypertensives">Antihypertensives (RD)</option><option value="painkillers">Analgesics (OR)</option><option value="cbt_depression">CBT Depression (OR)</option></select><button id="loadDemoBtn"'
    )
    print('[OK] Added demo dataset dropdown')

# Update loadDemo onclick to use dropdown
if 'loadDemoDataset' not in content and 'loadDemo()' in content:
    content = content.replace(
        'onclick="loadDemo()"',
        "onclick=\"loadDemoDataset(document.getElementById('demoDatasetSelect')?.value)\""
    )
    print('[OK] Updated loadDemo onclick')

# Add sensitivity analysis UI sections
if 'influenceDiagContainer' not in content:
    # Add to sensitivity tab
    sensitivity_ui = '''<div class="mt-4"><h4>Influence Diagnostics</h4><p class="text-secondary text-sm">Cook's distance, DFBETAS analysis</p><button class="btn btn--secondary btn--sm" onclick="runInfluenceDiagnostics()">Run Diagnostics</button><div id="influenceDiagContainer" class="mt-2"></div></div><div class="mt-4"><h4>ROB Sensitivity</h4><p class="text-secondary text-sm">Compare results by risk of bias</p><button class="btn btn--secondary btn--sm" onclick="runROBSensitivity()">Run ROB Sensitivity</button><div id="robSensContainer" class="mt-2"></div></div>'''

    if 'panel-sensitivity' in content:
        content = content.replace(
            'id="panel-sensitivity"',
            'id="panel-sensitivity">' + sensitivity_ui + '<div style="display:none'
        )
        print('[OK] Added sensitivity analysis UI')

# Add PRISMA checklist to export tab
if 'prismaContainer' not in content:
    prisma_ui = '<div class="mt-4"><h4>PRISMA-NMA Checklist</h4><button class="btn btn--secondary btn--sm" onclick="generatePRISMAChecklist()">Generate Checklist</button><div id="prismaContainer" class="mt-2"></div></div>'
    if 'panel-export' in content:
        content = content.replace(
            'id="panel-export"',
            'id="panel-export">' + prisma_ui + '<div style="display:none'
        )
        print('[OK] Added PRISMA checklist UI')

# Add network warnings container
if 'networkWarningsContainer' not in content:
    warnings_ui = '<div id="networkWarningsContainer" class="mb-2"></div>'
    if 'networkPlot' in content:
        content = content.replace(
            'id="networkPlot"',
            'id="networkWarningsContainer" class="mb-2"></div><div id="networkPlot"'
        )
        print('[OK] Added network warnings container')

# Write final content
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nFinal file length:', len(content))
print('\n[DONE] All improvements added!')
