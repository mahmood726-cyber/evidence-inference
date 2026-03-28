"""Check exposed functions in TruthCert-PairwisePro"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
driver.get('file:///C:/Truthcert1/TruthCert-PairwisePro-v1.0-fast.html')
time.sleep(3)

# Important functions to check
important_functions = [
    # Core analysis
    'runAnalysis', 'runFullAnalysis', 'calculatePooledEstimate', 'estimateTau2',
    'calculateHeterogeneity', 'calculateHKSJ',
    # Effect sizes
    'calculateLogOR', 'calculateLogRR', 'calculateRD', 'calculateSMD', 'calculateMD',
    # Bias tests
    'eggerTest', 'beggTest', 'trimAndFill', 'failsafeN', 'petPeese',
    'petersTest', 'harbordTest', 'copasSelectionModel', 'testExcessSignificance',
    # Fixed effects
    'mantelHaenszel', 'petoMethod',
    # Influence
    'cookDistance', 'leaveOneOut', 'baujatPlotData',
    # Advanced
    'metaRegression', 'subgroupAnalysis', 'cumulativeMetaAnalysis',
    'threeLevelMA', 'threeLevel_MetaAnalysis', 'bayesianMetaAnalysis', 'fragilityIndex',
    # Gap closure
    'glmmMetaAnalysis', 'betaBinomialMA', 'networkMAConsistency',
    'sideSplittingTest', 'netHeatPlotData', 'profileLikelihood', 'likelihoodRatioTest',
    # Innovative
    'robmaModelAveraging', 'multiverseMetaAnalysis', 'improvedPredictionInterval',
    'sequentialMetaAnalysis', 'pUniformStar', 'valueOfInformation',
    'albatrossPlotData', 'sunsetPlotData', 'draperyPlotData', 'harvestPlotData',
    'decisionCurveAnalysis', 'thresholdNNT', 'permutationTestI2', 'limitMetaAnalysis',
    'waapWLS', 'multiCriteriaDecision', 'specificationCurveAnalysis',
    'vibrationOfEffects', 'livingReviewStatus', 'threeParameterSelectionModel', 'robustTau2',
    # Plots
    'renderForestPlot', 'renderFunnelPlot', 'renderBaujatPlot', 'renderCumulativePlot',
    'renderRadialPlot', 'renderLabbePlot', 'renderQQPlot', 'renderDOIPlot',
    # State
    'AppState', 'DEMO_DATASETS', 'loadDemoDataset',
    # UI functions
    'runTruthCertAnalysis', 'runHTAAnalysis',
    'runGOSHAnalysis', 'runTSAAnalysis', 'runPCurveAnalysis', 'runZCurveAnalysis',
    'runInfluenceDiagnostics', 'runCopasModel', 'runGRADEAssessment', 'runSmallSampleCI',
    'runExtendedValidationUI',
    # Export
    'exportCSV', 'exportJSON', 'exportToExcel'
]

print("=" * 70)
print("EXPOSED FUNCTIONS CHECK")
print("=" * 70)

not_exposed = []
exposed_count = 0

for func in important_functions:
    exists = driver.execute_script(f'return typeof window.{func} !== "undefined"')
    func_type = driver.execute_script(f'return typeof window.{func}')
    status = "OK" if exists else "MISSING"
    if exists:
        exposed_count += 1
    else:
        not_exposed.append(func)
    print(f"  [{status}] {func}: {func_type}")

print("=" * 70)
print(f"Total: {len(important_functions)} | Exposed: {exposed_count} | Missing: {len(not_exposed)}")
if not_exposed:
    print(f"\nMissing functions: {', '.join(not_exposed)}")
print("=" * 70)

driver.quit()
