from typing import Generator

from calix.ont_detail import ont

# Takes in a list of ont_ids and e9 to get linked pon attribute
# TODO: working on taking in generator object of lists of ont ids


def get_pon_ports(ont_ids: list, e9: str):
    if isinstance(ont_ids, Generator):
        for lst_ids in ont_ids:
            pon_ports = [
                ont(e9, id).get("linked-pon") for id in lst_ids if id is not None
            ]
    else:
        pon_ports = [ont(e9, id).get("linked-pon") for id in ont_ids if id is not None]
    return pon_ports
