#!/usr/bin/env python

import plotter

files = ["../csv-samples/20220128_13-44-01_DS007_LargeGrains.csv",
        "../csv-samples/20220131_12-16-00_DS008_LargeGrains.csv",
        "../csv-samples/20220127_12-31-06_DS005_LargeGrain.csv",
        ]
plotter.plotPressureAndTemp(files)
