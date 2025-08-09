import itertools
from typing import Iterable, Iterator, List

def adjust_to_lengths(tokens: Iterable[str],
                      lengths: List[int],
                      charset: str) -> Iterator[str]:
    """
    For each token:
      - if len == L -> yield as-is
      - if len <  L -> complete with product(charset, missing)
      - if len >  L -> skip for that L
    WARNING: |charset|^(missing) could explote!!!! BOOM!!!.
    """
    for tok in tokens:
        lt = len(tok)
        for L in lengths:
            if lt > L:
                continue
            if lt == L:
                yield tok
            else:
                missing = L - lt
                if not charset:
                    continue
                for suf in itertools.product(charset, repeat=missing):
                    yield tok + ''.join(suf)

