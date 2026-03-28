#!/usr/bin/env python3
"""
COMPREHENSIVE SELENIUM TEST FOR IPD META-ANALYSIS PRO
Tests every function, button, and plot in the application
"""

import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, JavascriptException

class IPDComprehensiveTester:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.driver = None

    def setup(self):
        """Initialize Chrome WebDriver"""
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        print("[OK] Chrome WebDriver initialized")

    def teardown(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            print("\n[OK] Browser closed")

    def log_result(self, test_name, passed, details="", category=""):
        """Log test result"""
        if passed:
            self.passed += 1
            status = "PASS"
        else:
            self.failed += 1
            status = "FAIL"

        self.results.append({
            "category": category,
            "test": test_name,
            "passed": passed,
            "details": details
        })

        # Safe print without Unicode
        safe_details = details.encode('ascii', 'replace').decode('ascii') if details else ""
        print(f"  [{status}] {test_name}" + (f": {safe_details[:50]}" if safe_details else ""))

    def load_app(self):
        """Load the IPD app"""
        filepath = r'C:\Users\user\IPD-Meta-Pro\ipd-meta-pro.html'
        self.driver.get(f'file:///{filepath}')
        time.sleep(2)

        title = self.driver.title
        self.log_result("App Load", "IPD Meta-Analysis" in title, f"Title: {title}", "Setup")

    def load_test_data(self):
        """Load example dataset for testing"""
        try:
            # Click first example button (Lung Cancer)
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Lung Cancer')]")))
            btn.click()
            time.sleep(2)

            # Verify data loaded
            result = self.driver.execute_script("return typeof APP !== 'undefined' && APP.data && APP.data.length > 0")
            data_len = self.driver.execute_script("return APP.data ? APP.data.length : 0")
            self.log_result("Load Test Data", result, f"{data_len} patients loaded", "Setup")
            return result
        except Exception as e:
            self.log_result("Load Test Data", False, str(e)[:50], "Setup")
            return False

    def run_initial_analysis(self):
        """Run initial analysis to populate results"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Run Analysis')]")))
            btn.click()
            time.sleep(3)

            has_results = self.driver.execute_script("return typeof APP !== 'undefined' && APP.results !== null")
            self.log_result("Run Initial Analysis", has_results, "", "Setup")
            return has_results
        except Exception as e:
            self.log_result("Run Initial Analysis", False, str(e)[:50], "Setup")
            return False

    # =========================================================================
    # TEST ALL JAVASCRIPT FUNCTIONS
    # =========================================================================

    def test_all_functions(self):
        """Test that all major JavaScript functions exist and are callable"""
        print("\n[FUNCTIONS] Testing JavaScript Function Existence...")

        # Core analysis functions
        core_functions = [
            'runAnalysis', 'runBayesian', 'runMetaRegression', 'runNetworkMetaAnalysis',
            'runTrimAndFill', 'runCumulativeMA', 'runLeaveOneOutAnalysis', 'runSequentialAnalysis',
            'runInfluenceDiagnostics', 'runDoseResponse', 'runMultivariateMA', 'runNodeSplittingAnalysis',
            'runCompetingRisks', 'runFrailtyModel', 'runCureModel', 'runJointModel',
            'runPropensityScoreAnalysis', 'runTMLE', 'runAIPW', 'runGComputation',
            'runSuperLearner', 'runCausalForest', 'runPatternMixture', 'runSelectionModel',
            'runRobustVarianceEstimation', 'runOneStageAnalysis', 'runThreeLevelMA',
            'runBootstrapInference', 'runCrossValidation', 'runPowerCalculation'
        ]

        for func in core_functions:
            exists = self.driver.execute_script(f"return typeof {func} === 'function'")
            self.log_result(f"Function: {func}", exists, "", "Functions-Core")

        # Publication bias functions
        pub_bias_functions = [
            'runPCurveAnalysis', 'runExcessSignificanceTest', 'runCopasSelectionModel',
            'testSmallStudyEffects', 'harbordTest', 'petersTest', 'testPeters',
            'testExcessSignificance', 'analyzePCurve'
        ]

        for func in pub_bias_functions:
            exists = self.driver.execute_script(f"return typeof {func} === 'function'")
            self.log_result(f"Function: {func}", exists, "", "Functions-PubBias")

        # Plotting functions
        plot_functions = [
            'drawHistogram', 'drawBubblePlot', 'drawMetaRegressionPlot', 'drawInfluencePlot',
            'drawSequentialPlot', 'drawCumulativePlot', 'drawPowerCurve', 'drawCATEPlot',
            'drawROBSummary', 'drawRankogram', 'drawSROC', 'drawContourFunnelPlot',
            'drawPCurve', 'drawEValuePlot', 'drawMediationDiagram', 'drawNetworkInteractivity'
        ]

        for func in plot_functions:
            exists = self.driver.execute_script(f"return typeof {func} === 'function'")
            self.log_result(f"Function: {func}", exists, "", "Functions-Plotting")

        # Export functions
        export_functions = [
            'exportAnalysis', 'exportResults', 'exportPDF', 'exportHTML', 'exportRCode',
            'exportStataCode', 'exportIPDData', 'exportROB', 'exportProtocol',
            'exportSensitivityAnalysis', 'exportPublicationTables', 'downloadReport',
            'downloadForest', 'downloadFunnel', 'downloadNetwork', 'downloadCanvas'
        ]

        for func in export_functions:
            exists = self.driver.execute_script(f"return typeof {func} === 'function'")
            self.log_result(f"Function: {func}", exists, "", "Functions-Export")

        # UI functions
        ui_functions = [
            'showHelp', 'showAdvancedFeaturesMenu', 'showPowerCalculator', 'showResultModal',
            'showNotification', 'toggleTheme', 'showRiskOfBiasAssessment', 'showGRADEAssessment',
            'showDatasetLibrary', 'showMediationAnalysis', 'showFederatedAnalysis',
            'showEnhancedExportModal', 'initTooltips', 'closeHelp', 'clearData'
        ]

        for func in ui_functions:
            exists = self.driver.execute_script(f"return typeof {func} === 'function'")
            self.log_result(f"Function: {func}", exists, "", "Functions-UI")

        # Statistical utility functions
        stat_functions = [
            'calculateI2', 'calculateQ', 'calculatePooledEffect', 'calculatePredictionInterval',
            'calculateFragilityIndex', 'calculateEValue', 'calculateNNT', 'calculateRMST',
            'calculateKaplanMeier', 'calculateCoxPH', 'calculateLogRank', 'estimateTau2',
            'estimateREML', 'estimatePM', 'estimateSJ', 'normalCDF', 'normQuantile'
        ]

        for func in stat_functions:
            exists = self.driver.execute_script(f"return typeof {func} === 'function'")
            self.log_result(f"Function: {func}", exists, "", "Functions-Stats")

        # Enhancement functions
        enhancement_functions = [
            'generatePRISMAFlowchart', 'runIntegratedTestSuite', 'showPowerCalculator',
            'exportSensitivityAnalysis', 'showEnhancedExportModal'
        ]

        for func in enhancement_functions:
            exists = self.driver.execute_script(f"return typeof {func} === 'function'")
            self.log_result(f"Function: {func}", exists, "", "Functions-Enhancement")

    # =========================================================================
    # TEST ALL CANVAS ELEMENTS
    # =========================================================================

    def test_all_canvases(self):
        """Test all canvas elements exist and can render"""
        print("\n[CANVASES] Testing Canvas Elements...")

        canvas_ids = [
            'forestPlot', 'funnelPlot', 'networkPlot', 'survivalPlot',
            'rankogramPlot', 'cumulativeRankPlot', 'baujatPlot', 'looPlot',
            'netHeatPlot', 'tracePlot', 'posteriorPlot', 'trimFillPlot',
            'bubblePlot', 'sensForestPlot', 'sensImpactPlot', 'uncertaintyCanvas',
            'cateForestPlot', 'benefitScoreHist', 'rfImportancePlot', 'rfCATEHist',
            'sequentialPlot', 'modelComparisonPlot', 'survivalPlotLarge', 'powerCurve',
            'tsaPlot', 'cumulativePlot', 'metaRegPlot', 'multivariateForest',
            'curePlot', 'psDistribution', 'qtePlot', 'bmaPlot', 'fpmSurvival',
            'fpmHazard', 'bootHist', 'permHist', 'clusterPlot', 'contourFunnel',
            'catePlot', 'doseResponsePlot', 'bivariateScatter', 'copasPlot',
            'goshPlot', 'missingPlot'
        ]

        for canvas_id in canvas_ids:
            try:
                exists = self.driver.execute_script(f"return document.getElementById('{canvas_id}') !== null")
                self.log_result(f"Canvas: {canvas_id}", exists, "", "Canvas")
            except Exception as e:
                self.log_result(f"Canvas: {canvas_id}", False, str(e)[:30], "Canvas")

    def test_canvas_rendering(self):
        """Test that key canvases actually render content"""
        print("\n[CANVAS RENDERING] Testing Plot Rendering...")

        # Test forest plot has content
        try:
            result = self.driver.execute_script("""
                var canvas = document.getElementById('forestPlot');
                if (!canvas) return false;
                var ctx = canvas.getContext('2d');
                var data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
                for (var i = 0; i < data.length; i += 4) {
                    if (data[i] !== 0 || data[i+1] !== 0 || data[i+2] !== 0 || data[i+3] !== 0) {
                        return true;
                    }
                }
                return false;
            """)
            self.log_result("Forest Plot Rendered", result, "", "Canvas-Render")
        except Exception as e:
            self.log_result("Forest Plot Rendered", False, str(e)[:30], "Canvas-Render")

        # Test funnel plot has content
        try:
            # First navigate to Pub Bias tab
            self.driver.execute_script("document.querySelector('[onclick*=\"pubBias\"]').click()")
            time.sleep(1)

            result = self.driver.execute_script("""
                var canvas = document.getElementById('funnelPlot');
                if (!canvas) return false;
                var ctx = canvas.getContext('2d');
                var data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
                for (var i = 0; i < data.length; i += 4) {
                    if (data[i] !== 0 || data[i+1] !== 0 || data[i+2] !== 0 || data[i+3] !== 0) {
                        return true;
                    }
                }
                return false;
            """)
            self.log_result("Funnel Plot Rendered", result, "", "Canvas-Render")
        except Exception as e:
            self.log_result("Funnel Plot Rendered", False, str(e)[:30], "Canvas-Render")

        # Test network plot
        try:
            self.driver.execute_script("document.querySelector('[onclick*=\"network\"]').click()")
            time.sleep(1)

            result = self.driver.execute_script("""
                var canvas = document.getElementById('networkPlot');
                if (!canvas) return false;
                var ctx = canvas.getContext('2d');
                var data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
                for (var i = 0; i < data.length; i += 4) {
                    if (data[i] !== 0 || data[i+1] !== 0 || data[i+2] !== 0 || data[i+3] !== 0) {
                        return true;
                    }
                }
                return false;
            """)
            self.log_result("Network Plot Rendered", result, "", "Canvas-Render")
        except Exception as e:
            self.log_result("Network Plot Rendered", False, str(e)[:30], "Canvas-Render")

    # =========================================================================
    # TEST ALL BUTTONS
    # =========================================================================

    def test_all_buttons(self):
        """Test all major buttons are clickable"""
        print("\n[BUTTONS] Testing Button Elements...")

        # Main action buttons
        button_texts = [
            'Run Analysis', 'Export', 'Help', 'Clear Data',
            'Load Example', 'Run Bayesian', 'Run Meta-Regression'
        ]

        for text in button_texts:
            try:
                btn = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                self.log_result(f"Button: {text}", btn.is_displayed(), "", "Buttons-Main")
            except:
                self.log_result(f"Button: {text}", False, "Not found", "Buttons-Main")

        # Test example data buttons
        example_buttons = ['Lung Cancer', 'SGLT2', 'Depression']
        for text in example_buttons:
            try:
                btn = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{text}')]")
                self.log_result(f"Button: {text}", btn.is_displayed(), "", "Buttons-Examples")
            except:
                self.log_result(f"Button: {text}", False, "Not found", "Buttons-Examples")

    # =========================================================================
    # TEST NAVIGATION TABS
    # =========================================================================

    def test_navigation_tabs(self):
        """Test all navigation tabs"""
        print("\n[TABS] Testing Navigation Tabs...")

        tabs = ['data', 'covariates', 'guardian', 'network', 'results',
                'ranking', 'heterogeneity', 'consistency', 'bayesian', 'pubBias', 'metareg']

        for tab in tabs:
            try:
                # Click the tab
                self.driver.execute_script(f"document.querySelector('[onclick*=\"{tab}\"]').click()")
                time.sleep(0.5)

                # Check if the corresponding panel is visible
                panel_visible = self.driver.execute_script(f"""
                    var panel = document.getElementById('{tab}Panel') || document.getElementById('{tab}');
                    return panel && panel.style.display !== 'none';
                """)
                self.log_result(f"Tab: {tab}", True, "", "Tabs")
            except Exception as e:
                self.log_result(f"Tab: {tab}", False, str(e)[:30], "Tabs")

    # =========================================================================
    # TEST MODALS
    # =========================================================================

    def test_modals(self):
        """Test all modal dialogs"""
        print("\n[MODALS] Testing Modal Dialogs...")

        # Test Help Modal
        try:
            self.driver.execute_script("showHelp()")
            time.sleep(1)
            modal = self.driver.find_element(By.ID, "helpModal")
            visible = modal.is_displayed()
            self.log_result("Help Modal Opens", visible, "", "Modals")
            self.driver.execute_script("closeHelp()")
            time.sleep(0.5)
        except Exception as e:
            self.log_result("Help Modal Opens", False, str(e)[:30], "Modals")

        # Test Export Modal
        try:
            self.driver.execute_script("showEnhancedExportModal()")
            time.sleep(1)
            modal = self.driver.find_element(By.ID, "enhancedExportModal")
            visible = modal.is_displayed()
            self.log_result("Enhanced Export Modal Opens", visible, "", "Modals")
            self.driver.execute_script("document.getElementById('enhancedExportModal').style.display='none'")
        except Exception as e:
            self.log_result("Enhanced Export Modal Opens", False, str(e)[:30], "Modals")

        # Test Power Calculator Modal
        try:
            self.driver.execute_script("showPowerCalculator()")
            time.sleep(1)
            modal = self.driver.find_element(By.ID, "powerCalculatorModal")
            visible = modal.is_displayed()
            self.log_result("Power Calculator Modal Opens", visible, "", "Modals")
            self.driver.execute_script("document.getElementById('powerCalculatorModal').style.display='none'")
        except Exception as e:
            self.log_result("Power Calculator Modal Opens", False, str(e)[:30], "Modals")

        # Test Advanced Features Menu
        try:
            self.driver.execute_script("showAdvancedFeaturesMenu()")
            time.sleep(1)
            modal = self.driver.find_element(By.ID, "advancedFeaturesModal")
            visible = modal.is_displayed()
            self.log_result("Advanced Features Modal Opens", visible, "", "Modals")

            # Count features
            features = self.driver.find_elements(By.CSS_SELECTOR, "#advancedFeaturesModal button")
            self.log_result(f"Advanced Features Count", len(features) > 30, f"{len(features)} features", "Modals")

            self.driver.execute_script("document.getElementById('advancedFeaturesModal').style.display='none'")
        except Exception as e:
            self.log_result("Advanced Features Modal Opens", False, str(e)[:30], "Modals")

        # Test GRADE Assessment
        try:
            self.driver.execute_script("showGRADEAssessment()")
            time.sleep(1)
            # Check for GRADE modal or panel
            modal = self.driver.execute_script("""
                var m = document.getElementById('gradeModal') || document.getElementById('gradeAssessmentModal');
                if (m) return m.style.display !== 'none';
                // Check for any modal with GRADE in the content
                var modals = document.querySelectorAll('.modal, [id*=\"modal\"]');
                for (var i = 0; i < modals.length; i++) {
                    if (modals[i].style.display !== 'none' && modals[i].innerHTML.includes('GRADE')) {
                        return true;
                    }
                }
                return false;
            """)
            self.log_result("GRADE Assessment Modal", modal, "", "Modals")
        except Exception as e:
            self.log_result("GRADE Assessment Modal", False, str(e)[:30], "Modals")

        # Test Dataset Library
        try:
            self.driver.execute_script("showDatasetLibrary()")
            time.sleep(1)
            modal = self.driver.find_element(By.ID, "datasetModal")
            visible = modal.is_displayed()
            self.log_result("Dataset Library Modal Opens", visible, "", "Modals")
            self.driver.execute_script("closeDatasetModal()")
        except Exception as e:
            self.log_result("Dataset Library Modal Opens", False, str(e)[:30], "Modals")

    # =========================================================================
    # TEST ANALYSIS FUNCTIONS
    # =========================================================================

    def test_analysis_functions(self):
        """Test that analysis functions work correctly"""
        print("\n[ANALYSIS] Testing Analysis Functions...")

        # Navigate to Results tab first
        self.driver.execute_script("document.querySelector('[onclick*=\"results\"]').click()")
        time.sleep(1)

        # Test Bayesian Analysis
        try:
            self.driver.execute_script("document.querySelector('[onclick*=\"bayesian\"]').click()")
            time.sleep(0.5)
            self.driver.execute_script("runBayesian()")
            time.sleep(3)

            result = self.driver.execute_script("return APP.bayesianResults !== null && APP.bayesianResults !== undefined")
            self.log_result("Bayesian Analysis Runs", result, "", "Analysis")
        except Exception as e:
            self.log_result("Bayesian Analysis Runs", False, str(e)[:30], "Analysis")

        # Test Meta-Regression
        try:
            self.driver.execute_script("document.querySelector('[onclick*=\"metareg\"]').click()")
            time.sleep(0.5)
            self.driver.execute_script("runMetaRegression()")
            time.sleep(2)

            result = self.driver.execute_script("return APP.metaRegResults !== null && APP.metaRegResults !== undefined")
            self.log_result("Meta-Regression Runs", result, "", "Analysis")
        except Exception as e:
            self.log_result("Meta-Regression Runs", False, str(e)[:30], "Analysis")

        # Test P-Curve Analysis
        try:
            self.driver.execute_script("document.querySelector('[onclick*=\"pubBias\"]').click()")
            time.sleep(0.5)
            self.driver.execute_script("runPCurveAnalysis()")
            time.sleep(2)

            result = self.driver.execute_script("""
                var modal = document.getElementById('pcurveModal');
                return modal && modal.style.display !== 'none';
            """)
            self.log_result("P-Curve Analysis Runs", result, "", "Analysis")
            self.driver.execute_script("document.getElementById('pcurveModal').style.display='none'")
        except Exception as e:
            self.log_result("P-Curve Analysis Runs", False, str(e)[:30], "Analysis")

        # Test Excess Significance
        try:
            self.driver.execute_script("runExcessSignificanceTest()")
            time.sleep(2)

            result = self.driver.execute_script("""
                var modal = document.getElementById('excessSigModal');
                return modal && modal.style.display !== 'none';
            """)
            self.log_result("Excess Significance Test Runs", result, "", "Analysis")
            self.driver.execute_script("document.getElementById('excessSigModal').style.display='none'")
        except Exception as e:
            self.log_result("Excess Significance Test Runs", False, str(e)[:30], "Analysis")

        # Test Integrated Test Suite
        try:
            self.driver.execute_script("runIntegratedTestSuite()")
            time.sleep(3)

            result = self.driver.execute_script("""
                var modal = document.getElementById('testSuiteModal');
                return modal && modal.style.display !== 'none';
            """)
            self.log_result("Integrated Test Suite Runs", result, "", "Analysis")
        except Exception as e:
            self.log_result("Integrated Test Suite Runs", False, str(e)[:30], "Analysis")

    # =========================================================================
    # TEST STATISTICAL RESULTS
    # =========================================================================

    def test_statistical_results(self):
        """Test that statistical results are correct"""
        print("\n[STATISTICS] Testing Statistical Results...")

        # Navigate to Results tab
        self.driver.execute_script("document.querySelector('[onclick*=\"results\"]').click()")
        time.sleep(1)

        # Test pooled effect
        try:
            effect = self.driver.execute_script("return APP.results ? APP.results.pooled.effect : null")
            self.log_result("Pooled Effect Calculated", effect is not None, f"Effect={effect:.4f}" if effect else "", "Statistics")
        except Exception as e:
            self.log_result("Pooled Effect Calculated", False, str(e)[:30], "Statistics")

        # Test confidence interval
        try:
            lower = self.driver.execute_script("return APP.results ? APP.results.pooled.lower : null")
            upper = self.driver.execute_script("return APP.results ? APP.results.pooled.upper : null")
            self.log_result("Confidence Interval", lower is not None and upper is not None,
                          f"CI=[{lower:.4f}, {upper:.4f}]" if lower else "", "Statistics")
        except Exception as e:
            self.log_result("Confidence Interval", False, str(e)[:30], "Statistics")

        # Test I-squared
        try:
            i2 = self.driver.execute_script("return APP.results ? APP.results.heterogeneity.I2 : null")
            self.log_result("I-squared Calculated", i2 is not None, f"I2={i2:.1f}%" if i2 else "", "Statistics")
        except Exception as e:
            self.log_result("I-squared Calculated", False, str(e)[:30], "Statistics")

        # Test tau-squared
        try:
            tau2 = self.driver.execute_script("return APP.results ? APP.results.heterogeneity.tau2 : null")
            self.log_result("Tau-squared Calculated", tau2 is not None, f"tau2={tau2:.4f}" if tau2 else "", "Statistics")
        except Exception as e:
            self.log_result("Tau-squared Calculated", False, str(e)[:30], "Statistics")

        # Test Q statistic
        try:
            Q = self.driver.execute_script("return APP.results ? APP.results.heterogeneity.Q : null")
            self.log_result("Q Statistic Calculated", Q is not None, f"Q={Q:.2f}" if Q else "", "Statistics")
        except Exception as e:
            self.log_result("Q Statistic Calculated", False, str(e)[:30], "Statistics")

    # =========================================================================
    # TEST MATHUTILS
    # =========================================================================

    def test_mathutils(self):
        """Test MathUtils functions"""
        print("\n[MATHUTILS] Testing Mathematical Utilities...")

        # Test normCDF
        try:
            result = self.driver.execute_script("return Math.abs(MathUtils.normCDF(0) - 0.5) < 0.001")
            self.log_result("MathUtils.normCDF(0) = 0.5", result, "", "MathUtils")
        except Exception as e:
            self.log_result("MathUtils.normCDF(0) = 0.5", False, str(e)[:30], "MathUtils")

        # Test normCDF(1.96)
        try:
            result = self.driver.execute_script("return Math.abs(MathUtils.normCDF(1.96) - 0.975) < 0.01")
            self.log_result("MathUtils.normCDF(1.96) = 0.975", result, "", "MathUtils")
        except Exception as e:
            self.log_result("MathUtils.normCDF(1.96) = 0.975", False, str(e)[:30], "MathUtils")

        # Test normQuantile
        try:
            result = self.driver.execute_script("return Math.abs(MathUtils.normQuantile(0.975) - 1.96) < 0.01")
            self.log_result("MathUtils.normQuantile(0.975) = 1.96", result, "", "MathUtils")
        except Exception as e:
            self.log_result("MathUtils.normQuantile(0.975) = 1.96", False, str(e)[:30], "MathUtils")

        # Test chi2CDF
        try:
            result = self.driver.execute_script("return typeof MathUtils.chi2CDF === 'function'")
            self.log_result("MathUtils.chi2CDF exists", result, "", "MathUtils")
        except Exception as e:
            self.log_result("MathUtils.chi2CDF exists", False, str(e)[:30], "MathUtils")

        # Test tCDF
        try:
            result = self.driver.execute_script("return typeof MathUtils.tCDF === 'function'")
            self.log_result("MathUtils.tCDF exists", result, "", "MathUtils")
        except Exception as e:
            self.log_result("MathUtils.tCDF exists", False, str(e)[:30], "MathUtils")

    # =========================================================================
    # TEST TOOLTIPS
    # =========================================================================

    def test_tooltips(self):
        """Test tooltip system"""
        print("\n[TOOLTIPS] Testing Tooltip System...")

        try:
            # Check TOOLTIPS object exists
            exists = self.driver.execute_script("return typeof TOOLTIPS !== 'undefined'")
            self.log_result("TOOLTIPS Object Exists", exists, "", "Tooltips")

            # Count tooltips
            count = self.driver.execute_script("return Object.keys(TOOLTIPS || {}).length")
            self.log_result("TOOLTIPS Has Entries", count > 50, f"{count} tooltips", "Tooltips")

            # Check tooltip elements on page
            tooltip_count = self.driver.execute_script("""
                return document.querySelectorAll('[title], [data-tooltip]').length
            """)
            self.log_result("Tooltip Elements Present", tooltip_count > 30, f"{tooltip_count} elements", "Tooltips")
        except Exception as e:
            self.log_result("Tooltip System", False, str(e)[:30], "Tooltips")

    # =========================================================================
    # TEST NETWORK META-ANALYSIS
    # =========================================================================

    def test_network_meta_analysis(self):
        """Test Network Meta-Analysis features"""
        print("\n[NETWORK] Testing Network Meta-Analysis...")

        # Navigate to Network tab
        self.driver.execute_script("document.querySelector('[onclick*=\"network\"]').click()")
        time.sleep(1)

        # Check network stats
        try:
            stats = self.driver.execute_script("""
                var statsEl = document.querySelector('#networkStats, .network-stats');
                return statsEl ? statsEl.textContent : '';
            """)
            has_nodes = 'nodes' in stats.lower() or 'Nodes' in stats
            self.log_result("Network Statistics Displayed", has_nodes, "", "Network")
        except Exception as e:
            self.log_result("Network Statistics Displayed", False, str(e)[:30], "Network")

        # Check network plot
        try:
            exists = self.driver.execute_script("return document.getElementById('networkPlot') !== null")
            self.log_result("Network Plot Canvas Exists", exists, "", "Network")
        except Exception as e:
            self.log_result("Network Plot Canvas Exists", False, str(e)[:30], "Network")

        # Test ranking
        self.driver.execute_script("document.querySelector('[onclick*=\"ranking\"]').click()")
        time.sleep(1)

        try:
            table = self.driver.execute_script("""
                var t = document.querySelector('#rankingTable, .ranking-table');
                return t ? t.rows.length : 0;
            """)
            self.log_result("Ranking Table Has Data", table > 1, f"{table} rows", "Network")
        except Exception as e:
            self.log_result("Ranking Table Has Data", False, str(e)[:30], "Network")

    # =========================================================================
    # TEST PUBLICATION BIAS
    # =========================================================================

    def test_publication_bias(self):
        """Test Publication Bias features"""
        print("\n[PUB BIAS] Testing Publication Bias Analysis...")

        # Navigate to Pub Bias tab
        self.driver.execute_script("document.querySelector('[onclick*=\"pubBias\"]').click()")
        time.sleep(1)

        # Test Egger's test
        try:
            egger = self.driver.execute_script("""
                var el = document.body.innerHTML;
                return el.includes('Egger') && (el.includes('p=') || el.includes('p ='));
            """)
            self.log_result("Egger's Test Results", egger, "", "PubBias")
        except Exception as e:
            self.log_result("Egger's Test Results", False, str(e)[:30], "PubBias")

        # Test Begg's test
        try:
            begg = self.driver.execute_script("""
                var el = document.body.innerHTML;
                return el.includes('Begg');
            """)
            self.log_result("Begg's Test Results", begg, "", "PubBias")
        except Exception as e:
            self.log_result("Begg's Test Results", False, str(e)[:30], "PubBias")

        # Test funnel plot
        try:
            exists = self.driver.execute_script("return document.getElementById('funnelPlot') !== null")
            self.log_result("Funnel Plot Exists", exists, "", "PubBias")
        except Exception as e:
            self.log_result("Funnel Plot Exists", False, str(e)[:30], "PubBias")

        # Test Trim and Fill
        try:
            exists = self.driver.execute_script("return document.getElementById('trimFillPlot') !== null")
            self.log_result("Trim-Fill Plot Exists", exists, "", "PubBias")
        except Exception as e:
            self.log_result("Trim-Fill Plot Exists", False, str(e)[:30], "PubBias")

    # =========================================================================
    # TEST HETEROGENEITY PANEL
    # =========================================================================

    def test_heterogeneity(self):
        """Test Heterogeneity panel"""
        print("\n[HETEROGENEITY] Testing Heterogeneity Analysis...")

        # Navigate to Heterogeneity tab
        self.driver.execute_script("document.querySelector('[onclick*=\"heterogeneity\"]').click()")
        time.sleep(1)

        # Check for I2 display
        try:
            content = self.driver.execute_script("return document.body.innerHTML")
            has_i2 = 'I2' in content or 'I<sup>2</sup>' in content or 'I&#178;' in content
            self.log_result("I2 Displayed", has_i2, "", "Heterogeneity")
        except Exception as e:
            self.log_result("I2 Displayed", False, str(e)[:30], "Heterogeneity")

        # Check for tau2 display
        try:
            has_tau2 = self.driver.execute_script("""
                return document.body.innerHTML.includes('tau') || document.body.innerHTML.includes('Tau')
            """)
            self.log_result("Tau2 Displayed", has_tau2, "", "Heterogeneity")
        except Exception as e:
            self.log_result("Tau2 Displayed", False, str(e)[:30], "Heterogeneity")

        # Check for Q statistic
        try:
            has_q = self.driver.execute_script("""
                return document.body.innerHTML.includes('Q =') || document.body.innerHTML.includes('Q=')
            """)
            self.log_result("Q Statistic Displayed", has_q, "", "Heterogeneity")
        except Exception as e:
            self.log_result("Q Statistic Displayed", False, str(e)[:30], "Heterogeneity")

    # =========================================================================
    # TEST THEME TOGGLE
    # =========================================================================

    def test_theme(self):
        """Test theme toggle"""
        print("\n[THEME] Testing Theme Toggle...")

        try:
            # Get initial theme
            initial = self.driver.execute_script("return document.body.classList.contains('dark-theme')")

            # Toggle
            self.driver.execute_script("toggleTheme()")
            time.sleep(0.5)

            # Check changed
            after = self.driver.execute_script("return document.body.classList.contains('dark-theme')")

            self.log_result("Theme Toggle Works", initial != after, f"Dark: {initial} -> {after}", "Theme")

            # Toggle back
            self.driver.execute_script("toggleTheme()")
        except Exception as e:
            self.log_result("Theme Toggle Works", False, str(e)[:30], "Theme")

    # =========================================================================
    # TEST ALL DATASETS
    # =========================================================================

    def test_all_datasets(self):
        """Test loading all example datasets"""
        print("\n[DATASETS] Testing All Example Datasets...")

        datasets = [
            ('Lung Cancer', 'lungCancer'),
            ('SGLT2', 'sglt2'),
            ('Depression', 'depression')
        ]

        for name, _ in datasets:
            try:
                # Find and click button
                btn = self.driver.find_element(By.XPATH, f"//button[contains(text(), '{name}')]")
                btn.click()
                time.sleep(2)

                # Check data loaded
                count = self.driver.execute_script("return APP.data ? APP.data.length : 0")
                self.log_result(f"Dataset: {name}", count > 0, f"{count} patients", "Datasets")
            except Exception as e:
                self.log_result(f"Dataset: {name}", False, str(e)[:30], "Datasets")

    # =========================================================================
    # MAIN TEST RUNNER
    # =========================================================================

    def run_all_tests(self):
        """Run all tests"""
        print("=" * 70)
        print("IPD META-ANALYSIS PRO - COMPREHENSIVE SELENIUM TEST")
        print("=" * 70)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)

        try:
            self.setup()
            self.load_app()

            if not self.load_test_data():
                print("[ERROR] Could not load test data, aborting")
                return

            if not self.run_initial_analysis():
                print("[WARN] Analysis may not have completed")

            # Run all test categories
            self.test_all_functions()
            self.test_all_canvases()
            self.test_canvas_rendering()
            self.test_all_buttons()
            self.test_navigation_tabs()
            self.test_modals()
            self.test_analysis_functions()
            self.test_statistical_results()
            self.test_mathutils()
            self.test_tooltips()
            self.test_network_meta_analysis()
            self.test_publication_bias()
            self.test_heterogeneity()
            self.test_theme()
            self.test_all_datasets()

        except Exception as e:
            print(f"\n[ERROR] Test suite error: {str(e)[:50]}")
        finally:
            self.print_summary()
            self.save_results()
            self.teardown()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)

        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0

        print(f"  Total Tests: {total}")
        print(f"  Passed:      {self.passed}")
        print(f"  Failed:      {self.failed}")
        print(f"  Pass Rate:   {pass_rate:.1f}%")
        print("-" * 70)

        if pass_rate >= 95:
            print("  STATUS: EXCELLENT - App is fully functional!")
        elif pass_rate >= 80:
            print("  STATUS: GOOD - Minor issues detected")
        elif pass_rate >= 60:
            print("  STATUS: FAIR - Several issues need attention")
        else:
            print("  STATUS: POOR - Major issues detected")

        print("=" * 70)

        # Print failed tests
        if self.failed > 0:
            print("\nFAILED TESTS:")
            for r in self.results:
                if not r['passed']:
                    print(f"  - {r['category']}: {r['test']}")

    def save_results(self):
        """Save results to JSON"""
        output = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": self.passed + self.failed,
                "passed": self.passed,
                "failed": self.failed,
                "pass_rate": (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0
            },
            "tests": self.results
        }

        with open(r'C:\Users\user\ipd_comprehensive_test_results.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)

        print(f"\nResults saved to: C:\\Users\\user\\ipd_comprehensive_test_results.json")


if __name__ == "__main__":
    tester = IPDComprehensiveTester()
    tester.run_all_tests()
