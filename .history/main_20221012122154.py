import pyvisa

instrument_IP = "192.168.1.14"


def get_instrument():
    rm = pyvisa.ResourceManager("@py")

    # Does not detects TCPIP INST, should be resolved in the near furutre.
    # See github.com/pyvisa/pyvisa-py/issues/165
    # Use this in the future
    # print(rm.list_resources())

    # Connect directly
    instrument = rm.open_resource(f"TCPIP0::{instrument_IP}::inst0::INSTR")

    return instrument


if __name__ == "__name__":
    print(get_instrument())
