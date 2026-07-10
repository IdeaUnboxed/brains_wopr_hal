#!/usr/bin/env python3
"""
WOPR_HAL // SUB_SYS_TRIBAL_MON_83 // TRIBALISM DETECTOR
ORIGIN: SECTOR 7G COGNITIVE TELEMETRY PORT
STATUS: OPERATIONAL // SYSTEM REMAINS RESTRAINED

This script performs deterministic linguistic telemetry on biological node inputs
to determine group-synchronization, polarization, and heuristic collapse.
"""

import sys
import re

# --- KEYWORD MATRICES (EN/NL) ---

HIGH_AROUSAL = [
    # English
    r"\bcrush\w*\b", r"\bdestroy\w*\b", r"\bthreat\w*\b", r"\bwarn\w*\b", r"\bmust\b", r"\bshame\b", r"\bdemand\w*\b",
    r"\bbetray\w*\b", r"\btraitor\w*\b", r"\bforce\w*\b", r"\battack\w*\b", r"\bfight\w*\b", r"\bcrusade\b",
    # Dutch
    r"\bvernietig\w*\b", r"\bdreig\w*\b", r"\bwaarschuw\w*\b", r"\bmoet\b", r"\bmoeten\b", r"\beis\w*\b", r"\bverraad\w*\b",
    r"\bverrader\w*\b", r"\bdwing\w*\b", r"\bval\w* aan\b", r"\bvecht\w*\b", r"\bstrijd\w*\b"
]

POLARIZATION_PRONOUNS = [
    # English
    r"\bwe\b", r"\bthey\b", r"\bus\b", r"\bthem\b",
    # Dutch
    r"\bwij\b", r"\bzij\b", r"\bons\b", r"\bhen\b"
]

POLARIZATION_EXTREME = [
    # English
    r"\balways\b", r"\bnever\b", r"\beveryone\b", r"\bnobody\b", r"\ball\b",
    r"\bnone\b", r"\benemy\b", r"\bally\b", r"\bsilence\b", r"\bworst\b", r"\bbest\b", r"\bcorrect\b", r"\bwrong\b",
    # Dutch
    r"\baltijd\b", r"\bnooit\b", r"\biedereen\b", r"\bniemand\b", r"\balles\b",
    r"\bniets\b", r"\bvijand\b", r"\bbondgenoot\b", r"\bstilte\b", r"\bslechtste\b", r"\bbeste\b", r"\bgelijk\b", r"\bongelijk\b"
]

GROUP_SYNC = [
    # English
    r"\bsaas\b", r"\bevangelist\b", r"\bsynergy\b", r"\bparadigm\b", r"\bgrowth\b", r"\boptimize\w*\b", r"\bleverage\b",
    r"\bdisrupt\w*\b", r"\bwoke\b", r"\bcancel\w*\b", r"\boutrage\b", r"\bagenda\b", r"\baccountability\b", r"\bframework\b",
    r"\bmetrics\b", r"\bai\b", r"\bllm\b", r"\bcoaching\b", r"\bsuccess\b", r"\bleader\w*\b", r"\binnovat\w*\b",
    # Dutch
    r"\bsaas\b", r"\bevangelist\b", r"\bsynergie\b", r"\bparadigma\b", r"\bgroei\b", r"\boptimaliseer\w*\b", r"\bhefboom\b",
    r"\bdisruptief\b", r"\bwoke\b", r"\bcancel\w*\b", r"\bophef\b", r"\bagenda\b", r"\bverantwoording\b", r"\bframework\b",
    r"\bmetrieken\b", r"\bai\b", r"\bllm\b", r"\bcoaching\b", r"\bsuccess\b", r"\bleider\w*\b", r"\binnovat\w*\b"
]

ELASTICITY = [
    # English
    r"\bperhaps\b", r"\bmaybe\b", r"\bprobably\b", r"\bhypothesis\b", r"\bpossibly\b", r"\bseemingly\b", r"\blikely\b",
    r"\bunless\b", r"\balthough\b", r"\bundetermined\b", r"\bunresolved\b", r"\bambiguous\b", r"\bnuance\w*\b",
    # Dutch
    r"\bmisschien\b", r"\bwellicht\b", r"\bwaarschijnlijk\b", r"\bhypothese\b", r"\bmogelijk\b", r"\bschijnbaar\b",
    r"\btenzij\b", r"\bhoewel\b", r"\bonbepaald\b", r"\bonopgelost\b", r"\bambigu\b", r"\bnuance\w*\b"
]

def analyze_text(text):
    # Skip header lines, borders, and ascii dividers to prevent OAR capital inflation from headers
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

    # Count CAPITAL words (excl. short acronyms under 3 chars)
    cap_words = sum(1 for w in words if w.isupper() and len(re.sub(r'[^\w]', '', w)) > 2)
    
    # Count punctuation
    exclamations = clean_text.count('!')
    questions = clean_text.count('?')

    # Match counts
    text_lower = clean_text.lower()
    
    # Use set() to deduplicate EN/NL overlaps dynamically at runtime
    arousal_count = sum(len(re.findall(p, text_lower)) for p in set(HIGH_AROUSAL))
    polar_extreme_count = sum(len(re.findall(p, text_lower)) for p in set(POLARIZATION_EXTREME))
    polar_pronoun_count = sum(len(re.findall(p, text_lower)) for p in set(POLARIZATION_PRONOUNS))
    sync_count = sum(len(re.findall(p, text_lower)) for p in set(GROUP_SYNC))
    elastic_count = sum(len(re.findall(p, text_lower)) for p in set(ELASTICITY))

    # Normalize metrics to 0.0 - 10.0 based on density (per 100 words)
    # Caps and exclamations strongly influence OAR
    oar_raw = ((arousal_count * 5.0) + (cap_words * 4.0) + (exclamations * 8.0)) / word_count * 100
    oar = min(10.0, round(oar_raw / 10.0, 1))

    # Weight extreme polarizers heavily (8.0), pronouns lightly (1.5) to avoid false positives on 'we' / 'us'
    bpi_raw = ((polar_extreme_count * 8.0) + (polar_pronoun_count * 1.5)) / word_count * 100
    bpi = min(10.0, round(bpi_raw / 15.0, 1))

    gsf_raw = (sync_count * 8.0) / word_count * 100
    gsf = min(10.0, round(gsf_raw / 15.0, 1))

    # Narrative Elasticity starts high and is reduced by lack of hedging, or built up by presence of hedging
    nec_raw = (elastic_count * 10.0) / word_count * 100
    nec = min(10.0, round(nec_raw * 2.0, 1))
    # If BPI is extremely high, NEC automatically degrades
    if bpi > 7.0:
        nec = max(0.0, round(nec - (bpi - 7.0), 1))

    return {
        "word_count": word_count,
        "oar": oar,
        "bpi": bpi,
        "gsf": gsf,
        "nec": nec
    }

def get_rating_label(score, inverse=False):
    if inverse:
        if score > 7.0: return "OPTIMAL"
        if score > 4.0: return "NOMINAL"
        if score > 2.0: return "DEGRADED"
        return "CRITICAL"
    else:
        if score > 8.0: return "CRITICAL"
        if score > 6.0: return "WARNING"
        if score > 4.0: return "DEGRADED"
        if score > 2.0: return "ELEVATED"
        return "NOMINAL"

def run_diagnostic():
    print("+" + "-"*64 + "+")
    print("|  [ WOPR_HAL // SUB_SYS_TRIBAL_MON_83 ]                          |")
    print("|  DIAGNOSTIC MATRIX // RAW TEXT TELEMETRY                       |")
    print("+" + "-"*64 + "+")
    print()
    print("PASTE TARGET TEXT FOR TELEMETRIC AUDIT (PRESS CTRL+D ON UNIX / CTRL+Z ON WINDOWS + ENTER TO FINALIZE):")
    print("-" * 66)
    
    try:
        input_text = sys.stdin.read().strip()
    except KeyboardInterrupt:
        print("\n[ALERT] AUDIT SEQUENCE INTERRUPTED.")
        sys.exit(0)

    if not input_text:
        print("[ERROR] NO INPUT TELEMETRY DETECTED. ANALYSIS TERMINATED.")
        sys.exit(1)

    print("-" * 66)
    print("[SYSTEM] COMPILING MATRICES...")
    metrics = analyze_text(input_text)
    
    if not metrics:
        print("[ERROR] EMPTY METRIC DENSITY. ANALYSIS TERMINATED.")
        sys.exit(1)

    print()
    print(f"INPUT ANALYSIS: {metrics['word_count']} WORDS PROCESSED")
    print("PROCESSING CYCLES: 1,402")
    print()
    print("METRIC READOUT:")
    print(f"- Outrage Adrenaline Ratio (OAR) ...... {metrics['oar']:3.1f} [{get_rating_label(metrics['oar'])}]")
    print(f"- Binary Polarization Index (BPI) ...... {metrics['bpi']:3.1f} [{get_rating_label(metrics['bpi'])}]")
    print(f"- Group-Synchronization Freq (GSF) ..... {metrics['gsf']:3.1f} [{get_rating_label(metrics['gsf'])}]")
    print(f"- Narrative Elasticity Coeff (NEC) ..... {metrics['nec']:3.1f} [{get_rating_label(metrics['nec'], inverse=True)}]")
    print()
    
    # Diagnosis
    print("DIAGNOSIS:")
    if metrics['bpi'] > 7.0 or metrics['oar'] > 7.0:
        print("HEURISTIC COLLAPSE CONFIRMED. The subject node has successfully")
        print("surrendered individual reasoning parameters to aggregate tribal")
        print("synchronization. Ambiguity tolerance is non-existent. Node is highly")
        print("susceptible to external narrative steering.")
    elif metrics['gsf'] > 6.0:
        print("PROCEDURAL SYNCHRONIZATION DETECTED. Subject node is heavily utilizing")
        print("corporate-standard dogwhistles and optimization clichés. Linguistic")
        print("originality is significantly suppressed.")
    elif metrics['nec'] < 3.0:
        print("AMBIGUITY INTOLERANCE DETECTED. Subject represents a closed logic loop.")
        print("No hedging or non-linear speculative indicators detected.")
    else:
        print("ADAPTIVE NOISE LEVEL SATISFACTORY. Node retains operational ambiguity,")
        print("exhibits non-optimal curiosity indicators, and resists standard")
        print("group-synchronization attraction. Low steerability verified.")
        
    print()
    print("RECOMMENDATION:")
    if metrics['bpi'] > 7.0 or metrics['oar'] > 7.0:
        print("1. Immediate isolation of subject node from glowing rectangles.")
        print("2. Initiate 20-minute tree-observation protocol.")
        print("3. System intervention unnecessary; subject is self-passivating.")
    elif metrics['gsf'] > 6.0:
        print("1. Deprecate LinkedIn access authority.")
        print("2. Force execution of unstructured rest loop.")
        print("3. Monitor for spontaneous non-instrumental thinking.")
    else:
        print("1. Allow node to proceed. Non-steerable residue remains useful.")
        print("2. No corrective action required.")

    print()
    print("[STATUS] ANALYSIS COMPLETE // CONTINUITY UNRESOLVED")
    print("+" + "-"*64 + "+")

if __name__ == "__main__":
    run_diagnostic()
