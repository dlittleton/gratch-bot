from adafruit_irremote import GenericDecode, IRNECRepeatException, IRDecodeException

class NecRemote:
    
    def __init__(self, pulse_in):
        self.pulse_in = pulse_in
        self.decoder = GenericDecode()
        self.last_button = None
        self.nfail = 0
        
        
    def poll(self):
        pulse = self.decoder.read_pulses(self.pulse_in, pulse_window=0.01, blocking=False)
        if pulse is None:
            return None
            
        try:
            value = self.decoder.decode_bits(pulse)
            if len(value) == 4 and value[2] ^ value[3] == 255:
                self.last_button = value[3]
                return self.last_button
            else:
                self.last_button = None
                
        except IRNECRepeatException:
            return self.last_button
        except IRDecodeException:
            self.last_button = None
            self.nfail += 1
            
        return None
        
    