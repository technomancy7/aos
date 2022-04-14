#!/bin/env python3
import random, sys

def parseDiceNotation(notation):
    try:
        if "d" in notation:
            count = 1
            if notation.split("d")[0] != "":
                count = int(notation.split("d")[0])
            sides = notation.split("d")[1]
            if "+" in sides:
                realsides = int(sides.split("+")[0])
                mod = int(sides.split("+")[1])
                return {"sides": realsides, "modifier": mod, "die": count, "valid": True}
            else:
                sides = int(sides)
                return {"sides": sides, "modifier": 0, "die": count, "valid": True}
        else:
            return {"sides": 0, "modifier": 0, "die": 0, "valid": False}
    except Exception as e:
        print(e)
        return {"sides": 0, "modifier": 0, "die": 0, "valid": False}

def roll(notation):
    d = parseDiceNotation(notation)
    out = {"rolls": [], "total": 0, **d}
    if d["valid"]:
        for die in range(0, d["die"]):
            tmp = random.randrange(1, d["sides"]+1)
            if d["modifier"] != 0:
                tmp += d["modifier"]
            out["rolls"].append(tmp)
            out["total"] += tmp
    return out

def prettyRoll(result):
    if type(result) == str: result = roll(result)
    return f"""Rolling {result['die']}d{result['sides']} (+{result['modifier']})
Total: {result['total']}
Rolls: {result['rolls']}"""
    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(prettyRoll(roll("d6")))
    else:
        if sys.argv[1] in ["help", "h", "-h", "--help"]:
            print("Format: (fn)[die]d[sides](+mod)"); print("Examples: d6 | 2d6 | 2d6+2")
        else:
            print(prettyRoll(roll(sys.argv[1])))
