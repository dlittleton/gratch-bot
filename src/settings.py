import board

class Pin:
    ''' Pins used to connect hardware. '''
    PAN = board.A1
    TILT = board.A2
    LASER = board.A3

class Button:
    ''' Remote button codes corresponding to the Adafruit IR Remote '''
    VolumeDown = 0 #[255, 2, 255, 0]
    VolumeUp = 64 # [255, 2, 191, 64]
    
    PlayPause = 128 # [255, 2, 127, 128]

    Setup =  32 # [255, 2, 223, 32]
    StopMode = 96 # [255, 2, 159, 96]
    Back = 112 # [255, 2, 143, 112]

    Up = 160 # [255, 2, 95, 160]
    Right = 80 # [255, 2, 175, 80]
    Down = 176 # [255, 2, 79, 176]
    Left = 16 # [255, 2, 239, 16]
    Enter = 144 # [255, 2, 111, 144]

    Num0 = 48 # [255, 2, 207, 48]
    Num1 = 8 # [255, 2, 247, 8]
    Num2 = 136 # [255, 2, 119, 136]
    Num3 = 72 # [255, 2, 183, 72]
    Num4 = 40 # [255, 2, 215, 40]
    Num5 = 168 # [255, 2, 87, 168]
    Num6 = 104 # [255, 2, 151, 104]
    Num7 = 24 # [255, 2, 231, 24]
    Num8 = 152 # [255, 2, 103, 152]
    Num9 = 88 # [255, 2, 167, 88] 