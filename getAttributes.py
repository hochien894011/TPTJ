"""
USAGE:
python3 getAttributes.py /path/to/json/file
    default: Print out the dictionary of attributes and value EXCLUDING "JFULL" and "JPDF"
    --a: Print out the dictionary of all attributes
    --s: "<attrbuteName>": Print out a specific attribute
    --m: "<attrbuteName>,<attrbuteName>,...": Print out multiple attributes
"""

import json
import sys
import argparse

def load_json(filepath):
    """Load the JSON file from the specified path."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filepath}")
        sys.exit(1)

def get_attributes(data, exclude_jfull=True):
    """Return all attributes in the JSON file as a dictionary. Optionally exclude 'JFULL' and 'JPDF'."""
    result = {}
    for key, value in data.items():
        if exclude_jfull and key in ["JFULL", "JPDF"]:
            continue
        result[key] = value
    return result

def get_specific_attribute(data, attribute_name):
    """Return a specific attribute as a dictionary."""
    return {attribute_name: data.get(attribute_name, f"Attribute '{attribute_name}' not found.")}

def get_multiple_attributes(data, attribute_names):
    """Return multiple specific attributes as a dictionary."""
    result = {}
    for name in attribute_names:
        result[name] = data.get(name, f"Attribute '{name}' not found.")
    return result

def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Extract attributes from judgement JSON files.")
    parser.add_argument("filepath", help="Path to the judgement JSON file")
    parser.add_argument("--a", action="store_true", help="Return all attributes including 'JFULL' and 'JPDF'")
    parser.add_argument("--s", metavar="attribute", help="Return a specific attribute by name")
    parser.add_argument("--m", metavar="attributes", help="Return multiple specific attributes, separated by commas")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Load the JSON file
    data = load_json(args.filepath)

    # Determine the action based on the arguments and return the result as a dictionary
    if args.a:
        # Return all attributes including 'JFULL' and 'JPDF'
        result = get_attributes(data, exclude_jfull=False)
    elif args.s:
        # Return a specific attribute
        result = get_specific_attribute(data, args.s)
    elif args.m:
        # Return multiple specific attributes
        attribute_names = args.m.split(',')
        result = get_multiple_attributes(data, attribute_names)
    else:
        # Default: Return all attributes excluding 'JFULL' and 'JPDF'
        result = get_attributes(data)

    # Print the result as a JSON-formatted dictionary
    print(json.dumps(result, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()



