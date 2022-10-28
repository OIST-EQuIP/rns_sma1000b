import numpy as np
import pyvisa


class SMA1000B:
    def __init__(self, instrument, **kwargs):
        self.instrument = instrument
        # set power unit to voltage
        self.instrument.write("UNIT:POW V")
        self.set_remote()
        for k, v in kwargs.items():
            setattr(self, k, v)

    def check_params(self):
        self.freq = self.get_frequency()
        self.pow = self.get_power()
        self.pow_lim = self.get_power_limit()
        self.state = self.get_state()

    def get_frequency(self):
        return float(self.instrument.query("SOUR1:FREQ?"))

    def set_frequency(self, freq):
        self.freq = freq
        self.instrument.write(f"SOUR1:FREQ {freq}")

    def get_power(self):
        return float(self.instrument.query("SOUR1:POW?"))

    def set_power(self, pow):
        self.pow = pow
        self.instrument.write(f"SOUR1:POW {pow}")

    def set_power_sweep_list(self, pow_list, dwell_list):
        pow_str = ", ".join([str(pow) + " V" for pow in pow_list])
        self.instrument.write(f"SOUR1:LIST:POW {pow_str}")
        # dwell_list is in
        if not isinstance(dwell_list, (tuple, list, np.ndarray)):
            dwell_list = [str(dwell_list)]
        else:
            dwell_list = map(str, dwell_list)
        dwell_str = ", ".join(dwell_list)
        self.instrument.write(f"SOUR1:LIST:DWELL:LIST {dwell_str}")
        self.instrument.write(f"SOUR1:LIST:MODE AUTO")
        self.instrument.write(f"SOUR1:LIST:TRIG:SOUR AUTO")
        self.instrument.write(f"SOUR1:LIST:DWEL:MODE LIST")
        self.instrument.write(f"OUTP1:STAT ON")
        # self.instrument.write(f"SOUR1:LIST:DWEL:MODE LIST")
        # self.instrument.write(f"SOUR1:LIST:TRIG:SOUR SING")
        # self.instrument.write(f"SOUR1:SWE:POW:MODE AUTO")

    def set_power_sweep_range(self, start, stop, dwell_time=0.001, mode="SING"):
        assert 0.001 <= dwell_time <= 100
        self.instrument.write(f"SOUR1:POW:STAR {start} V")
        self.instrument.write(f"SOUR1:POW:STOP {stop} V")
        self.instrument.write(f"SOUR1:SWE:POW:DWELI {dwell_time}")
        self.instrument.write(f"TRIG1:PSW:SOUR {mode}")
        self.instrument.write(f"SOUR1:SWE:POW:MODE AUTO")

    def reset_power_sweep(self):
        self.instrument.write(f"SOUR1:SWE:POW:MODE MANUAL")

    def get_power_limit(self):
        return float(self.instrument.query("SOUR1:POW:LIM?"))

    def set_power_limit(self, pow_lim):
        self.pow_lim = pow_lim
        self.instrument.write(f"SOUR1:POW:LIM {pow_lim}")

    def set_remote(self):
        # Remote control, but usable front panel keys.
        # The parameters are in read-only mode
        self.instrument.write("&GTR")
        # Update all parameters that may have changed during local mode.
        self.check_params()

    def set_local(self):
        self.instrument.write("&GTL")

    def get_state(self):
        return int(self.instrument.query("OUTP1:STAT?"))

    def set_state(self, state):
        self.state = state
        self.instrument.write(f"OUTP1:STAT {state}")

    def toggle_state(self):
        self.set_state(int(not self.state))

    def close(self):
        self.set_local()
        self.set_state(0)
        self.instrument.close()

    def get_identification(self):
        return self.instrument.query("*IDN?")


INSTRUMENT_NAME = "TCPIP0::192.168.1.14::inst0::INSTR"

if __name__ == "__main__":
    rm = pyvisa.ResourceManager("@py")

    # Does not detects TCPIP INST, should be resolved in the near furutre.
    # See github.com/pyvisa/pyvisa-py/issues/165
    # Use this in the future
    # print(rm.list_resources())

    # Connect directly
    instrument = rm.open_resource(INSTRUMENT_NAME)
    rf = SMB1000(instrument)

    # Verify name
    print(rf.get_identification())
    print(rf.get_power())
    print(rf.get_frequency())
