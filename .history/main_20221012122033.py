import pyvisa

instrument_IP = "192.168.1.14"


def connect_instrument():
    rm = pyvisa.ResourceManager("@py")

    # Does not detects TCPIP INST, should be resolved in the near furutre.
    # See github.com/pyvisa/pyvisa-py/issues/165
    # Use this in the future
    # print(rm.list_resources())

    # Connect directly
    rm.open_resource(f"TCPIP0::{instrument_IP}::inst0::INSTR")


if __name__ is "__name__":
    print(connect_instrument())
