from fractions import Fraction
from typing import List
from pint import UnitRegistry

def number_str_to_float(amount_str:str) -> (any, bool):
    """
    Take in an amount string to return float (if possible).
    
    Valid string returns:
    Float
    Boolean -> True

    Invalid string Returns
    Original String
    Boolean -> False
    
    Examples:
    1 1/2 -> 1.5, True
    32 -> 32.0, True
    Abc -> Abc, False
    """
    success = False
    number_as_float = amount_str
    try:
        number_as_float = float(sum(Fraction(s) for s in f"{amount_str}".split()))
    except:
        pass
    if isinstance(number_as_float, float):
        success = True
    return number_as_float, success



def parse_paragraph_to_recipe_line(paragraph):
    paragraph = paragraph.replace("\n", " ").replace("\f", " ").replace("\t", " ")
    results = []
    current_str = ""
    for line in paragraph.split(" "):
        val, success = number_str_to_float(line)
        if success:
            # print(line, val)
            if current_str != "":
                results.append(current_str.strip())
            current_str = f"{line}"
        else:
            current_str += f" {line}"
    return results



def convert_to_qty_units(results: List[str]):
    ureg = UnitRegistry()
    dataset = []
    for i, x in enumerate(results):
        words = x.split(" ")
        qty = None
        qty_raw = None
        units = None
        other = []
        for word in words:
            val, success = number_str_to_float(word)
            if success:
                qty = val
                qty_raw = word
                continue
            iter_unit = None
            try:
                iter_unit = str(ureg[word.lower()].units)
            except:
                pass
            if units is None and iter_unit is not None:
                units = iter_unit
            else:
                other.append(word)
        name = ""
        other_txt = " ".join(other)
        description = None
        if len(other_txt) < 220:
            name = other_txt
        elif len(other_txt) >= 220:
            name = other_txt[:220]
            description = other_txt[220:]
        data = {
            "quantity_as_float": qty,
            "quantity": qty_raw,
            "unit": units,
            "name": name,
            "description": description,
        }
        dataset.append(data)
    return dataset