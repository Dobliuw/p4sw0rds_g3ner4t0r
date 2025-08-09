import argparse
import os, sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from modules.tokens import parse_words, base_passwords
from modules.mutate import mutate_pipeline
from modules.lengths import adjust_to_lengths
from io_utils.writer import stream_write
from typing import List

def build_completion_charset(words: List[str], extra_chars: str, include_words_chars: bool = True) -> str:
    """
    Construye el charset final de completado:
    - Si include_words_chars=True, agrega primero caracteres únicos que aparecen en las palabras (-w)
    - Luego agrega los de -c, evitando duplicados
    - Mantiene el orden de aparición (importa para el orden de generación)
    """
    seen = set()
    out = []

    if include_words_chars:
        for w in words:
            for ch in w:
                if ch not in seen:
                    seen.add(ch)
                    out.append(ch)

    for ch in extra_chars:
        if ch not in seen:
            seen.add(ch)
            out.append(ch)

    return ''.join(out)


def main():
    parser = argparse.ArgumentParser(description="P4sw0rds G3ner4t0r")
    parser.add_argument("-w", "--words", required=True, help="Words separated by comma (,)")
    parser.add_argument("-l", "--length", type=int, required=True, help="Each password Length ([!] Use --base-length to set min length and have password from length 8 to -l 12)")
    parser.add_argument("-bl", "--base-length", type=int, help="Set a min length to have more credentials (Recommended 8). DON'T USE THIS FLAG IF YOU KNOW THE PASSWORD LENGTH SEARCHED")
    parser.add_argument("-c", "--characters", default="", help="Extra characters to complete the password length (E.g. -w dobliuw -c 123 -l 9 -> dobliuw123)")
    parser.add_argument("--complete-chars", "--complete-characters", default=False, action="store_true", help="Complete the characters to fill length with the characters contained for each word used (E.g. If you use -w dobliuw,owen and -c 123 the final list of chars to fill the length desired will be owendbliu123)")
    parser.add_argument("-o", "--output", required=True, help="Path to save password into .txt")
    parser.add_argument("--preview", type=int, default=0, help="Show the first N passwords in output")

    # Mutations flags
    parser.add_argument("--leet", action="store_true", default=False, help="Use 'LEET SPEAK' technique (E.g. dobliuw, d0bl1uw, d0bl!uw)")
    parser.add_argument("--leet-policy", choices=["max", "full", "exact"], default="max")
    parser.add_argument("--leet-max-depth", type=int, default=2)
    parser.add_argument("--leet-exact-depth", type=int)

    parser.add_argument("--alup", action="store_true", default=False, help="Use 'Alternate, UPERCASE, lowercase and AltErNaTE technique (E.g. dobliuw -> Dobliuw, DOBLIUW, dobliuw, DoBlIuW)")
    parser.add_argument("--alup-mode", choices=["patterns", "toggle"], default="patterns")
    parser.add_argument("--alup-max-depth", type=int, default=2)
    parser.add_argument("--alup-exact-depth", type=int)

    parser.add_argument("--reverse", action="store_true", default=False, help="Use 'REVERSE' technique (E.g. dobliuw -> wuilbod)")

    parser.add_argument("--typoswap", action="store_true", default=False, help="Use 'TYPO SWAP technique (E.g. dobliuw -> douwbli)")
    parser.add_argument("--typo-max-swaps", type=int, default=1)

    args = parser.parse_args()

    # Generate base passwords
    words = parse_words(args.words)
    passwords = base_passwords(words)


    # Resolve target lengths
    if args.base_length:
        if args.length < args.base_length:
            # Normalize
            lo, hi = sorted((args.base_length, args.length))
        else:
            lo, hi = args.base_length, args.length
        target_lengths = list(range(lo, hi + 1))

    else:
        target_lengths = [args.length]
    
    # FInal charset priorized
    completion_charset = build_completion_charset(words, args.characters, include_words_chars=args.complete_chars)

    # Complete to lengths (With -c)
    prefilled = adjust_to_lengths(passwords, target_lengths, completion_charset)

    # Pipeline
    gen = mutate_pipeline(
        prefilled,
        leet=args.leet,
        leet_policy=args.leet_policy,
        leet_max_depth=args.leet_max_depth,
        leet_exact_depth=args.leet_exact_depth,
        alup=args.alup,
        alup_mode=args.alup_mode,
        alup_max_depth=args.alup_max_depth,
        alup_exact_depth=args.alup_exact_depth,
        reverse=args.reverse,
        typoswap=args.typoswap,
        typo_max_swaps=args.typo_max_swaps
    )

    # Write the passwords in real time
    total = stream_write(gen, args.output, preview=args.preview)
    print(f"[+] {total} passwords generated in -> {args.output}")

if __name__ == "__main__":
    main()

