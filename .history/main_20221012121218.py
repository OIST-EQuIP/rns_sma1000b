import pyvisa

instrument_IP = "192.168.1.14"


def connect_instrument():
    # Does not detects TCPIP INST, should be resolved in the near furutre.
    # See github.com/pyvisa/pyvisa-py/issues/165
    # Use this in the future to allow for connections other than TCP/IP
    rm = pyvisa.ResourceManager("@py")
    print(rm.list_resources())

    # Connect directly
    f"TCPIP0::{instrument_IP}::inst0::INSTR"
