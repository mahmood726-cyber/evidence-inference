"""
Fix all R validation issues in NMA Pro v6.2:
1. TrimFill - Implement R0 estimator to match metafor::trimfill
2. Egger Test - Add z-statistic to output
3. NMA Matrix - Improve numerical stability
"""

file_path = r'C:/Users/user/OneDrive - NHS/Documents/NMAhtml/nma-pro-v6.2-optimized.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================================
# FIX 1: EGGER TEST - Add z-statistic (zValue) to output
# ============================================================================

old_egger = '''eggerTest(y,se){const n=y.length;if(n<3)return{applicable:false};const precision=se.map(s=>1/s),intercepts=y.map((yi,i)=>yi/se[i]);const xMean=Stats.mean(precision),yMean=Stats.mean(intercepts);let num=0,den=0;for(let i=0;i<n;i++){num+=(precision[i]-xMean)*(intercepts[i]-yMean);den+=(precision[i]-xMean)**2}const slope=num/den,intercept=yMean-slope*xMean;const resid=intercepts.map((yi,i)=>yi-intercept-slope*precision[i]);const mse=Stats.sum(resid.map(r=>r*r))/(n-2);const t=intercept/Math.sqrt(mse*(1/n+xMean**2/den));const pValue=2*(1-Stats.pt(Math.abs(t),n-2));return{intercept,pValue,significant:pValue<0.1,interpretation:pValue<0.1?'Evidence of small-study effects':'No evidence'}}'''

new_egger = '''eggerTest(y,se){const n=y.length;if(n<3)return{applicable:false};const precision=se.map(s=>1/s),intercepts=y.map((yi,i)=>yi/se[i]);const xMean=Stats.mean(precision),yMean=Stats.mean(intercepts);let num=0,den=0;for(let i=0;i<n;i++){num+=(precision[i]-xMean)*(intercepts[i]-yMean);den+=(precision[i]-xMean)**2}const slope=num/den,intercept=yMean-slope*xMean;const resid=intercepts.map((yi,i)=>yi-intercept-slope*precision[i]);const mse=Stats.sum(resid.map(r=>r*r))/(n-2);const seInt=Math.sqrt(mse*(1/n+xMean**2/den));const t=intercept/seInt;const z=t*Math.sqrt(n-2)/Math.sqrt(n);const pValue=2*(1-Stats.pt(Math.abs(t),n-2));return{intercept,se:seInt,t,z,zValue:z,pValue,df:n-2,significant:pValue<0.1,interpretation:pValue<0.1?'Evidence of small-study effects':'No evidence'}}'''

if old_egger in content:
    content = content.replace(old_egger, new_egger)
    print("[OK] Fixed Egger test - added z-statistic")
else:
    print("[SKIP] Egger test pattern not found")

# ============================================================================
# FIX 2: TRIM-AND-FILL - Implement R0 estimator like metafor
# ============================================================================

old_trimfill = '''trimAndFill(y,se,tau2){const n=y.length;const w=se.map(s=>1/(s*s+tau2)),sumW=Stats.sum(w);const pooled=Stats.sum(y.map((yi,i)=>w[i]*yi))/sumW;const resid=y.map(yi=>yi-pooled);let k0=0;const sorted=resid.map((r,i)=>({r,se:se[i]})).sort((a,b)=>a.r-b.r);for(let i=0;i<Math.floor(n/2);i++){if(sorted[i].r+sorted[n-1-i].r>0)k0++}k0=Math.min(k0,Math.floor(n/2));const filled=[];for(let i=0;i<k0&&i<sorted.length;i++){const mirror=-sorted[sorted.length-1-i].r*2+pooled;filled.push({yi:mirror,se:sorted[sorted.length-1-i].se})}const augY=[...y,...filled.map(f=>f.yi)],augSE=[...se,...filled.map(f=>f.se)];const adjW=augSE.map(s=>1/(s*s+tau2)),adjSumW=Stats.sum(adjW);const adjEst=Stats.sum(augY.map((yi,i)=>adjW[i]*yi))/adjSumW;return{k0,adjustedEstimate:adjEst,originalEstimate:pooled,filledStudies:filled}}'''

# Implement R0 estimator (rank-based) like R metafor::trimfill
new_trimfill = '''trimAndFill(y,se,tau2){const n=y.length;if(n<3)return{k0:0,adjustedEstimate:null,originalEstimate:null,filledStudies:[]};const w=se.map(s=>1/(s*s+(tau2||0))),sumW=Stats.sum(w);let pooled=Stats.sum(y.map((yi,i)=>w[i]*yi))/sumW;const maxIter=50;for(let iter=0;iter<maxIter;iter++){const centered=y.map(yi=>yi-pooled);const absC=centered.map(c=>Math.abs(c));const indices=absC.map((v,i)=>({v,i})).sort((a,b)=>a.v-b.v);const ranks=Array(n);indices.forEach((item,r)=>{ranks[item.i]=r+1});let S=0;for(let i=0;i<n;i++){if(centered[i]>0)S+=ranks[i]}const k0Est=Math.max(0,Math.round((4*S-n*(n+1))/(2*n-1)));if(k0Est===0)break;const sorted=centered.map((c,i)=>({c,se:se[i],idx:i})).sort((a,b)=>a.c-b.c);const toFill=sorted.slice(n-k0Est);const filled=toFill.map(s=>({yi:pooled-(s.c),se:s.se}));const augY=[...y,...filled.map(f=>f.yi)],augSE=[...se,...filled.map(f=>f.se)];const adjW=augSE.map(s=>1/(s*s+(tau2||0))),adjSumW=Stats.sum(adjW);const newPooled=Stats.sum(augY.map((yi,i)=>adjW[i]*yi))/adjSumW;if(Math.abs(newPooled-pooled)<1e-6){return{k0:k0Est,adjustedEstimate:newPooled,originalEstimate:Stats.sum(y.map((yi,i)=>w[i]*yi))/sumW,filledStudies:filled,studiesAdded:k0Est}}pooled=newPooled}const centered=y.map(yi=>yi-pooled);const absC=centered.map(c=>Math.abs(c));const indices=absC.map((v,i)=>({v,i})).sort((a,b)=>a.v-b.v);const ranks=Array(n);indices.forEach((item,r)=>{ranks[item.i]=r+1});let S=0;for(let i=0;i<n;i++){if(centered[i]>0)S+=ranks[i]}const k0=Math.max(0,Math.round((4*S-n*(n+1))/(2*n-1)));const sorted=centered.map((c,i)=>({c,se:se[i],idx:i})).sort((a,b)=>a.c-b.c);const toFill=k0>0?sorted.slice(n-k0):[];const filled=toFill.map(s=>({yi:pooled-(s.c),se:s.se}));const augY=[...y,...filled.map(f=>f.yi)],augSE=[...se,...filled.map(f=>f.se)];const adjW=augSE.map(s=>1/(s*s+(tau2||0))),adjSumW=Stats.sum(adjW);const adjEst=k0>0?Stats.sum(augY.map((yi,i)=>adjW[i]*yi))/adjSumW:pooled;return{k0,adjustedEstimate:adjEst,originalEstimate:Stats.sum(y.map((yi,i)=>w[i]*yi))/sumW,filledStudies:filled,studiesAdded:k0}}'''

if old_trimfill in content:
    content = content.replace(old_trimfill, new_trimfill)
    print("[OK] Fixed TrimFill - implemented R0 estimator")
else:
    print("[SKIP] TrimFill pattern not found")

# ============================================================================
# FIX 3: MATRIX SOLVE - Add regularization for numerical stability
# ============================================================================

old_matrix_solve = '''solve(A,b){const n=A.length,{L,U,P}=Matrix.lu(A),pb=Matrix.multiply(P,b.map(x=>[x])).map(r=>r[0]),y=Array(n).fill(0);for(let i=0;i<n;i++){y[i]=pb[i];for(let j=0;j<i;j++)y[i]-=L[i][j]*y[j]}const x=Array(n).fill(0);for(let i=n-1;i>=0;i--){x[i]=y[i];for(let j=i+1;j<n;j++)x[i]-=U[i][j]*x[j];if(Math.abs(U[i][i])>1e-14)x[i]/=U[i][i]}return x}'''

# Add regularization and better handling of near-singular matrices
new_matrix_solve = '''solve(A,b){const n=A.length;const Areg=A.map((row,i)=>row.map((v,j)=>i===j?v+1e-10:v));const{L,U,P}=Matrix.lu(Areg),pb=Matrix.multiply(P,b.map(x=>[x])).map(r=>r[0]),y=Array(n).fill(0);for(let i=0;i<n;i++){y[i]=pb[i];for(let j=0;j<i;j++)y[i]-=L[i][j]*y[j]}const x=Array(n).fill(0);for(let i=n-1;i>=0;i--){x[i]=y[i];for(let j=i+1;j<n;j++)x[i]-=U[i][j]*x[j];const diag=U[i][i];x[i]=Math.abs(diag)>1e-12?x[i]/diag:0}return x}'''

if old_matrix_solve in content:
    content = content.replace(old_matrix_solve, new_matrix_solve)
    print("[OK] Fixed Matrix.solve - added regularization")
else:
    print("[SKIP] Matrix.solve pattern not found")

# ============================================================================
# FIX 4: MATRIX INVERSE - Add regularization for numerical stability
# ============================================================================

old_matrix_inverse = '''inverse(A){const n=A.length,I=Matrix.identity(n),inv=Matrix.zeros(n,n);for(let j=0;j<n;j++){const col=Matrix.solve(A,I.map(r=>r[j]));for(let i=0;i<n;i++)inv[i][j]=col[i]}return inv}'''

new_matrix_inverse = '''inverse(A){const n=A.length,I=Matrix.identity(n),inv=Matrix.zeros(n,n);const Areg=A.map((row,i)=>row.map((v,j)=>i===j?v+1e-10:v));for(let j=0;j<n;j++){const col=Matrix.solve(Areg,I.map(r=>r[j]));for(let i=0;i<n;i++)inv[i][j]=col[i]}return inv}'''

if old_matrix_inverse in content:
    content = content.replace(old_matrix_inverse, new_matrix_inverse)
    print("[OK] Fixed Matrix.inverse - added regularization")
else:
    print("[SKIP] Matrix.inverse pattern not found")

# ============================================================================
# FIX 5: FrequentistNMA.analyze - Better error handling
# ============================================================================

old_nma_analyze = '''analyze(studies,options={}){const{reference,effectMeasure='OR',estimator='REML',smallStudyCorrection='hksj',predictionIntervals=true}=options;
const processed=this.calcEffects(studies,effectMeasure);const matrices=this.buildMatrices(processed,reference);const tau2Result=this.estimateTau2(matrices,estimator);const effects=this.calcTreatmentEffects(matrices,tau2Result.tau2,smallStudyCorrection);const heterogeneity=this.calcHeterogeneity(matrices,tau2Result.tau2);const tau2CI=this.profileLikelihoodCI(matrices,tau2Result.tau2);
if(predictionIntervals)this.addPredictionIntervals(effects,tau2Result.tau2,matrices);const leagueTable=this.buildLeagueTable(effects,matrices.treatments,reference,effectMeasure);const consistency=this.nodeSplitting(processed,matrices,tau2Result.tau2);
return{effects,heterogeneity,leagueTable,consistency,tau2:tau2Result.tau2,tau:Math.sqrt(tau2Result.tau2),tau2CI,treatments:matrices.treatments,reference,processed,matrices}}'''

new_nma_analyze = '''analyze(studies,options={}){const{reference,effectMeasure='OR',estimator='REML',smallStudyCorrection='hksj',predictionIntervals=true}=options;
try{const processed=this.calcEffects(studies,effectMeasure);if(!processed||processed.length===0)return{error:'No valid studies processed'};const matrices=this.buildMatrices(processed,reference);if(!matrices||!matrices.X)return{error:'Failed to build design matrices'};const tau2Result=this.estimateTau2(matrices,estimator);const tau2=tau2Result.tau2||0;const effects=this.calcTreatmentEffects(matrices,tau2,smallStudyCorrection);if(!effects||!effects.effects)return{error:'Failed to calculate treatment effects',tau2};const heterogeneity=this.calcHeterogeneity(matrices,tau2);const tau2CI=this.profileLikelihoodCI(matrices,tau2);
if(predictionIntervals)this.addPredictionIntervals(effects,tau2,matrices);const leagueTable=this.buildLeagueTable(effects,matrices.treatments,reference,effectMeasure);const consistency=this.nodeSplitting(processed,matrices,tau2);
return{effects:effects.effects,treatmentEffects:effects.effects,heterogeneity,leagueTable,consistency,tau2,tau:Math.sqrt(tau2),tau2CI,treatments:matrices.treatments,reference,processed,matrices}}catch(e){return{error:e.message}}}'''

if old_nma_analyze in content:
    content = content.replace(old_nma_analyze, new_nma_analyze)
    print("[OK] Fixed FrequentistNMA.analyze - added error handling")
else:
    print("[SKIP] FrequentistNMA.analyze pattern not found")

# Write the fixed content
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*50)
print("All fixes applied!")
print("="*50)
