# -*- coding: utf-8 -*-
"""
Parses csv files containing distances and scales and outputs JSON object file
"""

import pandas as pd

dist = pd.read_csv("dist.csv")
scale = pd.read_csv("scale.csv")