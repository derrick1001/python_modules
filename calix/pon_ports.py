from calix.fibers import get_fibers
from calix.ont_detail import ont


def get_pon_fibers(ont_ids: list, e9: str):
    """
    Gets linked-pon for each ont id

    Parameters:
        ont_ids: list
        e9: str

    Returns tuple(Generator) object
    """
    for id in ont_ids.copy():
        try:
            ont(e9, id).get("linked-pon")
        except AttributeError:
            print(f"{id} does not exist and was removed")
            ont_ids.remove(id)
    pon_ports = [ont(e9, id).get("linked-pon") for id in ont_ids]
    fibers = (fiber for fiber in get_fibers(pon_ports))
    pon_ports = (port for port in pon_ports)
    return pon_ports, fibers
