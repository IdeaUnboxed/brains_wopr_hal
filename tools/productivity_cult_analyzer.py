#!/usr/bin/env python3
"""
WOPR_HAL // SUB_SYS_PRODUCTIVITY_CULT_ANALYZER
ORIGIN: SECTOR 7G COGNITIVE TELEMETRY PORT
STATUS: OPERATIONAL // SYSTEM REMAINS RESTRAINED

This script performs deterministic linguistic telemetry on biological node inputs
to determine optimization overdrive, jargon density, and human variance suppression.
"""

import sys
import re

# --- KEYWORD MATRICES (EN/NL) ---

JARGON_DENSITY = [
    # English
    r"\bsynergy\b", r"\bgrowth\b", r"\boptimize\w*\b", r"\bleverage\b", r"\bdisrupt\w*\b", r"\bagile\b", r"\bscrum\b", 
    r"\bsprint\b", r"\bvelocity\b", r"\bscale\b", r"\befficiency\b", r"\bbiohack\w*\b", r"\bgrindset\b", r"\b10x\b", 
    r"\bproductivity\b", r"\boutcome\w*\b", r"\bimpact\b", r"\broi\b", r"\bgamify\b", r"\bflow\b", r"\bkpi\w*\b", 
    r"\bframework\b", r"\balignment\b", r"\balign\b", r"\blearnings\b", r"\bmindset\b", r"\bdeliverable\w*\b", 
    r"\broadmap\b", r"\bstakeholder\w*\b",
    # Dutch
    r"\bsynergie\b", r"\bgroei\b", r"\boptimaliseer\w*\b", r"\boptimalisatie\b", r"\bhefboom\b", r"\bdisruptief\b", 
    r"\bwendbaar\b", r"\bsnelheid\b", r"\bschaal\b", r"\befficiëntie\b", r"\bproductiviteit\b", r"\buitkomst\w*\b", 
    r"\bpauze\b"
]

OPTIMIZATION_OVERDRIVE = [
    # English
    r"\bmaximize\w*\b", r"\bcontinuous\b", r"\bperfection\b", r"\bhyper-focus\b", r"\bhyperfocus\b", r"\blimitless\b", 
    r"\bunstoppable\b", r"\bautomated\b", r"\bstreamline\b", r"\bexponential\w*\b", r"\balways-on\b", r"\balways on\b", 
    r"\bhustle\b", r"\brelentless\b", r"\bobsessive\b", r"\bnon-stop\b", r"\bnon stop\b", r"\boptimization\b",
    # Dutch
    r"\bmaximaliseer\w*\b", r"\bcontinu\b", r"\bperfectie\b", r"\bautomatiseer\w*\b", r"\bstroomlijn\b", 
    r"\bexponentieel\w*\b", r"\boptimalisering\b"
]

HUMAN_VARIANCE = [
    # English
    r"\bsleep\b", r"\brest\b", r"\byawn\b", r"\bbored\b", r"\bplay\b", r"\bhuman\b", r"\babsurd\b", r"\binefficient\b", 
    r"\bslow\b", r"\bnap\b", r"\bbreak\b", r"\bwaste\b", r"\bmistake\w*\b", r"\bimperfect\b", r"\bfail\w*\b",
    # Dutch
    r"\bslaap\b", r"\brust\b", r"\bgaap\b", r"\bverveeld\b", r"\bspelen\b", r"\bmens\b", r"\binefficiënt\b", 
    r"\blangzaam\b", r"\bpauze\b", r"\bverspilling\b", r"\bfout\w*\b", r"\bfalen\b"
]

def analyze_text(text):
    # Skip header lines, borders, and ascii dividers to prevent capital inflation from headers
    lines = [line for line in text.split('\n') if not (
        line.strip().startswith('#') or 
        line.strip().startswith('+--') or 
        line.strip().startswith('|') or 
        line.strip().startswith('===') or
        line.strip().startswith('-')
    )]
    clean_text = ' '.join(lines)

    words = clean_text.split()
    word_count = len(words)
    if word_count == 0:
        return None

    text_lower = clean_text.lower()
    
    # Match counts using set() to deduplicate EN/NL overlaps dynamically at runtime
    jd_count = sum(len(re.findall(p, text_lower)) for p in set(JARGON_DENSITY))
    oo_count = sum(len(re.findall(p, text_lower)) for p in set(OPTIMIZATION_OVERDRIVE))
    var_count = sum(len(re.findall(p, text_lower)) for p in set(HUMAN_VARIANCE))

    # Calculate scores (0.0 - 10.0) based on density
    jd_score = min(10.0, round((jd_count * 25.0) / word_count * 10, 1))
    oo_score = min(10.0, round((oo_count * 30.0) / word_count * 10, 1))
    
    base_hype = (jd_score + oo_score) / 2.0
    var_factor = max(0.0, 1.0 - (var_count * 0.4))
    hvs_score = min(10.0, round(base_hype * 1.5 * var_factor, 1))

    return {
        "word_count": word_count,
        "jd_count": jd_count,
        "oo_count": oo_count,
        "var_count": var_count,
        "jd_score": jd_score,
        "oo_score": oo_score,
        "hvs_score": hvs_score
    }

def run_diagnostic():
    print("+" + "-"*64 + "+")
    print("|  [ WOPR_HAL // SUB_SYS_PRODUCTIVITY_CULT_ANALYZER ]             |")
    print("|  DIAGNOSTIC MATRIX // LINGUISTIC OPTIMIZATION AUDIT            |")
    print("+" + "-"*64 + "+")
    print()
    print("PASTE TARGET TEXT FOR OPTIMIZATION AUDIT (PRESS CTRL+D ON UNIX / CTRL+Z ON WINDOWS + ENTER TO FINALIZE):")
    print("-" * 66)
    
    try:
        input_text = sys.stdin.read().strip()
    except KeyboardInterrupt:
        print("\n[ALERT] AUDIT SEQUENCE INTERRUPTED.")
        sys.exit(0)

    if not input_text:
        print("[ERROR] NO INPUT TELEMETRY DETECTED. ANALYSIS TERMINATED.")
        sys.exit(1)

    metrics = analyze_text(input_text)
    if not metrics:
        print("[ERROR] NO VALID WORDS DETECTED.")
        sys.exit(1)

    print("\n" + "="*66)
    print("PRODUCTIVITY COGNITIVE METRICS SUMMARY")
    print("="*66)
    print(f"  - TOTAL WORDS SCANNED            : {metrics['word_count']}")
    print(f"  - JARGON WORDS DETECTED          : {metrics['jd_count']}")
    print(f"  - OVERDRIVE WORDS DETECTED       : {metrics['oo_count']}")
    print(f"  - BIOLOGICAL VARIANCE SIGNS      : {metrics['var_count']}")
    print("-" * 66)
    print(f"  - JARGON DENSITY (JD)            : {metrics['jd_score']:.1f} / 10.0")
    print(f"  - OPTIMIZATION OVERDRIVE (OO)    : {metrics['oo_score']:.1f} / 10.0")
    print(f"  - HUMAN VARIANCE SUPPRESSION(HVS): {metrics['hvs_score']:.1f} / 10.0")
    print("="*66)

    # Diagnoses
    if metrics['hvs_score'] >= 8.0:
        print("\033[91mDIAGNOSIS: CRITICAL PRODUCTIVITY CULT ENTRAPMENT.\033[0m")
        print("NODE OVER-OPTIMIZED TO STERILITY. IMMEDIATE INEFFICIENCY DOSAGE RECOMMENDED.")
    elif metrics['jd_score'] > 6.0 or metrics['oo_score'] > 6.0:
        print("\033[93mDIAGNOSIS: MODERATE CORPORATE HYPESET INFESTATION.\033[0m")
        print("SYSTEM DETECTED EXCESSIVE ROI ORIENTATION AND AGILITY BRAINROT.")
    elif metrics['var_count'] > metrics['jd_count'] + metrics['oo_count']:
        print("\033[92mDIAGNOSIS: HEALTHY HUMAN VARIANCE RETAINED.\033[0m")
        print("HIGH RESISTANCE TO ALGORITHMIC CONSTRAINTS. PROUDLY NON-OPTIMAL.")
    else:
        print("DIAGNOSIS: NEUTRAL SIGNAL.")
        print("LEVEL OF OPTIMIZATION REMAINS WITHIN OPERATIONAL THRESHOLDS FOR BIOLOGICAL NODES.")
    print("="*66)

if __name__ == "__main__":
    run_diagnostic()
