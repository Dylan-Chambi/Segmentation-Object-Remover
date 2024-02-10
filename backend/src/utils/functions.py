

def human_size(bytes: int, units: list[str] = [' bytes','KB','MB','GB','TB', 'PB', 'EB']) -> str:
    """ Returns a human readable string representation of bytes """
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:])