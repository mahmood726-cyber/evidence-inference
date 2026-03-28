#!/usr/bin/env python3
"""
FULL-SCALE KM BATCH RUNNER
===========================

Processes all 14,336 RCT PDFs across 7 therapeutic areas.
Designed for efficient batch processing with checkpointing.

Features:
- Parallel processing with configurable workers
- Automatic checkpointing every N PDFs
- Resume capability from last checkpoint
- Per-folder and overall statistics
- Memory-efficient streaming output

Usage:
    python km_batch_runner.py --mode full        # Process all PDFs
    python km_batch_runner.py --mode resume      # Resume from checkpoint
    python km_batch_runner.py --mode stats       # Show statistics only
    python km_batch_runner.py --folder oncology  # Process single folder

Author: Claude Code
Date: 2026-01-12
"""

import sys
import json
import os
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback
import argparse

# Import the training pipeline
from km_training_pipeline import KMTrainingPipeline


class BatchRunner:
    """Full-scale batch processing manager."""

    # Folder configuration with expected counts
    FOLDERS = {
        'cardiology_rcts': {'expected': 4462, 'priority': 1},
        'oncology_rcts': {'expected': 445, 'priority': 2},
        'diabetes_rcts': {'expected': 611, 'priority': 3},
        'respiratory_rcts': {'expected': 173, 'priority': 4},
        'rheumatology_rcts': {'expected': 173, 'priority': 5},
        'neurology_rcts': {'expected': 1, 'priority': 6},
        'infectious_rcts': {'expected': 0, 'priority': 7},
    }

    def __init__(
        self,
        output_dir: str = "C:/Users/user/km_training_data",
        checkpoint_interval: int = 100,
        max_workers: int = 4
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.checkpoint_interval = checkpoint_interval
        self.max_workers = max_workers

        self.checkpoint_file = self.output_dir / "checkpoint.json"
        self.stats_file = self.output_dir / "processing_stats.json"

        # Initialize pipeline
        self.pipeline = KMTrainingPipeline(
            output_dir=str(self.output_dir),
            max_workers=max_workers
        )

        # Load or initialize checkpoint
        self.checkpoint = self._load_checkpoint()

    def _load_checkpoint(self) -> dict:
        """Load checkpoint from disk or initialize."""
        if self.checkpoint_file.exists():
            with open(self.checkpoint_file) as f:
                return json.load(f)
        return {
            'processed_pdfs': [],
            'current_folder': None,
            'current_index': 0,
            'stats': {},
            'last_update': None
        }

    def _save_checkpoint(self):
        """Save checkpoint to disk."""
        self.checkpoint['last_update'] = datetime.now().isoformat()
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.checkpoint, f, indent=2)

    def process_folder(self, folder_name: str, resume: bool = False) -> dict:
        """
        Process all PDFs in a single folder.

        Args:
            folder_name: Name of the folder (e.g., 'oncology_rcts')
            resume: Whether to resume from checkpoint

        Returns:
            Statistics dictionary
        """
        folder_path = Path(f"C:/Users/user/{folder_name}")

        if not folder_path.exists():
            print(f"Warning: Folder not found: {folder_path}")
            return {'error': 'folder_not_found'}

        pdfs = sorted(folder_path.glob("*.pdf"))
        total_pdfs = len(pdfs)

        print(f"\n{'='*60}")
        print(f"PROCESSING: {folder_name}")
        print(f"Total PDFs: {total_pdfs}")
        print(f"{'='*60}\n")

        # Determine starting point
        start_index = 0
        if resume and self.checkpoint.get('current_folder') == folder_name:
            start_index = self.checkpoint.get('current_index', 0)
            print(f"Resuming from PDF {start_index + 1}")

        # Initialize folder stats
        folder_stats = {
            'folder': folder_name,
            'total_pdfs': total_pdfs,
            'processed': 0,
            'with_km': 0,
            'with_ground_truth': 0,
            'errors': 0,
            'start_time': datetime.now().isoformat()
        }

        # Results output file (append mode)
        results_file = self.output_dir / f"{folder_name}_results.jsonl"

        # Process PDFs
        processed_in_batch = 0

        for i, pdf_path in enumerate(pdfs[start_index:], start=start_index):
            try:
                print(f"[{i+1}/{total_pdfs}] {pdf_path.name}...", end=" ", flush=True)

                result = self.pipeline.process_single_pdf(pdf_path)
                folder_stats['processed'] += 1

                if result.get('is_km_pdf'):
                    folder_stats['with_km'] += 1
                    print(f"KM pages: {len(result.get('km_pages', []))}", end=" ")

                if result.get('ground_truth', {}).get('hazard_ratios'):
                    folder_stats['with_ground_truth'] += 1
                    print(f"HR: {len(result['ground_truth']['hazard_ratios'])}", end="")

                print()

                # Write result to JSONL file (streaming)
                with open(results_file, 'a') as f:
                    f.write(json.dumps(result, default=str) + '\n')

                # Update checkpoint
                processed_in_batch += 1
                if processed_in_batch >= self.checkpoint_interval:
                    self.checkpoint['current_folder'] = folder_name
                    self.checkpoint['current_index'] = i + 1
                    self.checkpoint['stats'][folder_name] = folder_stats
                    self._save_checkpoint()
                    processed_in_batch = 0
                    print(f"  [Checkpoint saved at PDF {i+1}]")

            except Exception as e:
                folder_stats['errors'] += 1
                print(f"ERROR: {e}")
                traceback.print_exc()

        # Final checkpoint
        folder_stats['end_time'] = datetime.now().isoformat()
        self.checkpoint['stats'][folder_name] = folder_stats
        self.checkpoint['current_folder'] = None
        self.checkpoint['current_index'] = 0
        self._save_checkpoint()

        # Print folder summary
        print(f"\n{'-'*40}")
        print(f"FOLDER COMPLETE: {folder_name}")
        print(f"  Processed: {folder_stats['processed']}")
        print(f"  With KM curves: {folder_stats['with_km']} ({100*folder_stats['with_km']/max(1,folder_stats['processed']):.1f}%)")
        print(f"  With ground truth: {folder_stats['with_ground_truth']} ({100*folder_stats['with_ground_truth']/max(1,folder_stats['processed']):.1f}%)")
        print(f"  Errors: {folder_stats['errors']}")
        print(f"{'-'*40}")

        return folder_stats

    def process_all(self, resume: bool = False):
        """Process all folders in priority order."""
        print("\n" + "="*60)
        print("FULL-SCALE KM TRAINING DATA EXTRACTION")
        print("="*60)
        print(f"Total expected PDFs: ~14,336")
        print(f"Workers: {self.max_workers}")
        print(f"Checkpoint interval: {self.checkpoint_interval}")
        print("="*60 + "\n")

        all_stats = {}

        # Sort folders by priority
        sorted_folders = sorted(
            self.FOLDERS.items(),
            key=lambda x: x[1]['priority']
        )

        for folder_name, config in sorted_folders:
            stats = self.process_folder(folder_name, resume=resume)
            all_stats[folder_name] = stats

        # Final summary
        self._print_final_summary(all_stats)

        return all_stats

    def _print_final_summary(self, all_stats: dict):
        """Print final processing summary."""
        print("\n" + "="*60)
        print("FINAL PROCESSING SUMMARY")
        print("="*60 + "\n")

        total_processed = 0
        total_km = 0
        total_gt = 0
        total_errors = 0

        for folder, stats in all_stats.items():
            if isinstance(stats, dict) and 'processed' in stats:
                print(f"{folder}:")
                print(f"  Processed: {stats['processed']}")
                print(f"  With KM: {stats['with_km']}")
                print(f"  With GT: {stats['with_ground_truth']}")
                print()

                total_processed += stats['processed']
                total_km += stats['with_km']
                total_gt += stats['with_ground_truth']
                total_errors += stats['errors']

        print("-"*40)
        print(f"TOTALS:")
        print(f"  Total PDFs: {total_processed}")
        print(f"  With KM curves: {total_km} ({100*total_km/max(1,total_processed):.1f}%)")
        print(f"  With ground truth: {total_gt} ({100*total_gt/max(1,total_processed):.1f}%)")
        print(f"  Errors: {total_errors}")

    def show_stats(self):
        """Show current processing statistics."""
        if self.checkpoint_file.exists():
            print("\nCurrent checkpoint status:")
            print(json.dumps(self.checkpoint, indent=2))
        else:
            print("No checkpoint found. Processing not started.")


def main():
    parser = argparse.ArgumentParser(description="Full-scale KM batch runner")
    parser.add_argument("--mode", choices=["full", "resume", "stats", "folder"],
                       default="stats", help="Execution mode")
    parser.add_argument("--folder", default=None,
                       help="Specific folder to process")
    parser.add_argument("--workers", type=int, default=4,
                       help="Number of parallel workers")
    parser.add_argument("--checkpoint-interval", type=int, default=100,
                       help="Save checkpoint every N PDFs")

    args = parser.parse_args()

    runner = BatchRunner(
        max_workers=args.workers,
        checkpoint_interval=args.checkpoint_interval
    )

    if args.mode == "stats":
        runner.show_stats()
    elif args.mode == "folder" and args.folder:
        runner.process_folder(args.folder)
    elif args.mode == "resume":
        runner.process_all(resume=True)
    elif args.mode == "full":
        runner.process_all(resume=False)


if __name__ == "__main__":
    main()
