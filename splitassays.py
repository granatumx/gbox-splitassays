#!/usr/bin/env python

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from colour import Color
from matplotlib.patches import Polygon
import statistics as st
import time
from random import randrange
import re
import sys

from granatum_sdk import Granatum

def invert_dict(my_map):
    inv_map = {}
    for k, v in my_map.items():
        inv_map[v] = inv_map.get(v, []) + [k]
    return inv_map


def main():
    tic = time.perf_counter()

    gn = Granatum()
    assay = gn.pandas_from_assay(gn.get_import('assay'))
    groups = gn.get_import('groups')

    inv_map = invert_dict(groups)

    toc = time.perf_counter()
    time_passed = round(toc - tic, 2)

    for key, val in inv_map.items():
        assay_export_name = "[A]{}".format(key)
        overlap = set(val).intersection(set(assay.columns))
        if len(overlap) > 4:
            tb = assay.loc[:, list(overlap)]

            exported_assay = {
                "matrix": tb.T.values.tolist(),
                "sampleIds": tb.columns.tolist(),
                "geneIds": tb.index.tolist(),
            }

            gn.export(exported_assay, assay_export_name, "assay")
            gn.export(tb.to_csv(), "{}.csv".format(key), kind='raw', meta=None, raw=True)

    timing = "* Finished step in {} seconds*".format(time_passed)
    gn.add_result(timing, "markdown")

    gn.commit()


if __name__ == "__main__":
    main()
