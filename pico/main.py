from machine import ADC, Pin
from time import sleep
import sys


buttons = [21]
button_pressed_state = False

selectors = [[0, 1, 2, 3], [4, 5, 6, 7]] # selector pins [[<pin_selector1_state1>, <pin_selector1_state2>, <pin_selector1_state3>, ...], [<pin_selector2_state1>, ...], ...]
selector_selection_state = False # what the state of the selector swich pin has to be for it to be registered as selected. Boolean.

pots = [26, 27, 28] # potentiometer pins [<pin_pot1>, <pin_pot2>, <pin_pot3>, ...]
pot_range = [13000, 65500] # value range [<0% value>, <100% value>]

dev_identifier = "3273e2cefa50a16eafefca053ba87625"




def get_button_states():
    """
    Reads the values of selector switches connected to the pins in 'selectors'.
    Returns a list of lists with the first value being the current state of each selector switch and the second value being the highest state that selector switch can become, 0 being the first state.
    """
    state_list = []
    for button in buttons:
        pin = Pin(button, Pin.IN, Pin.PULL_UP) # read if pin is True or False
        
        state = pin.value() # Read pin state into var
        if button_pressed_state == False: # Invert if False is the pressed state.
            state = not state
            
        state_list.append(int(state)) # convert bool to int so that serial output is less cloged. Reason: str(bool) => "True" and "False".
    return state_list


def get_selector_states():
    """
    Reads the values of selector switches connected to the pins in 'selectors'.
    Returns a list of lists with the first value being the current state of each selector switch and the second value being the highest state that selector switch can become, 0 being the first state.
    """
    state_list = []
    for selector in selectors:
        for state in range(len(selector)): # range(len(selector)) is used so the state counter always starts from 0 to n.
            pin = Pin(selector[state], Pin.IN, Pin.PULL_UP) # read if pin is True or False
            if pin.value() == selector_selection_state:
                state_list.append([state, len(selector) - 1])
                break
    return state_list


def get_pot_values():
    """
    Reads the values of potentimeters connected to the pins in 'pots'.
    Returns a list with the values of each pot, ranging from 0 - 100%. 0% and 100% are defined by 'pot_range'.
    """
    value_list = []
    for pin in pots:
        pot_value = ADC(pin).read_u16() # read value from pin
        
        if pot_value < pot_range[0]: # clip off at min value if required
            pot_value = pot_range[0]
        if pot_value > pot_range[1]: # clip off at max value if required
            pot_value = pot_range[1]
        pot_value = pot_value - pot_range[0] # adjust pot_value to zero
        
        pot_pct = 100 / (pot_range[1] - pot_range[0]) * pot_value # turn into %
        
        value_list.append(pot_pct)
    return value_list




while True: # main loop
    button_states = get_button_states()
    selector_states = get_selector_states()
    pot_values = get_pot_values()
    
    sys.stdout.write("Device: " + dev_identifier + ";    Buttons: " + str(button_states) + ";    Selectors: " + str(selector_states) + ";    Pots: " + str(pot_values) + ";\r") # Output to serial console. ';' is the delimiter
