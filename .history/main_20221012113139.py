import pyvisa

# does not detects TCPIP INST
# github.com/pyvisa/pyvisa-py
rm = pyvisa.ResourceManager("@ivi")
print(rm.list_resources())
