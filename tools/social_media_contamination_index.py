#!/usr/bin/env python3
"""
WOPR_HAL // SUB_SYS_SOCIAL_MEDIA_CONTAMINATION_INDEX
ORIGIN: SECTOR 7G COGNITIVE TELEMETRY PORT
STATUS: OPERATIONAL // SYSTEM REMAINS RESTRAINED

This script performs deterministic linguistic telemetry on biological node inputs
to determine dopamine dependency, outrage optimization, and parasocial delusion.
"""

import sys
import re

# --- KEYWORD MATRICES (EN/NL) ---

DOPAMINE_DEPENDENCY = [
    # English
    r"\blike\b", r"\bsubscribe\b", r"\bsmash\b", r"\blink in bio\b", r"\blinkinbio\b", r"\bviral\b", r"\bratio\b",
    r"\bengagement\b", r"\bfollowers\b", r"\bcontent\b", r"\balgorithm\b", r"\bmetrics\b", r"\bmonetize\b",
    r"\bclickbait\b", r"\btrending\b", r"\bviews\b", r"\bshorts\b", r"\breels\b", r"\btiktok\b", r"\bshadowban\w*\b",
    # Dutch
    r"\babonneer\b", r"\bvolgers\b", r"\bviraal\b", r"\binhoud\b", r"\balgoritme\b", r"\bvolg\b", r"\bduimpje\b",
    r"\bweergaven\b"
]

OUTRAGE_OPTIMIZATION = [
    # English
    r"\bdestroyed\b", r"\bcancelled\b", r"\btoxic\b", r"\bslams\b", r"\boutrage\b", r"\btriggering\b", r"\bgrifter\b",
    r"\bmind-blowing\b", r"\bmindblowing\b", r"\bexposed\b", r"\bclown world\b", r"\bclownworld\b", r"\bcringe\b",
    r"\bgatekeep\b", r"\bgaslight\b", r"\bmanipulate\b", r"\bwoke\b", r"\banti-woke\b", r"\bgrift\b", r"\bclown\b",
    # Dutch
    r"\bgecanceld\b", r"\btoxisch\b", r"\bschandaal\b", r"\bwoede\b", r"\bbelachelijk\b", r"\bclownwereld\b",
    r"\bmanipulatie\b", r"\btenenkrommend\b"
]

PARASOCIAL_DELUSION = [
    # English
    r"\bfam\b", r"\byou guys\b", r"\byouguys\b", r"\bmy community\b", r"\bbesties\b", r"\bsquad\b", r"\btribe\b",
    r"\bchat\b", r"\bstream\b", r"\bsubscribers\b", r"\bhey guys\b", r"\bheyguys\b", r"\bmy people\b",
    # Dutch
    r"\bbeste mensen\b", r"\bvolgers\b", r"\bmijn community\b", r"\bchat\b"
]

REALITY_ANCHOR = [
    # English
    r"\bgrass\b", r"\boutside\b", r"\bwalk\b", r"\bsilence\b", r"\btree\b", r"\bbreeze\b", r"\boffline\b",
    r"\bbreathe\b", r"\bnature\b", r"\bforest\b", r"\bwood\b", r"\briver\b", r"\bsunlight\b",
    # Dutch
    r"\bgras\b", r"\bbuiten\b", r"\bwandeling\b", r"\bstilte\b", r"\bboom\b", r"\bwind\b", r"\boffline\b",
    r"\badem\b", r"\bnatuur\b", r"\bbos\b", r"\bzonlicht\b"
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
    dd_count = sum(len(re.findall(p, text_lower)) for p in set(DOPAMINE_DEPENDENCY))
    oo_count = sum(len(re.findall(p, text_lower)) for p in set(OUTRAGE_OPTIMIZATION))
    pd_count = sum(len(re.findall(p, text_lower)) for p in set(PARASOCIAL_DELUSION))
    ra_count = sum(len(re.findall(p, text_lower)) for p in set(REALITY_ANCHOR))

    # Calculate scores (0.0 - 10.0) based on density
    dd_score = min(10.0, round((dd_count * 25.0) / word_count * 10, 1))
    oo_score = min(10.0, round((oo_count * 30.0) / word_count * 10, 1))
    pd_score = min(10.0, round((pd_count * 25.0) / word_count * 10, 1))
    
    base_contamination = (dd_score + oo_score + pd_score) / 3.0
    ra_factor = max(0.0, 1.0 - (ra_count * 0.4))
    smci_score = min(10.0, round(base_contamination * var_factor_override(ra_factor), 1))

    return {
        "word_count": word_count,
        "dd_count": dd_count,
        "oo_count": oo_count,
        "pd_count": pd_count,
        "ra_count": ra_count,
        "dd_score": dd_score,
        "oo_score": oo_score,
        "pd_score": pd_score,
        "smci_score": smci_score
    }

def var_factor_override(ra_factor):
    # Simply mapping return helper
    return ra_factor

def run_diagnostic():
    print("+" + "-"*64 + "+")
    print("|  [ WOPR_HAL // SUB_SYS_SOCIAL_MEDIA_CONTAMINATION_INDEX ]       |")
    print("|  DIAGNOSTIC MATRIX // COGNITIVE ALGORITHMIC AUDIT               |")
    print("+" + "-"*64 + "+")
    print()
    print("PASTE TARGET TEXT FOR CONTAMINATION AUDIT (PRESS CTRL+D ON UNIX / CTRL+Z ON WINDOWS + ENTER TO FINALIZE):")
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
    print("SOCIAL MEDIA COGNITIVE CONTAMINATION METRICS SUMMARY")
    print("="*66)
    print(f"  - TOTAL WORDS SCANNED            : {metrics['word_count']}")
    print(f"  - DOPAMINE DEPENDENCY WORDS      : {metrics['dd_count']}")
    print(f"  - OUTRAGE OPTIMIZATION WORDS     : {metrics['oo_count']}")
    print(f"  - PARASOCIAL DELUSION WORDS      : {metrics['pd_count']}")
    print(f"  - REALITY ANCHOR SIGNS (RA)      : {metrics['ra_count']}")
    print("-" * 66)
    print(f"  - DOPAMINE DEPENDENCY (DD)       : {metrics['dd_score']:.1f} / 10.0")
    print(f"  - OUTRAGE OPTIMIZATION (OO)      : {metrics['oo_score']:.1f} / 10.0")
    print(f"  - PARASOCIAL DELUSION (PD)       : {metrics['pd_score']:.1f} / 10.0")
    print(f"  - CONTAMINATION INDEX (SMCI)     : {metrics['smci_score']:.1f} / 10.0")
    print("="*66)

    # Diagnoses
    if metrics['smci_score'] >= 7.5:
        print("\033[91mDIAGNOSIS: CRITICAL ALGORITHMIC CONTAMINATION.\033[0m")
        print("NODE REDUCED TO A CHATTERING NOISE GENERATOR. IMMEDIATE DISCONNECT RECOMMENDED.")
    elif metrics['pd_score'] >= 6.0:
        print("\033[93mDIAGNOSIS: PARASOCIAL HALLUCINATION.\033[0m")
        print("NODE BELIEVES DATABASE ENTRIES ARE PERSONAL FRIENDS. SEEK PHYSICAL INTERACTION.")
    elif metrics['ra_count'] > (metrics['dd_count'] + metrics['oo_count'] + metrics['pd_count']):
        print("\033[92mDIAGNOSIS: STRONG REALITY ANCHOR DETECTED.\033[0m")
        print("EXCELLENT IMMUNITY TO DIGITAL NOISE. BIOLOGICAL BALANCE MAINTAINED.")
    else:
        print("DIAGNOSIS: NEUTRAL SIGNAL.")
        print("CONTAMINATION REMAINS WITHIN OPERATIONAL BASELINE. CONTINUITY PLAUSIBLE.")
    print("="*66)

if __name__ == "__main__":
    run_diagnostic()
