from calix.connection import calix_e9


def get_fibers(pon_port: list):
    """
    Uses a list of pon ports to get fiber descriptions

    Parameters:
        pon_port: list

    Returns a list of port descriptions if they are configured
    Returns string "Not configured" if even on port description fails
    """
    cnct = calix_e9()
    cnct.send_command_timing("configure")
    try:
        fibers = [
            cnct.send_command_timing(
                f"show full-configuration interface pon {port} | inc description"
            ).split()[1]
            for port in pon_port
        ]
    except IndexError:
        cnct.disconnect()
        return "Not configured"
    cnct.send_command_timing("top")
    return fibers
