def make_range(v, delta):
    return range(v - delta, v + delta)

nec_delta = 100 
nec_start = make_range(9000, nec_delta)
nec_start_space = make_range(4500, nec_delta)
nec_repeat_space = make_range(2250, nec_delta)
nec_signal = make_range(562, nec_delta)
nec_long_signal = make_range(562 * 3, nec_delta)

class State:
    ''' Enum for decoder states. '''
    # Initial state, waiting for start pulse
    Initial = 1
    
    # Start pulse received, waiting for repeat or signal start
    Start = 2
    
    # Repeat space received, waiting for mark
    Repeat = 3
    
    # In signal, waiting for mark
    Signal_Mark = 4
    
    # In signal, waiting for space
    Signal_Space = 5
    
    
class NecRemote:
    ''' State machine based decoder for Nec Remote Codes 
    
    - Addresses are ignored.
    - Handles repeat signals
    - Verifies command and inverse match
    '''
    
    
    def __init__(self, pulse_in):
        self.pulse = pulse_in
        self.reset()
        
        
    def poll(self):
        ''' Check for a received signal.
        
        Will return command code if a signal is received or None otherwise.
        
        If a repeat signal is received immediately after a command, the previous
        command is returned again.
        '''
        
        while self.pulse:
            current = self.pulse.popleft()
            
            if self.state == State.Initial:
                if current in nec_start:
                    self.state = State.Start
            
            elif self.state == State.Start:
                if current in nec_start_space:
                    self.state = State.Signal_Mark
                elif current in nec_repeat_space:
                    self.state = State.Repeat
                else:
                    self.reset()
                
                
            elif self.state == State.Repeat:
                if current in nec_signal:
                    self.reset(clear_last=False)
                    return self.last_button
                else:
                    self.reset()                  
                
            elif self.state == State.Signal_Mark:
                if current in nec_signal:
                    self.state = State.Signal_Space
                else:
                    self.reset()
                    
            elif self.state == State.Signal_Space:
                if not (current in nec_signal or current in nec_long_signal):
                    self.reset()
                else:
                    self.value = (self.value << 1)
                    if current in nec_long_signal:
                        self.value |= 1
                    self.nbits += 1
                    self.state = State.Signal_Mark
                    
                if self.nbits == 32:
                    # Command is now complete
                    b = self.value.to_bytes(4, 0)
                    if b[2] ^ b[3] == 255:
                        self.last_button = b[2]
                        self.reset(clear_last=False)
                        return self.last_button
                    else:
                        self.reset()
        
        
    def reset(self, clear_last=True):
        self.state = State.Initial
        self.nbits = 0
        self.value = 0
        
        if clear_last:
            self.last_button = None
            
    
    def clear_last_button(self):
        ''' Clears the last pressed button to prevent repeats.

        Useful if a particular command should not be automatically repeated.
        '''
        self.last_button = None