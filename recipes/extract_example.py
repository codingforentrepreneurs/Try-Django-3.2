from fractions import Fraction
from typing import List
from pint import UnitRegistry

def number_str_to_float(amount_str:str) -> (any, bool):
    success = False
    number_as_float = amount_str
    try:
        number_as_float = float(sum(Fraction(s) for s in f"{amount_str}".split()))
    except:
        pass
    if isinstance(number_as_float, float):
        success = True
    return number_as_float, success


extracted = {"results": ["1 pound chicken breasts cut into bite", "size pieces", "", "2 tbsp olive oil", "", "2 clove garlic crushed or minced", "", "1 tbsp chili powder", "", "1/2 teaspoon ground cumin", "", "1/4 teaspoon onion or garlic powder", "1/4 teaspoon kosher salt", "", "1 tbsp olive oil", "", "squeeze of lime optional", "\f"], "original": "1 pound chicken breasts cut into bite\nsize pieces\n\n2 tbsp olive oil\n\n2 clove garlic crushed or minced\n\n1 tbsp chili powder\n\n1/2 teaspoon ground cumin\n\n1/4 teaspoon onion or garlic powder\n1/4 teaspoon kosher salt\n\n1 tbsp olive oil\n\nsqueeze of lime optional\n\f"}

og = extracted['original']

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
        data = {
            "qty": qty,
            "qty_raw": qty_raw,
            "unit": units,
            "other": " ".join(other)
        }
        dataset.append(data)
    return dataset


results = parse_paragraph_to_recipe_line(og)
dataset = convert_to_qty_units(results)

print(dataset, results)