"""Add editorial improvements to NMA Pro v6.2"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f'Original file size: {len(content)} bytes')

# 1. Add DEMO_DATASETS if not present
if 'const DEMO_DATASETS=' not in content:
    demo_datasets = '''
const DEMO_DATASETS={
thrombolytics:{name:"Thrombolytics (OR)",effectMeasure:"OR",reference:"SK",studies:[
{id:"Coll1988",treat1:"SK",treat2:"tPA",events1:8,n1:54,events2:4,n2:56},
{id:"Coll1988b",treat1:"SK",treat2:"ASPAC",events1:8,n1:54,events2:5,n2:52},
{id:"ISIS2",treat1:"SK",treat2:"Placebo",events1:791,n1:8592,events2:1029,n2:8595},
{id:"GISSI",treat1:"SK",treat2:"Placebo",events1:628,n1:5860,events2:758,n2:5852},
{id:"ISAM",treat1:"SK",treat2:"Placebo",events1:27,n1:859,events2:41,n2:882},
{id:"ASSET",treat1:"tPA",treat2:"Placebo",events1:182,n1:2516,events2:227,n2:2495},
{id:"AIMS",treat1:"ASPAC",treat2:"Placebo",events1:32,n1:502,events2:65,n2:502},
{id:"EMERAS",treat1:"SK",treat2:"Placebo",events1:94,n1:1169,events2:117,n2:1182},
{id:"LATE",treat1:"tPA",treat2:"Placebo",events1:284,n1:2838,events2:323,n2:2895},
{id:"GISSI2",treat1:"SK",treat2:"tPA",events1:887,n1:10396,events2:880,n2:10372},
{id:"ISIS3",treat1:"SK",treat2:"tPA",events1:2841,n1:13780,events2:2878,n2:13746},
{id:"GUSTO",treat1:"SK",treat2:"tPA",events1:1473,n1:20173,events2:1248,n2:10344}
]},
vaccines_rr:{name:"Vaccines (RR)",effectMeasure:"RR",reference:"Placebo",studies:[
{id:"Trial1",treat1:"VaccineA",treat2:"Placebo",events1:15,n1:1000,events2:50,n2:1000},
{id:"Trial2",treat1:"VaccineB",treat2:"Placebo",events1:20,n1:800,events2:45,n2:810},
{id:"Trial3",treat1:"VaccineA",treat2:"VaccineB",events1:18,n1:600,events2:22,n2:590},
{id:"Trial4",treat1:"VaccineA",treat2:"Placebo",events1:12,n1:500,events2:35,n2:500},
{id:"Trial5",treat1:"VaccineB",treat2:"Placebo",events1:25,n1:900,events2:55,n2:880}
]},
antihypertensives:{name:"Antihypertensives (OR)",effectMeasure:"OR",reference:"Placebo",studies:[
{id:"ALLHAT1",treat1:"Diuretic",treat2:"Placebo",events1:450,n1:5000,events2:520,n2:5000},
{id:"ALLHAT2",treat1:"ACEi",treat2:"Placebo",events1:430,n1:4800,events2:500,n2:4750},
{id:"ALLHAT3",treat1:"CCB",treat2:"Placebo",events1:440,n1:4900,events2:510,n2:4850},
{id:"VALUE1",treat1:"Diuretic",treat2:"ACEi",events1:350,n1:4000,events2:360,n2:4050},
{id:"VALUE2",treat1:"ACEi",treat2:"CCB",events1:280,n1:3500,events2:300,n2:3600},
{id:"INVEST",treat1:"CCB",treat2:"Diuretic",events1:200,n1:2500,events2:220,n2:2600}
]},
painkillers:{name:"Pain Relief (OR)",effectMeasure:"OR",reference:"Placebo",studies:[
{id:"Analg1",treat1:"DrugA",treat2:"Placebo",events1:80,n1:200,events2:40,n2:200},
{id:"Analg2",treat1:"DrugB",treat2:"Placebo",events1:90,n1:220,events2:45,n2:210},
{id:"Analg3",treat1:"DrugC",treat2:"Placebo",events1:75,n1:190,events2:38,n2:185},
{id:"Analg4",treat1:"DrugA",treat2:"DrugB",events1:85,n1:210,events2:88,n2:215},
{id:"Analg5",treat1:"DrugB",treat2:"DrugC",events1:92,n1:230,events2:78,n2:200}
]},
cbt_depression:{name:"CBT vs Medications (SMD)",effectMeasure:"SMD",reference:"WaitList",studies:[
{id:"CBT1",treat1:"CBT",treat2:"WaitList",mean1:-1.2,sd1:0.8,n1:50,mean2:-0.3,sd2:0.9,n2:48},
{id:"CBT2",treat1:"SSRI",treat2:"WaitList",mean1:-1.1,sd1:0.7,n1:60,mean2:-0.2,sd2:0.8,n2:55},
{id:"CBT3",treat1:"CBT",treat2:"SSRI",mean1:-1.3,sd1:0.9,n1:45,mean2:-1.2,sd2:0.8,n2:50},
{id:"CBT4",treat1:"Combined",treat2:"WaitList",mean1:-1.5,sd1:0.7,n1:40,mean2:-0.25,sd2:0.85,n2:42},
{id:"CBT5",treat1:"Combined",treat2:"CBT",mean1:-1.4,sd1:0.75,n1:55,mean2:-1.25,sd2:0.85,n2:52}
]}
};
function loadDemoDataset(name){const d=DEMO_DATASETS[name];if(!d)return;AppState.studies=d.studies.map((s,i)=>({...s,id:s.id||'Study'+(i+1)}));AppState.effectMeasure=d.effectMeasure;AppState.reference=d.reference;if(typeof updateStudyTable==='function')updateStudyTable();if(typeof updateNetworkGraph==='function')updateNetworkGraph();}
'''
    # Insert after AppState
    appstate_end = content.find('const AppState=')
    if appstate_end >= 0:
        # Find the end of AppState definition
        brace_count = 0
        i = content.find('{', appstate_end)
        while i < len(content):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    break
            i += 1
        insert_pos = content.find(';', i) + 1
        content = content[:insert_pos] + '\n' + demo_datasets + content[insert_pos:]
        print('Added DEMO_DATASETS')

# 2. Add editorial modules before closing </script>
editorial_modules = '''
const InfluenceDiagnostics={calculate(results){if(!results||!results.processed)return null;const{processed,pooledEffect,heterogeneity}=results;const tau2=heterogeneity?.tau2||0;const n=processed.length;if(n<3)return null;const diagnostics=[];const weights=processed.map(s=>1/(s.variance+(tau2||0)));const W=weights.reduce((a,b)=>a+b,0);for(let i=0;i<n;i++){const wi=weights[i];const hi=wi/W;const ei=processed[i].effect-pooledEffect.effect;const vi=processed[i].variance;const cooksD=ei*ei*hi/((1-hi)*vi);const dfbetas=ei*Math.sqrt(wi)/(1-hi);diagnostics.push({study:processed[i].study||processed[i].id,effect:processed[i].effect,weight:wi,leverage:hi,residual:ei,cooksD:cooksD,dfbetas:dfbetas,influence:cooksD>4/n?'high':cooksD>1/n?'moderate':'low'});}return diagnostics;},getThresholds(n){return{cooksD:4/n,dfbetas:2/Math.sqrt(n)};}};
const ROBSensitivity={analyze(studies,effectMeasure){if(!studies||studies.length<3)return null;const fullResult=typeof FrequentistNMA!=='undefined'?FrequentistNMA.analyze(studies,{effectMeasure}):null;const lowRisk=studies.filter(s=>s.rob==='low'||!s.rob);const lowResult=lowRisk.length>=3&&typeof FrequentistNMA!=='undefined'?FrequentistNMA.analyze(lowRisk,{effectMeasure}):null;const excludeHigh=studies.filter(s=>s.rob!=='high');const excludeResult=excludeHigh.length>=3&&typeof FrequentistNMA!=='undefined'?FrequentistNMA.analyze(excludeHigh,{effectMeasure}):null;const robCounts={low:studies.filter(s=>s.rob==='low').length,unclear:studies.filter(s=>s.rob==='unclear'||!s.rob).length,high:studies.filter(s=>s.rob==='high').length};return{full:fullResult,lowRiskOnly:lowResult,excludeHighRisk:excludeResult,robCounts,sensitivity:fullResult&&excludeResult?Math.abs(fullResult.pooledEffect.effect-excludeResult.pooledEffect.effect):null};}};
const PRISMANMAChecklist={items:[{id:'1',section:'Title',item:'Identify the report as a systematic review incorporating NMA',status:'auto'},{id:'2',section:'Abstract',item:'Structured summary including NMA-specific elements',status:'manual'},{id:'3',section:'Rationale',item:'Describe rationale for NMA over pairwise MA',status:'manual'},{id:'4',section:'Objectives',item:'State research question using PICOS for multiple interventions',status:'manual'},{id:'5',section:'Protocol',item:'Registration information',status:'manual'},{id:'6',section:'Eligibility',item:'Specify inclusion criteria considering network geometry',status:'manual'},{id:'7',section:'Search',item:'Full electronic search strategy',status:'manual'},{id:'8',section:'Selection',item:'Study selection process',status:'manual'},{id:'9',section:'Data',item:'Data extraction including treatment comparisons',status:'manual'},{id:'10',section:'ROB',item:'Risk of bias assessment per study',status:'auto'},{id:'11',section:'Effect',item:'Effect measures with justification',status:'auto'},{id:'12',section:'Synthesis',item:'NMA methods and software',status:'auto'},{id:'13',section:'Heterogeneity',item:'Assessment of statistical heterogeneity',status:'auto'},{id:'14',section:'Inconsistency',item:'Assessment of network inconsistency',status:'auto'},{id:'15',section:'ROB-evidence',item:'Certainty assessment using CINeMA/GRADE',status:'auto'},{id:'16',section:'Results-search',item:'Search and selection results',status:'manual'},{id:'17',section:'Results-ROB',item:'ROB within studies',status:'auto'},{id:'18',section:'Results-NMA',item:'Network geometry and characteristics',status:'auto'},{id:'19',section:'Results-effects',item:'All pairwise effect estimates',status:'auto'},{id:'20',section:'Results-ranking',item:'Treatment ranking with uncertainty',status:'auto'},{id:'21',section:'Results-inconsistency',item:'Inconsistency assessment results',status:'auto'},{id:'22',section:'Discussion',item:'Summary of evidence and implications',status:'manual'},{id:'23',section:'Funding',item:'Funding source',status:'manual'}],generateHTML(results,appState){let html='<h3>PRISMA-NMA Checklist</h3><table class="prisma-table"><tr><th>Item</th><th>Section</th><th>Description</th><th>Status</th></tr>';this.items.forEach(item=>{const status=this.checkItem(item,results,appState);html+=`<tr><td>${item.id}</td><td>${item.section}</td><td>${item.item}</td><td class="${status}">${status}</td></tr>`;});html+='</table>';return html;},checkItem(item,results,appState){if(item.status==='manual')return'Review needed';if(results){if(item.id==='10'&&appState?.studies?.some(s=>s.rob))return'Reported';if(item.id==='11')return'Reported';if(item.id==='12')return'Reported';if(item.id==='13'&&results.heterogeneity)return'Reported';if(item.id==='14')return results.inconsistency?'Reported':'Not assessed';if(item.id==='17'&&appState?.studies?.some(s=>s.rob))return'Reported';if(item.id==='18')return'Reported';if(item.id==='19')return'Reported';if(item.id==='20'&&results.rankings)return'Reported';if(item.id==='21')return results.inconsistency?'Reported':'Not assessed';}return'Check';}};
const NetworkWarnings={assess(studies){const warnings=[];if(!studies||studies.length<3){warnings.push({level:'error',message:'Insufficient studies for NMA (minimum 3 required)'});return warnings;}const treatments=new Set();studies.forEach(s=>{treatments.add(s.treat1);treatments.add(s.treat2);});const k=treatments.size;const m=studies.length;const minStudies=k-1;if(m<minStudies){warnings.push({level:'error',message:`Network requires at least ${minStudies} studies for ${k} treatments`});}const tCounts={};studies.forEach(s=>{tCounts[s.treat1]=(tCounts[s.treat1]||0)+1;tCounts[s.treat2]=(tCounts[s.treat2]||0)+1;});const singleArm=Object.entries(tCounts).filter(([t,c])=>c===1);if(singleArm.length>0){warnings.push({level:'warning',message:`Treatments with only 1 study: ${singleArm.map(([t])=>t).join(', ')}`});}const compCounts={};studies.forEach(s=>{const key=[s.treat1,s.treat2].sort().join('-');compCounts[key]=(compCounts[key]||0)+1;});const singleComp=Object.entries(compCounts).filter(([c,n])=>n===1);if(singleComp.length>k-1){warnings.push({level:'info',message:`${singleComp.length} comparisons informed by single studies only`});}if(studies.length<10){warnings.push({level:'info',message:'Small network - interpret heterogeneity estimates with caution'});}return warnings;}};
const MethodologyTooltips={tips:{REML:'Restricted Maximum Likelihood - recommended for most NMA analyses, provides unbiased tau-squared estimates',DL:'DerSimonian-Laird - simple moment-based estimator, may underestimate heterogeneity',PM:'Paule-Mandel - iterative estimator that performs well with few studies',HKSJ:'Hartung-Knapp-Sidik-Jonkman - adjusts confidence intervals for uncertainty in tau-squared estimation, recommended',OR:'Odds Ratio - ratio of odds between treatment and control, symmetric on log scale',RR:'Risk Ratio - ratio of event probabilities, more intuitive but asymmetric',RD:'Risk Difference - absolute difference in event probabilities',tau2:'Between-study variance - measures heterogeneity beyond sampling error',I2:'Proportion of variance due to heterogeneity - 25% low, 50% moderate, 75% high',SUCRA:'Surface Under Cumulative Ranking - probability of being best treatment (0-100%)'},get(key){return this.tips[key]||'No description available';},render(element,key){const tip=this.get(key);if(element){element.title=tip;element.classList.add('has-tooltip');}}};
const RValidationDoc={generateHTML(results,datasetName){if(!results)return'<p>Run analysis first</p>';let html='<h3>R Validation Script</h3><pre>';html+='# NMA Pro validation against R netmeta package\\n';html+='library(netmeta)\\n\\n';html+=`# Dataset: ${datasetName||'custom'}\\n`;html+='# Effect measure: '+((results.effectMeasure||'OR'))+'\\n\\n';html+='# To validate:\\n';html+='# 1. Load your data into R\\n';html+='# 2. Run: net <- netmeta(TE, seTE, treat1, treat2, studlab, data=mydata)\\n';html+='# 3. Compare pooled estimates and heterogeneity statistics\\n\\n';if(results.pooledEffect){html+=`# NMA Pro pooled effect: ${results.pooledEffect.effect.toFixed(4)}\\n`;html+=`# NMA Pro 95% CI: [${results.pooledEffect.ciLower.toFixed(4)}, ${results.pooledEffect.ciUpper.toFixed(4)}]\\n`;}if(results.heterogeneity){html+=`# NMA Pro tau2: ${results.heterogeneity.tau2?.toFixed(4)||'NA'}\\n`;html+=`# NMA Pro I2: ${results.heterogeneity.I2?.toFixed(1)||'NA'}%\\n`;}html+='</pre>';return html;}};
'''

# Insert before final </script>
script_end = content.rfind('</script>')
if script_end >= 0:
    if 'const InfluenceDiagnostics=' not in content:
        content = content[:script_end] + editorial_modules + '\n' + content[script_end:]
        print('Added editorial modules')
    else:
        print('Editorial modules already present')

# 3. Add UI elements for demo dataset selection in HTML
if 'demoDatasetSelect' not in content:
    # Find the data input section
    data_input = content.find('id="dataInput"')
    if data_input >= 0:
        # Find the next suitable place to add dropdown
        form_start = content.find('<div', data_input)
        if form_start >= 0:
            dropdown_html = '''
<div class="demo-selector" style="margin-bottom:15px;padding:10px;background:#f8f9fa;border-radius:5px;">
<label style="font-weight:bold;">Load Demo Dataset: </label>
<select id="demoDatasetSelect" onchange="if(this.value)loadDemoDataset(this.value)" style="padding:5px;margin-left:10px;">
<option value="">-- Select Dataset --</option>
<option value="thrombolytics">Thrombolytics (OR, 12 studies)</option>
<option value="vaccines_rr">Vaccines (RR, 5 studies)</option>
<option value="antihypertensives">Antihypertensives (OR, 6 studies)</option>
<option value="painkillers">Pain Relief (OR, 5 studies)</option>
<option value="cbt_depression">CBT vs Meds (SMD, 5 studies)</option>
</select>
</div>'''
            # Insert at beginning of dataInput div content
            div_content_start = content.find('>', data_input) + 1
            content = content[:div_content_start] + dropdown_html + content[div_content_start:]
            print('Added demo dataset dropdown')

# Save file
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Final file size: {len(content)} bytes')
print('Done!')
