#!/usr/bin/env python3

import sys
import json

with open(sys.argv[1]) as f:
    loaded = json.load(f)
    for a in loaded["annotations"]:
        if a["namespace"] == "onset":
            for d in a["data"]:
                print(d["time"])
