import itertools 
from typing import Iterator, List 

def parse_words(raw: str) -> List[str]:
    return [w.strip() for w in raw.split(",") if w.strip()]

def base_passwords(words: List[str], max_concat_depth: int = 2) -> Iterator[str]:
    """
    Generate base passwords: Each word + concatenations (2 of depth).
    Avoid trivial duplicates.
    """
    seen = set()

    for w in words:
        # If the password was not added, add it 
        if w and w not in seen:
            seen.add(w); yield w


    for r in range(2, max_concat_depth + 1):
        """
        If the user insert -w fit,sport,marquez -> firsport, sportmarquez, marquezfit, sportfit, etc.
        """
        # Concatenate the words with 2 of depth
        for tup in itertools.permutations(words, r):
            unification = "".join(tup)
            if unification not in seen: 
                seen.add(unification); yield unification


