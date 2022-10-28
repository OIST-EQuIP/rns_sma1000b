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

    def set_sweep_list(
        self, freq_list=None, pow_list=None, dwell_list=0.001, repeat=False
    ):
        if not freq_list and not pow_list:
            return

        # use a temporary file for storing the list
        self.instrument.write("SOUR1:LIST:SEL '/var/user/tmp.lsw'")

        if freq_list:
            assert 5e-3 <= min(freq_list)
            assert max(freq_list) <= 5e-9
            freq_str = ", ".join([str(freq) + "Hz" for freq in freq_list])
        else:
            freq_str = ", ".join([str(self.freq) + "Hz"] * len(pow_list))
        self.instrument.write(f"SOUR1:LIST:FREQ {freq_str}")

        # pow_list needs to be converted into dbm
        pow_list_dBm = 10 * np.log10(np.power(pow_list, 2) * 1000 / 50)
        assert -145 <= min(pow_list_dBm)
        assert -max(pow_list_dBm) <= 36
        pow_str = ", ".join([str(pow) + "dBm" for pow in pow_list_dBm])
        self.instrument.write(f"SOUR1:LIST:POW {pow_str}")

        # dwell_list needs to be converted into us
        if not isinstance(dwell_list, (tuple, list, np.ndarray)):
            assert 0.001 <= dwell_list <= 100
            dwell_str = str(dwell_list * 1e6)
        else:
            assert 0.001 <= min(dwell_list)
            assert max(dwell_list) <= 100
            dwell_list = np.array(dwell_list) * 1e6
            dwell_str = ", ".join([map(str, dwell_list)])
        self.instrument.write(f"SOUR1:LIST:DWELL:LIST {dwell_str}")

        self.instrument.write(f"SOUR1:LIST:MODE AUTO")
        self.instrument.write(f"SOUR1:FREQ:MODE LIST")
        self.instrument.write(f"SOUR1:LIST:DWEL:MODE LIST")
        if repeat:
            self.instrument.write(f"SOUR1:LIST:TRIG:SOUR AUTO")
        else:
            self.instrument.write(f"SOUR1:LIST:TRIG:SOUR SING")

    def set_power_sweep_range(self, start, stop, dwell_time=0.001, repeat=False):
        assert 0.001 <= dwell_time <= 100
        self.instrument.write(f"SOUR1:POW:STAR {start} V")
        self.instrument.write(f"SOUR1:POW:STOP {stop} V")
        self.instrument.write(f"SOUR1:SWE:POW:DWELI {dwell_time}")
        self.instrument.write(f"SOUR1:SWE:POW:MODE AUTO")
        if repeat:
            self.instrument.write(f"TRIG1:PSW:SOUR AUTO")
        else:
            self.instrument.write(f"TRIG1:PSW:SOUR SING")

    def start_sweep(self):
        pass

    def stop_sweep(self):
        self.instrument.write(f"SOUR1:FREQ:MODE CW")
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
