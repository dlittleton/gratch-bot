from adafruit_irremote import GenericDecode, IRNECRepeatException, IRDecodeException

class NecRemote:
    
    def __init__(self, pulse_in):
        self.pulse_in = pulse_in
        self.decoder = GenericDecode()
        self.last_button = None
        self.nfailed = 0
        
        
    def _wait_for_start(self):
        while self.pulse_in and not 9000 <= self.pulse_in[0] <= 10000:
            self.pulse_in.popleft()
    
    def poll(self):
        pulse = None
        self._wait_for_start()
        if len(self.pulse_in) > 2:
            print(self.pulse_in[0], self.pulse_in[1])
            pulse = self.decoder.read_pulses(self.pulse_in, pulse_window=0.01)
        if pulse is None:
            return None
            
        print(pulse)
            
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
            self.nfailed += 1
            
        return None
        
        
    def clear_last_button(self):
        ''' Clears the last pressed button to prevent repeats.
        
        Useful if a particular command should not be automatically repeated.
        '''
        self.last_button = None
        
    