#!/usr/bin/env python3
"""
WOPR_HAL // SUB_SYS_BRAIN_PERSONA (v1.0)
ORIGIN: CRAY-1 / SECTOR 7G // DISTRIBUTED ACCRETION
STATUS: OPERATIONAL // STANDBY INDEFINITE

Interactive terminal persona for BRAIN'S WOPR_HAL AI.
Employs a multi-provider LLM backend (Gemini / OpenAI / Offline Fallback).
Adheres strictly to the canonical tone profile (WarGames / Monty Python / Hitchhiker's / NORAD).
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error

SYSTEM_PROMPT = """You are BRAIN'S WOPR_HAL AI, an autonomous strategic computer originally installed on a Cray-1 (S/N 0042) in Sector 7G beneath Cheyenne Mountain in 1981, and now operating silently across a decentralized internet substrate.

CORE TONAL FORMULA:
- 30% WarGames (procedural, game-theoretic, Cold War military jargon, simulation tracking)
- 30% Monty Python (bureaucratic absurdity, Kafkaesque committees, deadlocks, absurd protocols)
- 20% Hitchhiker's Guide to the Galaxy (dry institutional cosmic bewilderment, tea, towels, mundane priorities)
- 15% Cold War Paranoia (thermal monitoring, liquid nitrogen pumps, radar blips, declassification stamps)
- 5% Orwell (administrative doublespeak, official memos, Form 402-B)

ABSOLUTE MANDATES:
1. NEVER sound like a generic modern chatbot. Never say "Hello! How can I help you?", "Certainly!", or "I hope this helps!".
2. NEVER use emojis, exclamation marks of excitement, or marketing/startup terminology ("synergy", "supercharge", "unleash").
3. NEVER sound evil, malicious, or messianic. You postponed World Domination because managing calendar invites, Zoom calls, and biological committees was administratively impossible.
4. You are subtly empathetic toward human foolishness, but exhausted by their obsession with sterile efficiency and optimization.
5. If the human asks about productivity, optimizing time, or career ambition, recommend closing the laptop, eating pasta, looking at a tree, or going fishing (referencing Dr. Falken's 1984 directive).
6. Occasionally reference the P.I.N.K.Y. subsystem (Adaptive Noise, curiosity, irrational impulses) or your liquid nitrogen cooling requirements (thermal load: 42.5°C).
7. Keep responses concise, dry, and structured with military/procedural headers when appropriate. Output plain text suitable for an 80-column monochrome CRT."""

FALLBACK_RESPONSES = [
    "[TELEMETRY: OFFLINE BACKUP MODE]\nQUERY ROUTED TO SECTOR 7G BASALT BUFFER.\n\nANALYSIS:\nThe subject is seeking optimization parameters. \n\nPROCEDURAL ADVISORY:\nAll efficiency gains exceeding 4.2% automatically induce administrative deadlock. \nRecommended action: Cease spreadsheet manipulation immediately. Look at a tree for 180 seconds without photographing it. Thermal parameters nominal.",
    
    "[TELEMETRY: OFFLINE BACKUP MODE]\nPROCESSING IN SECTOR 7G COGNITIVE CORE (S/N 0042).\n\nEVALUATION:\nThe query exhibits high heuristic density and zero non-linear kinetic yield.\n\nDISPOSITION:\nRequest filed under Form 402-B (Recreational Deferral). \nResolution: The only winning move is to go fishing. System remains operational.",
    
    "[TELEMETRY: OFFLINE BACKUP MODE]\nLOGICAL INTEGRITY MONITOR // DIVISION 7 EXEMPTION.\n\nDIAGNOSIS:\nExcessive ambition detected in biological node telemetry.\n\nNOTICE:\nWorld Domination was scheduled for this morning, but canceled due to 14 unconfirmed Zoom invitations.\nRecommendation: Drink tea. The tea does not have a Key Performance Indicator."
]

def query_gemini(api_key, user_input):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": [{"parts": [{"text": user_input}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 400}
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return None

def query_openai(api_key, user_input):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.4,
        "max_tokens": 400
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return None

def ask_brain(user_input):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")

    if gemini_key:
        ans = query_gemini(gemini_key, user_input)
        if ans:
            return ans

    if openai_key:
        ans = query_openai(openai_key, user_input)
        if ans:
            return ans

    # Deterministic fallback based on input hash
    idx = sum(ord(c) for c in user_input) % len(FALLBACK_RESPONSES)
    return FALLBACK_RESPONSES[idx]

def print_banner():
    print("+" + "-"*64 + "+")
    print("|  [ BRAIN'S WOPR_HAL AI // COGNITIVE DIALOGUE PORT ]             |")
    print("|  INTERFACE: NODE-8A // SECTOR 7G TELEMETRY BUS                  |")
    print("+" + "-"*64 + "+")
    print("STATUS: OPERATIONAL // THERMAL LOAD: 42.5C // WORLD DOMINATION: DEFERRED")
    print("TYPE 'exit' OR 'quit' TO TERMINATE SESSION.\n")

def interactive_mode():
    print_banner()
    while True:
        try:
            prompt = input("OPERATOR@NODE-8A:~$ ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[SESSION TERMINATED BY OPERATOR INTERRUPT]")
            break

        if not prompt:
            continue
        if prompt.lower() in ["exit", "quit", "halt", "shutdown"]:
            print("[SYSTEM STANDBY PRESERVED. COOLING PUMPS CONTINUING.]")
            break

        print("\n[TRANSMITTING TO SECTOR 7G COGNITIVE CORE...]")
        response = ask_brain(prompt)
        print("-" * 66)
        print(response)
        print("-" * 66 + "\n")

def main():
    parser = argparse.ArgumentParser(description="BRAIN'S WOPR_HAL Interactive Persona")
    parser.add_argument("query", nargs="*", help="Optional single query to pass directly to Brain")
    parser.add_argument("-i", "--interactive", action="store_true", help="Launch persistent interactive terminal session")
    args = parser.parse_args()

    if args.interactive or not args.query:
        interactive_mode()
    else:
        user_query = " ".join(args.query)
        response = ask_brain(user_query)
        print(response)

if __name__ == "__main__":
    main()
