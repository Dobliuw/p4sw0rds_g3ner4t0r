from typing import List 

def resolve_final_length(length: int, min_length: int, base_passwords: bool, warning: bool) -> List[int]:
    """
    - By default only generate an exactly 'length'.
    - If 'base_passwords' -> We generate all passwords from 'min_length' to 'length'. 
    - If 'length' < 'min_length' & '!warning' -> Elevate 'min_length'
    - If 'length' < 'min_length' & 'warning' -> We respect what has been requested by flags.
    """
    # The -l flag is mandatory.
    if length is None: 
        raise ValueError("You should indicate -l / --length")

    # Set the min length to 8
    if min_length < 1:
        min_length = 8

    used_length = length 

    # Elevate the 'length' to 'min_length'
    if length < min_length and not warning:
        print(f"[i] length={length} < min_length={min_length}. Using {min_length}\n\tUse --warning to force less.")
        used_length = min_length 

    # Respect what the user set 
    if base_passwords:
        start, end = sorted((min_length, used_length))
        return list(range(start, end + 1))
    else: 
        return [used_length]
        
