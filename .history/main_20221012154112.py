import pyvisa


class SMB1000:
    def __init__(self, instrument, **kwargs):
        self.instrument = instrument
        # set power unit to voltage
        self.instrument.write("UNIT:POW V")
        self.set_remote()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def check_params(self):
        self.pow_lim = self.get_power_limit()
        self.pow_lim = self.get_power_limit()

    def get_frequency(self):
        pass

    def set_frequency(self):
        pass

    def get_power(self):
        pass

    def set_power(self):
        pass

    def get_power_limit(self):
        return float(instrument.query("SOUR1:POW:LIM?"))

    def set_power_limit(self, pow_lim):
        self.pow_lim = pow_lim
        instrument.write(f"SOUR1:POW:LIM {pow_lim}")

    def set_remote(self):
        # Remote control, but usable front panel keys.
        # The parameters are in read-only mode
        instrument.write("&GTR")
        self.check_params()

    def set_local(self):
        self.instrument.write("&GTL")

    def close(self):
        self.set_local()
        self.instrument.close()

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

    rf.set
