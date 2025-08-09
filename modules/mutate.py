import itertools
from typing import Iterator, Optional

# Replaces to do with Leet Speak
_LEET = {
    'a': ['4', '@'], 'A': ['4', '@'],
    'e': ['3'],       'E': ['3'],
    'i': ['1', '!'],  'I': ['1', '!'],
    'o': ['0'],       'O': ['0'],
    's': ['5', '$'],  'S': ['5', '$'],
    't': ['7'],       'T': ['7']
}

def _variants_for_char(ch: str):
    variants = _LEET.get(ch)
    if variants is None:
        return None
    return variants if isinstance(variants, (list, tuple)) else [variants]


def mutate_leet(password: str,
                policy: str = "max",                  # "max" | "full" | "exact"
                max_depth: Optional[int] = 2,         # Used if policy == "max"
                exact_depth: Optional[int] = None     # Used if policy == "exact"
                ) -> Iterator[str]:
    """
    Generate variations in leet replacing positions.

    Policies:
      - policy == "max"  -> generate depths 1..min(max_depth, k)
      - policy == "full" -> generate depths 1..k
      - policy == "exact"-> generate only depth == exact_depth
    Where k = count of replaceable positions in 'password'.

    Notes:
      - If max_depth is None and policy == "max", no variants are produced
        (use policy == "full" if you want full depth).
      - Always yields the original password first.
    """
    # Yield original password
    yield password

    # Find replaceable positions and their variants
    positions = []
    for idx, ch in enumerate(password):
        vs = _variants_for_char(ch)
        if vs:
            positions.append((idx, vs))

    k = len(positions)
    if k == 0:
        return

    # Decide depths according to policy
    if policy == "full":
        depths = range(1, k + 1)

    elif policy == "exact":
        if exact_depth is None or exact_depth < 1 or exact_depth > k:
            return
        depths = [exact_depth]

    else:  # default "max"
        if max_depth is None or max_depth < 1:
            return
        depths = range(1, min(max_depth, k) + 1)

    # Generate combinations for each depth
    for depth in depths:
        # Choose which positions to replace (combinations of length = depth)
        for combo in itertools.combinations(positions, depth):
            idxs = [c[0] for c in combo]
            choices_per_pos = [c[1] for c in combo]  # variants per chosen position

            # For the chosen positions, try all variant combinations
            for repl_tuple in itertools.product(*choices_per_pos):
                leet_password = list(password)
                for idx, new_ch in zip(idxs, repl_tuple):
                    leet_password[idx] = new_ch
