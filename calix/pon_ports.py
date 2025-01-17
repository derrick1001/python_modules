from calix.ont_detail import ont

# NOTE: Takes in a list of ont_ids and e9 to get linked pon attribute


def get_pon_ports(ont_ids: list, e9: str):
    pon_ports = [ont(e9, id).get("linked-pon") for id in ont_ids if id is not None]
    return pon_ports
