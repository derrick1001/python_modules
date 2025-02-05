from crayon import c_BLUE, c_WHITE


def ssp():
    """
    This function is used to get shelf/slot/port
    information for use with other programs

    Parameters
        n/a

    Returns 3 element tuple
    """
    shelf = input(f"{c_BLUE}Shelf: {c_WHITE}")
    slot = input(f"{c_BLUE}Slot: {c_WHITE}")
    port = input(f"{c_BLUE}Port: {c_WHITE}")
    return shelf, slot, port
