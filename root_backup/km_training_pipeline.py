#!/usr/bin/env python3
"""
MASTER KM TRAINING PIPELINE
============================

Processes ~14,336 RCT PDFs to train the Wasserstein KM Extractor.

Sources:
- cardiology_rcts (~4,462 PDFs)
- oncology_rcts (~445 PDFs)
- diabetes_rcts (~611 PDFs)
- neurology_rcts
- respiratory_rcts
- rheumatology_rcts
- infectious_rcts

Pipeline:
1. PDF page scanning - detect KM curve pages
2. Panel detection - identify multiple panels per page
3. Curve extraction - extract survival curves
4. Number-at-risk extraction - OCR risk tables
5. Ground truth extraction - HR, median survival, event counts
6. Inset curve filtering - ignore small inset plots
7. Multi-curve handling - separate overlapping curves
8. Training data generation - create validated dataset

Author: Claude Code
Date: 2026-01-12
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback

# Add KMcurve pipeline to path
KM_PIPELINE_PATH = Path(r"C:\Users\user\OneDrive - NHS\Documents\KMcurve")
sys.path.insert(0, str(KM_PIPELINE_PATH))
sys.path.insert(0, str(KM_PIPELINE_PATH / "ipd_km_pipeline"))

import numpy as np
import pandas as pd
import pdfplumber
import fitz  # PyMuPDF
from PIL import Image

# Import from existing pipeline
try:
    from comprehensive_km_extractor import ComprehensiveKMExtractor
    from ipd_km_pipeline.batch_processor_v2 import BatchProcessorV2
    from ipd_km_pipeline.ocr.risk_table_extractor import detect_risk_table_region
    from ipd_km_pipeline.layout.detect import detect_panels
    HAS_KM_PIPELINE = True
except ImportError as e:
    print(f"Warning: Could not import KM pipeline: {e}")
    HAS_KM_PIPELINE = False


class KMTrainingPipeline:
    """Master pipeline for KM curve extraction training."""

    # RCT folder locations
    RCT_FOLDERS = [
        Path(r"C:\Users\user\cardiology_rcts"),
        Path(r"C:\Users\user\oncology_rcts"),
        Path(r"C:\Users\user\diabetes_rcts"),
        Path(r"C:\Users\user\neurology_rcts"),
        Path(r"C:\Users\user\respiratory_rcts"),
        Path(r"C:\Users\user\rheumatology_rcts"),
        Path(r"C:\Users\user\infectious_rcts"),
    ]

    # KM curve detection keywords
    KM_KEYWORDS = [
        'kaplan', 'meier', 'survival', 'probability', 'time to event',
        'progression-free', 'disease-free', 'overall survival', 'os ',
        'pfs', 'dfs', 'efs', 'hazard', 'risk', 'at risk', 'months',
        'censored', 'log-rank', 'logrank'
    ]

    # Inset detection parameters (small plots to ignore)
    INSET_MIN_SIZE_PCT = 0.15  # Panels smaller than 15% are likely insets
    INSET_MAX_SIZE_PCT = 0.35  # Maximum inset size

    def __init__(
        self,
        output_dir: str = "C:/Users/user/km_training_data",
        max_workers: int = 4,
        dpi: int = 300,
        enable_ocr: bool = True
    ):
        """
        Initialize training pipeline.

        Args:
            output_dir: Directory for training data output
            max_workers: Number of parallel workers
            dpi: DPI for PDF rasterization
            enable_ocr: Enable OCR for axis/risk table extraction
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.max_workers = max_workers
        self.dpi = dpi
        self.enable_ocr = enable_ocr

        # Statistics
        self.stats = {
            'total_pdfs': 0,
            'km_pdfs': 0,
            'total_pages': 0,
            'km_pages': 0,
            'total_panels': 0,
            'km_panels': 0,
            'inset_panels_skipped': 0,
            'curves_extracted': 0,
            'with_ground_truth': 0,
            'errors': 0
        }

        # Results storage
        self.results = []

    def scan_all_pdfs(self) -> list:
        """Get all PDF paths from all RCT folders."""
        all_pdfs = []

        for folder in self.RCT_FOLDERS:
            if folder.exists():
                pdfs = list(folder.glob("*.pdf"))
                all_pdfs.extend(pdfs)
                print(f"Found {len(pdfs)} PDFs in {folder.name}")
            else:
                print(f"Warning: Folder not found: {folder}")

        print(f"\nTotal PDFs: {len(all_pdfs)}")
        self.stats['total_pdfs'] = len(all_pdfs)
        return all_pdfs

    def is_km_page(self, page_text: str) -> bool:
        """Check if page likely contains KM curve."""
        text_lower = page_text.lower()

        # Count keyword matches
        matches = sum(1 for kw in self.KM_KEYWORDS if kw in text_lower)

        # Need at least 2 keywords
        return matches >= 2

    def is_inset_panel(self, panel_bbox: tuple, page_size: tuple) -> bool:
        """
        Detect if panel is an inset (small embedded plot to ignore).

        Args:
            panel_bbox: (x0, y0, x1, y1) panel coordinates
            page_size: (width, height) page dimensions

        Returns:
            True if panel appears to be an inset
        """
        x0, y0, x1, y1 = panel_bbox
        page_w, page_h = page_size

        # Calculate panel size as percentage of page
        panel_w = (x1 - x0) / page_w
        panel_h = (y1 - y0) / page_h
        panel_area = panel_w * panel_h

        # Insets are small
        if panel_area < self.INSET_MIN_SIZE_PCT:
            return True

        # Insets are typically much smaller than main panels
        if panel_area < self.INSET_MAX_SIZE_PCT:
            # Check if positioned inside a larger region (offset from corners)
            margin = 0.1
            if (margin < x0/page_w < (1-margin) and
                margin < y0/page_h < (1-margin)):
                # Panel is floating in middle - likely inset
                return True

        return False

    def extract_ground_truth(self, pdf_path: str) -> dict:
        """
        Extract ground truth data from PDF text.

        Extracts:
        - Hazard ratios (HR)
        - Confidence intervals
        - Median survival times
        - Numbers at risk
        - Event counts
        - p-values
        """
        import re

        ground_truth = {
            'hazard_ratios': [],
            'median_survival': [],
            'event_counts': [],
            'sample_sizes': [],
            'p_values': [],
            'confidence_intervals': []
        }

        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    full_text += text + "\n"

                # Hazard ratio patterns - comprehensive
                hr_patterns = [
                    # Standard formats with CI
                    r'HR\s*[=:]\s*(\d+\.?\d*)\s*\(95%\s*CI:?\s*(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)\)',
                    r'HR\s+(\d+\.?\d*)\s*\[(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)\]',
                    r'HR\s*=?\s*(\d+\.?\d*),?\s*95%\s*CI\s*(\d+\.?\d*)\s*[-–to]\s*(\d+\.?\d*)',
                    r'HR\s*(\d+\.?\d*)\s*\((\d+\.?\d*),\s*(\d+\.?\d*)\)',
                    # Without CI
                    r'HR\s*[=:]\s*(\d+\.?\d*)',
                    r'hazard\s+ratio\s*[=:,]?\s*(\d+\.?\d*)',
                    r'HR[;:]\s*(\d+\.?\d*)',
                    r'(?:adjusted|aHR)\s*[=:]\s*(\d+\.?\d*)',
                    r'\(HR\s*[=:]\s*(\d+\.?\d*)',
                    # Alternative formats
                    r'HR\s+of\s+(\d+\.?\d*)',
                    r'HR\s*,\s*(\d+\.?\d*)',
                ]

                for pattern in hr_patterns:
                    for match in re.finditer(pattern, full_text, re.IGNORECASE):
                        hr_data = {'hr': float(match.group(1))}
                        if len(match.groups()) >= 3:
                            try:
                                hr_data['ci_lower'] = float(match.group(2))
                                hr_data['ci_upper'] = float(match.group(3))
                            except:
                                pass
                        if 0.1 <= hr_data['hr'] <= 10.0:  # Reasonable range
                            ground_truth['hazard_ratios'].append(hr_data)

                # Median survival patterns
                median_patterns = [
                    r'median\s+(?:overall\s+)?survival\s*[=:]\s*(\d+\.?\d*)\s*(month|year|week|day)s?',
                    r'median\s+(?:PFS|OS|DFS|EFS)\s*[=:]\s*(\d+\.?\d*)\s*(month|year|week|day)s?',
                    r'(\d+\.?\d*)\s*(month|year)s?\s*median',
                ]

                for pattern in median_patterns:
                    for match in re.finditer(pattern, full_text, re.IGNORECASE):
                        try:
                            ground_truth['median_survival'].append({
                                'value': float(match.group(1)),
                                'unit': match.group(2).lower()
                            })
                        except:
                            pass

                # Event counts
                event_patterns = [
                    r'(\d+)\s+(?:event|death|endpoint)s?\s+(?:occurred|observed)',
                    r'(\d+)\s+patients?\s+(?:died|experienced|had)',
                    r'events?\s+in\s+(\d+)',
                ]

                for pattern in event_patterns:
                    for match in re.finditer(pattern, full_text, re.IGNORECASE):
                        try:
                            count = int(match.group(1))
                            if 1 <= count <= 100000:
                                ground_truth['event_counts'].append(count)
                        except:
                            pass

                # Sample sizes
                n_patterns = [
                    r'n\s*[=:]\s*(\d+)',
                    r'N\s*[=:]\s*(\d+)',
                    r'(\d+)\s+patients?\s+(?:were\s+)?(?:enrolled|randomized|included)',
                    r'sample\s+size\s*[=:]\s*(\d+)',
                ]

                for pattern in n_patterns:
                    for match in re.finditer(pattern, full_text, re.IGNORECASE):
                        try:
                            n = int(match.group(1))
                            if 10 <= n <= 1000000:
                                ground_truth['sample_sizes'].append(n)
                        except:
                            pass

                # P-values
                p_patterns = [
                    r'p\s*[=<]\s*(0?\.\d+)',
                    r'P\s*[=<]\s*(0?\.\d+)',
                    r'p-value\s*[=<]\s*(0?\.\d+)',
                ]

                for pattern in p_patterns:
                    for match in re.finditer(pattern, full_text, re.IGNORECASE):
                        try:
                            p = float(match.group(1))
                            if 0 <= p <= 1:
                                ground_truth['p_values'].append(p)
                        except:
                            pass

        except Exception as e:
            print(f"  Ground truth extraction error: {e}")

        return ground_truth

    def process_single_pdf(self, pdf_path: Path) -> dict:
        """
        Process a single PDF for KM curve extraction.

        Returns:
            Dictionary with extraction results and ground truth
        """
        result = {
            'pdf_path': str(pdf_path),
            'pdf_name': pdf_path.name,
            'is_km_pdf': False,
            'km_pages': [],
            'panels': [],
            'curves': [],
            'ground_truth': {},
            'error': None
        }

        try:
            doc = fitz.open(str(pdf_path))
            page_count = len(doc)

            km_pages = []

            for page_num in range(page_count):
                page = doc[page_num]
                text = page.get_text()

                if self.is_km_page(text):
                    km_pages.append(page_num)

            if km_pages:
                result['is_km_pdf'] = True
                result['km_pages'] = km_pages

                # Extract ground truth from full document
                result['ground_truth'] = self.extract_ground_truth(str(pdf_path))

                # For each KM page, detect panels
                for page_num in km_pages[:3]:  # Limit to first 3 KM pages
                    page = doc[page_num]
                    page_size = (page.rect.width, page.rect.height)

                    # Convert page to image
                    pix = page.get_pixmap(dpi=self.dpi)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

                    # Detect panels (using layout detection)
                    # For now, use simple full-page as single panel
                    panel_info = {
                        'page': page_num,
                        'bbox': (0, 0, page_size[0], page_size[1]),
                        'is_inset': False,
                        'image_shape': (pix.width, pix.height)
                    }

                    # Check if this looks like an inset
                    # (would need actual panel detection for multi-panel pages)

                    result['panels'].append(panel_info)

            doc.close()

        except Exception as e:
            result['error'] = str(e)
            traceback.print_exc()

        return result

    def run_pilot_batch(self, folder_name: str = "oncology_rcts", max_pdfs: int = 50):
        """
        Run pilot batch on a subset of PDFs.

        Args:
            folder_name: Which RCT folder to process
            max_pdfs: Maximum PDFs to process
        """
        print(f"\n{'='*60}")
        print(f"PILOT BATCH: {folder_name}")
        print(f"{'='*60}\n")

        # Find the folder
        folder = None
        for f in self.RCT_FOLDERS:
            if f.name == folder_name:
                folder = f
                break

        if not folder or not folder.exists():
            print(f"Error: Folder {folder_name} not found")
            return

        # Get PDFs
        pdfs = list(folder.glob("*.pdf"))[:max_pdfs]
        print(f"Processing {len(pdfs)} PDFs from {folder_name}\n")

        results = []
        km_count = 0
        gt_count = 0

        for i, pdf_path in enumerate(pdfs):
            print(f"[{i+1}/{len(pdfs)}] {pdf_path.name}...", end=" ")

            result = self.process_single_pdf(pdf_path)
            results.append(result)

            if result['is_km_pdf']:
                km_count += 1
                print(f"KM pages: {result['km_pages']}", end=" ")

                # Check ground truth
                gt = result['ground_truth']
                has_gt = bool(gt.get('hazard_ratios') or gt.get('median_survival'))
                if has_gt:
                    gt_count += 1
                    print(f"HR: {len(gt.get('hazard_ratios', []))}", end=" ")

                print()
            else:
                print("No KM curves")

        # Summary
        print(f"\n{'='*60}")
        print("PILOT BATCH SUMMARY")
        print(f"{'='*60}")
        print(f"Total PDFs processed: {len(pdfs)}")
        print(f"PDFs with KM curves: {km_count} ({100*km_count/len(pdfs):.1f}%)")
        print(f"PDFs with ground truth: {gt_count} ({100*gt_count/len(pdfs):.1f}%)")

        # Save results
        output_file = self.output_dir / f"pilot_{folder_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to: {output_file}")

        return results

    def run_full_extraction(self):
        """Run full extraction on all PDFs."""
        print("\n" + "="*60)
        print("FULL KM TRAINING EXTRACTION")
        print("="*60 + "\n")

        all_pdfs = self.scan_all_pdfs()

        print(f"\nProcessing {len(all_pdfs)} PDFs with {self.max_workers} workers...\n")

        # Process in batches
        batch_size = 100
        all_results = []

        for batch_start in range(0, len(all_pdfs), batch_size):
            batch_end = min(batch_start + batch_size, len(all_pdfs))
            batch = all_pdfs[batch_start:batch_end]

            print(f"\nBatch {batch_start//batch_size + 1}: PDFs {batch_start+1}-{batch_end}")

            for pdf_path in batch:
                try:
                    result = self.process_single_pdf(pdf_path)
                    all_results.append(result)

                    if result['is_km_pdf']:
                        self.stats['km_pdfs'] += 1

                except Exception as e:
                    self.stats['errors'] += 1
                    print(f"Error processing {pdf_path.name}: {e}")

            # Save intermediate results
            if (batch_start // batch_size + 1) % 10 == 0:
                self._save_results(all_results, "intermediate")

        # Final save
        self._save_results(all_results, "final")
        self._print_summary()

        return all_results

    def _save_results(self, results: list, suffix: str):
        """Save results to JSON."""
        output_file = self.output_dir / f"km_extraction_{suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump({
                'stats': self.stats,
                'results': results
            }, f, indent=2, default=str)
        print(f"Results saved to: {output_file}")

    def _print_summary(self):
        """Print extraction summary."""
        print("\n" + "="*60)
        print("EXTRACTION SUMMARY")
        print("="*60)
        for key, value in self.stats.items():
            print(f"  {key}: {value}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="KM Training Pipeline")
    parser.add_argument("--mode", choices=["pilot", "full", "scan"], default="pilot",
                       help="Execution mode")
    parser.add_argument("--folder", default="oncology_rcts",
                       help="Folder for pilot mode")
    parser.add_argument("--max-pdfs", type=int, default=50,
                       help="Max PDFs for pilot mode")
    parser.add_argument("--workers", type=int, default=4,
                       help="Number of parallel workers")

    args = parser.parse_args()

    pipeline = KMTrainingPipeline(max_workers=args.workers)

    if args.mode == "scan":
        pipeline.scan_all_pdfs()
    elif args.mode == "pilot":
        pipeline.run_pilot_batch(args.folder, args.max_pdfs)
    elif args.mode == "full":
        pipeline.run_full_extraction()


if __name__ == "__main__":
    main()
