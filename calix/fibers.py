from calix.connection import calix_e9


def get_fibers(pon_port: list):
    cnct = calix_e9()
    cnct.send_command_timing("configure")
    fibers = (
        cnct.send_command_timing(
            f"show full-configuration interface pon {port} | inc description"
        ).split()[1]
        for port in pon_port
    )
    cnct.send_command_timing("top")
    return fibers
