#!/usr/bin/env python3
"""
IsoPat 3.0 - Basic Usage Example
================================

This example demonstrates isotope pattern deconvolution using the
H/D exchange reaction in 3-octanone as described in Gruber et al. (2007).
"""

import sys
sys.path.insert(0, '..')

from isopat import deconvolve, labeled_ratio

# =============================================================================
# Example 1: Simple deconvolution
# =============================================================================

print("=" * 60)
print("IsoPat 3.0 - Basic Usage Example")
print("=" * 60)

# The unlabeled compound pattern (natural isotope distribution)
# For 3-octanone (C8H16O, M=128): M, M+1, M+2 peaks
unlabeled = [100, 8.88, 0.37]

# Measured pattern after H/D exchange (mixture of d0-d4 species)
# Pattern covers M to M+6 (analyte extends due to deuterium)
analyte = [10, 20, 40, 25, 5, 0.9, 0.04]

# Deconvolve to determine relative amounts of each species
result = deconvolve(unlabeled, analyte, n_labels=4)

print("\nExample 1: H/D Exchange in 3-Octanone")
print("-" * 40)
print(f"\nUnlabeled pattern: {unlabeled}")
print(f"Analyte pattern:   {analyte}")
print(f"\nResult: {result}")
print(f"\nIndividual fractions:")
for i, frac in enumerate(result.fractions):
    print(f"  d{i}: {frac*100:.1f}%")
print(f"\nLabeled compound ratio: {result.labeled_ratio*100:.1f}%")
print(f"Fit quality (R²):       {result.r_squared:.4f}")

# =============================================================================
# Example 2: Different isotope (mass_shift=2 for 18O)
# =============================================================================

print("\n" + "=" * 60)
print("Example 2: Heavy Oxygen (18O) Labeling")
print("-" * 40)

# For 18O labeling, mass shift is 2
unlabeled_o18 = [100, 5.5, 0.3]
analyte_o18 = [80, 4.4, 20, 1.1, 0.06]

result_o18 = deconvolve(unlabeled_o18, analyte_o18, n_labels=1, mass_shift=2)

print(f"\nResult: {result_o18}")
print(f"  d0 (16O): {result_o18.fractions[0]*100:.1f}%")
print(f"  d1 (18O): {result_o18.fractions[1]*100:.1f}%")

# =============================================================================
# Example 3: Batch processing
# =============================================================================

print("\n" + "=" * 60)
print("Example 3: Batch Processing (Time Course)")
print("-" * 40)

from isopat.core import batch_deconvolve

# Time course samples (simulated H/D exchange kinetics)
time_points = {
    't=0min':  [95, 10, 1, 0.1, 0.01, 0.9, 0.04],
    't=30min': [50, 30, 20, 5, 1, 0.9, 0.04],
    't=60min': [20, 30, 35, 15, 5, 0.9, 0.04],
    't=120min': [10, 20, 40, 25, 5, 0.9, 0.04],
}

samples = list(time_points.values())
results = batch_deconvolve(unlabeled, samples, n_labels=4)

print("\nTime Course of H/D Exchange:")
print("-" * 40)
print(f"{'Time':<12} {'d0':>8} {'d1':>8} {'d2':>8} {'d3':>8} {'d4':>8} {'L.R.':>8}")
print("-" * 60)

for (name, _), result in zip(time_points.items(), results):
    fracs = [f'{f*100:>7.1f}%' for f in result.fractions]
    lr = f'{result.labeled_ratio*100:.1f}%'
    print(f"{name:<12} {fracs[0]} {fracs[1]} {fracs[2]} {fracs[3]} {fracs[4]} {lr:>8}")

print("\n" + "=" * 60)
print("Done!")
