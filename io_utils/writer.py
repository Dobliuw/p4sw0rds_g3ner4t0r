import os
from typing import Iterable

def stream_write(gen: Iterable[str],
                 out_path: str,
                 preview: int = 0,
                 chunk_size: int = 50_000) -> int:
    """
    Write the credentials as they are generated.
    - preview: Show the first 'N' password in terminal (1..100 recomended).
    - chunk_size: How many lines to buffer before dumping to disk.
    CTRL + C Handle.
    """
    # Create the directory inserted by user if does not exist.
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    total = 0
    shown = 0
    buf = []
    do_preview = 1 <= preview <= 100

    try:
        with open(out_path, "w", encoding="utf-8", buffering=1024*1024) as f:
            for pwd in gen:
                total += 1

                if do_preview and shown < preview:
                    print(pwd)
                    shown += 1

                buf.append(pwd)
                if len(buf) >= chunk_size:
                    f.write(''.join(p + '\n' for p in buf))
                    buf.clear()
    except KeyboardInterrupt:
        # Flush what we have in buffer and re-raise
        try:
            if buf:
                with open(out_path, "a", encoding="utf-8", buffering=1024*1024) as f:
                    f.write(''.join(p + '\n' for p in buf))
                    buf.clear()
        finally:
            raise
    else:
        # Final flush
        if buf:
            with open(out_path, "a", encoding="utf-8", buffering=1024*1024) as f:
                f.write(''.join(p + '\n' for p in buf))
                buf.clear()

    return total

