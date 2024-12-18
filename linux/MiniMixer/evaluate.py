#!/usr/bin/env python3
from ast import literal_eval


def _extract_string(string, key, delimiter = ";"):
    start_string = f"{key}: "
    start = string.find(start_string)
    if start == -1: # Catch if key doesn't exist
        return None
    start += len(start_string)  # Move past start_string

    end = string.find(delimiter, start)
    if end == -1: # If delimiter doesn't exist: no bueno!!
        raise Exception("Delimiter for key", key, "not found!!!!!!!!!!")

    string_stripped = string[start:end].strip()
    return string_stripped


def serial2dict(serial_output):
    device    = _extract_string(serial_output, "Device")
    str_buttons   = _extract_string(serial_output, "Buttons")
    str_selectors = _extract_string(serial_output, "Selectors")
    str_pots      = _extract_string(serial_output, "Pots")

    serial_dict = {}
    if str_buttons != None:
        buttons = literal_eval(str_buttons)
        serial_dict["buttons"] = buttons
    if str_selectors != None:
        selectors = literal_eval(str_selectors)
        serial_dict["selectors"] = selectors
    if str_pots != None:
        pots = literal_eval(str_pots)
        serial_dict["pots"] = pots

    return serial_dict
