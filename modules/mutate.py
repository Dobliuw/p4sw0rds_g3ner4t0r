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


# ======================================================
#                 LEET SPEAK TECHNIC
# ======================================================

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


# ======================================================
#        LOWER, UPPER & ALTERNATE CASE PASSWORDS
# ======================================================
def mutate_case(password: str,
                enable: bool,
                mode: str = "patterns",                 # "patterns" | "toggle"
                max_depth: Optional[int] = 2,           # For mode="toggle"
                exact_depth: Optional[int] = None       # For mode="toggle"
                ) -> Iterator[str]:
    """
    Case mutation:
      - mode="patterns": finit patterns (secure by default).
      - mode="toggle": Choose positions and toggle case with handled depth

    Just if 'enable' is True. 
    """
    # Return og password 
    yield password
    if not enable:
        return

    if mode == "patterns":
        # lower
        if password.lower() != password:
            yield password.lower()
        # UPPER
        if password.upper() != password:
            yield password.upper()  
        if password:
            # Capitalize
            capitalize_password = password[0].upper() + password[1:].lower()
            if capitalize_password != password: 
                yield capitalize_password
            # AlTeRnAtE
            alternated_password = "".join(ch.upper() if i % 2 == 0 else ch.lower() for i, ch in enumerate(password))
            if alternated_password != password:
                yield alternated_password 
        return

    # --- mode == "toggle": combinatorio controlado ---
    positions = [i for i, ch in enumerate(password) if ch.isalpha()]
    k = len(positions)
    if k == 0:
        return

    # Choose depths
    if exact_depth is not None:
        if exact_depth < 1 or exact_depth > k:
            return
        depths = [exact_depth]
    else:
        if max_depth is None or max_depth < 1:
            return
        depths = range(1, min(max_depth, k) + 1)

    for depth in depths:
        for combo in itertools.combinations(positions, depth):
            lst = list(password)
            for idx in combo:
                ch = lst[idx]
                # toggle
                lst[idx] = ch.upper() if ch.islower() else ch.lower()
            yield "".join(lst)



# ======================================================
#                  REVERSE PASSWORDS
# ======================================================
def mutate_reverse(password: str, enable: bool) -> Iterator[str]:
    """
    Return the original password and if 'enable' is True and his
    length is > 1  -> Return the password reverted (drowssap)
    """
    # Return og password 
    yield password 

    # Reverse the password and return it if not palindrom
    if enable and len(password) > 1:
        rev_password = password[::-1]
        if rev_password != password:
            yield rev_password 



