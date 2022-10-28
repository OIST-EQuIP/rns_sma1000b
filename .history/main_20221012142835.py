import pyvisa


class SMB1000:
    def __init__(self, instrument, **kwargs):
        self.instrument = instrument
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_frequency(self):
        pass

    def set_frequency(self):
        pass

    def get_voltage_amplitude(self):
        pass

    def set_voltage_amplitude(self):
        pass

    def set_remote(self):
        # Remote control, but usable front panel keys.
        # The parameters are in read-only mode
        instrument.write("&GTR")

    def set_local(self):
        instrument.write("&GTL")

    def get_identification(self):
        return instrument.query("*IDN?")


INSTRUMENT_IP = "192.168.1.14"

if __name__ == "__main__":
    rm = pyvisa.ResourceManager("@py")

    # Does not detects TCPIP INST, should be resolved in the near furutre.
    # See github.com/pyvisa/pyvisa-py/issues/165
    # Use this in the future
    # print(rm.list_resources())

    # Connect directly
    instrument = rm.open_resource(f"TCPIP0::{INSTRUMENT_IP}::inst0::INSTR")
    rf = SMB1000(instrument)

    # Verify name
    print(rf.get_identification())
