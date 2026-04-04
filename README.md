# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/oemof/oemof-solph/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                        |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|------------------------------------------------------------ | -------: | -------: | -------: | -------: | ---------: | --------: |
| src/oemof/solph/\_\_init\_\_.py                             |       19 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/\_console\_scripts.py                       |       33 |        0 |        6 |        0 |    100.00% |           |
| src/oemof/solph/\_energy\_system.py                         |      109 |        4 |       48 |        3 |     95.54% |102-\>104, 319-323, 329-333 |
| src/oemof/solph/\_groupings.py                              |       28 |        0 |       12 |        3 |     92.50% |69-\>72, 83-\>86, 95-\>98 |
| src/oemof/solph/\_helpers.py                                |       26 |        2 |       10 |        0 |     94.44% |   118-120 |
| src/oemof/solph/\_models.py                                 |      158 |        4 |       58 |        5 |     95.83% |184-\>189, 189-\>exit, 379-\>358, 383-\>358, 408, 506-509 |
| src/oemof/solph/\_options.py                                |       84 |        0 |       30 |        0 |    100.00% |           |
| src/oemof/solph/\_plumbing.py                               |       65 |        0 |       26 |        0 |    100.00% |           |
| src/oemof/solph/\_results.py                                |      116 |       26 |       56 |        2 |     72.09% |93, 155, 158-159, 205-263 |
| src/oemof/solph/buses/\_\_init\_\_.py                       |        2 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/buses/\_bus.py                              |       38 |        0 |       16 |        2 |     96.30% |53-\>55, 55-\>57 |
| src/oemof/solph/components/\_\_init\_\_.py                  |       12 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/components/\_converter.py                   |       49 |        2 |       24 |        1 |     95.89% |107-\>110, 240-241 |
| src/oemof/solph/components/\_extraction\_turbine\_chp.py    |       43 |        1 |       12 |        1 |     96.36% |       217 |
| src/oemof/solph/components/\_generic\_chp.py                |      146 |       15 |       20 |        8 |     86.14% |133-\>135, 177, 215-219, 342, 484, 498-506, 520-526, 541 |
| src/oemof/solph/components/\_generic\_storage.py            |      600 |       90 |      264 |       30 |     82.64% |194-\>196, 512, 583-586, 732-\>739, 734-\>732, 829-\>828, 849-850, 1355, 1363, 1524-1530, 1561-1568, 1595-1596, 1610-1611, 1621-1631, 1635-1636, 1659-1671, 1701-1703, 1707-1711, 1736, 1816-\>1823, 1818-\>1816, 1862-1868, 1963-1965, 1982-1986, 2023-2027, 2036-2064, 2169-\>2175, 2207-2246, 2250-2256, 2266-2271, 2281-2288, 2344-2373 |
| src/oemof/solph/components/\_link.py                        |       54 |        2 |       24 |        5 |     91.03% |96-\>98, 170, 183-\>exit, 184-\>183, 185-\>184, 198 |
| src/oemof/solph/components/\_offset\_converter.py           |      145 |       29 |       48 |        5 |     82.38% |214, 234, 283, 307-\>311, 338-380, 437 |
| src/oemof/solph/components/\_sink.py                        |       10 |        1 |        4 |        1 |     85.71% |        49 |
| src/oemof/solph/components/\_source.py                      |       10 |        1 |        4 |        1 |     85.71% |        67 |
| src/oemof/solph/constraints/\_\_init\_\_.py                 |       15 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/constraints/equate\_flows.py                |       20 |        0 |       10 |        1 |     96.67% |   50-\>46 |
| src/oemof/solph/constraints/equate\_variables.py            |        7 |        0 |        2 |        1 |     88.89% |   91-\>94 |
| src/oemof/solph/constraints/flow\_count\_limit.py           |       23 |        0 |       10 |        1 |     96.97% |   88-\>82 |
| src/oemof/solph/constraints/integral\_limit.py              |       48 |       21 |       24 |        5 |     58.33% |49, 148-154, 157, 175-\>181, 182, 229-267, 301 |
| src/oemof/solph/constraints/investment\_limit.py            |       50 |       37 |       28 |        0 |     21.79% |35-57, 78-120 |
| src/oemof/solph/constraints/shared\_limit.py                |       15 |        0 |        4 |        0 |    100.00% |           |
| src/oemof/solph/constraints/storage\_level.py               |       76 |       38 |       20 |        2 |     50.00% |109-172, 185, 251-315, 328 |
| src/oemof/solph/flows/\_\_init\_\_.py                       |        2 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/flows/\_flow.py                             |      105 |        0 |       60 |        1 |     99.39% | 300-\>306 |
| src/oemof/solph/flows/\_invest\_non\_convex\_flow\_block.py |      101 |        0 |       24 |        1 |     99.20% |140-\>exit |
| src/oemof/solph/flows/\_investment\_flow\_block.py          |      250 |      139 |      110 |       10 |     39.17% |233-234, 248-258, 458-464, 473-622, 663-668, 679-685, 696-702, 711-742, 907-1034, 1090-1125, 1134-1140, 1156-1161 |
| src/oemof/solph/flows/\_non\_convex\_flow\_block.py         |       54 |        0 |       10 |        1 |     98.44% |   93-\>92 |
| src/oemof/solph/flows/\_shared.py                           |      159 |       18 |       52 |        6 |     84.83% |178, 185, 424-448, 467-495, 620-\>619, 648-\>647 |
| src/oemof/solph/flows/\_simple\_flow\_block.py              |      127 |       15 |       66 |        7 |     85.49% |337, 350-352, 368-375, 443-\>442, 456-\>469, 475, 484-488, 495-500 |
| src/oemof/solph/helpers.py                                  |       20 |        1 |        8 |        2 |     89.29% |28, 37-\>39 |
| src/oemof/solph/processing.py                               |      347 |       42 |      152 |       13 |     87.37% |52, 55-\>exit, 67, 101-103, 151-157, 191-196, 265, 317, 324, 431, 443-448, 492, 527, 653-667, 706-709, 776, 779-782, 879, 916 |
| src/oemof/solph/views.py                                    |      132 |        3 |       50 |        5 |     95.60% |68, 91, 96, 296-\>299, 340-\>342 |
| **TOTAL**                                                   | **3298** |  **491** | **1292** |  **123** | **82.75%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/oemof/oemof-solph/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/oemof/oemof-solph/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/oemof/oemof-solph/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/oemof/oemof-solph/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Foemof%2Foemof-solph%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/oemof/oemof-solph/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.