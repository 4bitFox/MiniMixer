from machine import ADC, Pin
from time import sleep
import sys


buttons = [
    [21, {"pressed_state": False}]
    ] # [[<pin>, {"pressed_state": <bool>}], [...], ...]

selectors = [
    [[4, 5, 6, 7], {"selected_state": False}],
    [[0, 1, 2, 3], {"selected_state": False}]
    ] # [[[<pin1>, <pin2>, ...], {"selected_state": <bool>}], [...], ...]

pots = [
    [26, {"min": 13500, "max": 65000, "log": True, "log_base": 10}],
    [27, {"min": 13500, "max": 65000, "log": True, "log_base": 10}],
    [28, {"min": 13500, "max": 65000, "log": True, "log_base": 10}]
    ] # [[<pin_pot1>, {"min": <min value>, "max": <max value>, "log": <bool>, "log_base": <if "log": True => log base value; else => no need to specify>}], [...], ...]

dev_identifier = "3273e2cefa50a16eafefca053ba87625"

    



def get_button_states():
    """
    Reads the values of selector switches connected to the pins in 'selectors'.
    Returns a list of lists with the first value being the current state of each selector switch and the second value being the highest state that selector switch can become, 0 being the first state.
    """
    state_list = []
    for button, props in buttons:
        pin = Pin(button, Pin.IN, Pin.PULL_UP) # read if pin is True or False
        
        state = pin.value() # Read pin state into var
        if props["pressed_state"] == False: # Invert if False is the pressed state.
            state = not state
            
        state_list.append(int(state)) # convert bool to int so that serial output is less cloged. Reason: str(bool) => "True" and "False".
    return state_list


def get_selector_states():
    """
    Reads the values of selector switches connected to the pins in 'selectors'.
    Returns a list of lists with the first value being the current state of each selector switch and the second value being the highest state that selector switch can become, 0 being the first state.
    """
    state_list = []
    for selector, props in selectors:
        for state in range(len(selector)): # range(len(selector)) is used so the state counter always starts from 0 to n.
            pin = Pin(selector[state], Pin.IN, Pin.PULL_UP) # read if pin is True or False
            if pin.value() == props["selected_state"]:
                state_list.append([state, len(selector) - 1])
                break
    return state_list


def get_pot_values():
    """
    Reads the values of potentimeters connected to the pins in 'pots'.
    Returns a list with the values of each pot, ranging from 0 - 100%. 0% and 100% are defined by 'pot_range'.
    """
    value_list = []
    for pin, props in pots:
        pot_value = ADC(pin).read_u16() # read value from pin

        pot_range = [props["min"], props["max"]] # Get min and max pot value out of dict
        if pot_value < pot_range[0]: # clip off at min value if required
            pot_value = pot_range[0]
        if pot_value > pot_range[1]: # clip off at max value if required
            pot_value = pot_range[1]
        pot_value = pot_value - pot_range[0] # adjust pot_value to zero
        
        pot_pct = 1 / (pot_range[1] - pot_range[0]) * pot_value # turn into %
        
        props_out = props.copy() # Keep original dict untouched!
        del props_out["min"]
        del props_out["max"]
        
        value_list.append([pot_pct, props_out])
    return value_list




def main_loop():
    while True:
        button_states = get_button_states()
        selector_states = get_selector_states()
        pot_values = get_pot_values()
    
        sys.stdout.write("Device: " + dev_identifier + ";    Buttons: " + str(button_states) + ";    Selectors: " + str(selector_states) + ";    Pots: " + str(pot_values) + ";\r") # Output to serial console. ';' is the delimiter
      

if __name__ == "__main__": # don't start main loop when imported => for debugging purposes
    main_loop()
