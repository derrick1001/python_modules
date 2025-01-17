from calix.connection import calix_e9

# Make a list comp of port descriptions
# Order is important, if any IndexError, return None
# Convert to generator comp and return


def get_fibers(pon_port: list):
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
    fibers = (fiber for fiber in fibers)
    return fibers
