from typing import Generator

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
    pon_ports: list = [
        ont(e9, id).get("linked-pon") for id in ont_ids if id is not None
    ]
    fibers: Generator = (fiber for fiber in get_fibers(pon_ports))
    pon_ports: Generator = (port for port in pon_ports)
    return pon_ports, fibers
