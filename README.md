# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/oemof/oemof-solph/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                        |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|------------------------------------------------------------ | -------: | -------: | -------: | -------: | ---------: | --------: |
| src/oemof/solph/\_\_init\_\_.py                             |       19 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/\_console\_scripts.py                       |       33 |        0 |        6 |        0 |    100.00% |           |
| src/oemof/solph/\_energy\_system.py                         |      109 |        4 |       48 |        3 |     95.54% |102-\>104, 319-323, 329-333 |
| src/oemof/solph/\_groupings.py                              |       28 |        0 |       12 |        3 |     92.50% |69-\>72, 83-\>86, 95-\>98 |
| src/oemof/solph/\_helpers.py                                |       26 |        2 |       10 |        0 |     94.44% |   118-120 |
| src/oemof/solph/\_models.py                                 |      159 |        4 |       58 |        5 |     95.85% |184-\>189, 189-\>exit, 379-\>358, 383-\>358, 408, 511-514 |
| src/oemof/solph/\_options.py                                |       98 |        0 |       30 |        0 |    100.00% |           |
| src/oemof/solph/\_plumbing.py                               |      113 |        1 |       26 |        1 |     98.56% |       152 |
| src/oemof/solph/\_results.py                                |      118 |       24 |       56 |        1 |     74.14% |77, 94, 207-265 |
| src/oemof/solph/buses/\_\_init\_\_.py                       |        2 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/buses/\_bus.py                              |       38 |        0 |       16 |        2 |     96.30% |53-\>55, 55-\>57 |
| src/oemof/solph/components/\_\_init\_\_.py                  |       12 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/components/\_converter.py                   |       51 |        2 |       24 |        1 |     96.00% |110-\>113, 241-242 |
| src/oemof/solph/components/\_extraction\_turbine\_chp.py    |       45 |        1 |       12 |        1 |     96.49% |       219 |
| src/oemof/solph/components/\_generic\_chp.py                |      148 |       15 |       20 |        8 |     86.31% |136-\>138, 180, 218-222, 345, 487, 501-509, 523-529, 544 |
| src/oemof/solph/components/\_generic\_storage.py            |      638 |       90 |      270 |       30 |     83.48% |220-\>222, 577, 650-653, 799-\>806, 801-\>799, 933-\>932, 953-954, 1459, 1467, 1626-1632, 1663-1670, 1697-1698, 1712-1713, 1723-1733, 1737-1738, 1761-1773, 1803-1805, 1809-1813, 1838, 1918-\>1925, 1920-\>1918, 1964-1970, 2065-2067, 2084-2088, 2125-2129, 2138-2166, 2271-\>2277, 2309-2348, 2352-2358, 2368-2373, 2383-2390, 2446-2475 |
| src/oemof/solph/components/\_link.py                        |       56 |        2 |       24 |        5 |     91.25% |99-\>101, 172, 185-\>exit, 186-\>185, 187-\>186, 200 |
| src/oemof/solph/components/\_offset\_converter.py           |      117 |       28 |       34 |        3 |     79.47% |196, 214, 248-290, 347 |
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
| src/oemof/solph/flows/\_flow.py                             |      113 |        0 |       60 |        1 |     99.42% | 311-\>317 |
| src/oemof/solph/flows/\_invest\_non\_convex\_flow\_block.py |      101 |        0 |       24 |        1 |     99.20% |140-\>exit |
| src/oemof/solph/flows/\_investment\_flow\_block.py          |      250 |      139 |      110 |       10 |     39.17% |233-234, 248-258, 458-464, 473-622, 663-668, 679-685, 696-702, 711-742, 907-1034, 1090-1125, 1134-1140, 1156-1161 |
| src/oemof/solph/flows/\_non\_convex\_flow\_block.py         |       54 |        0 |       10 |        1 |     98.44% |   93-\>92 |
| src/oemof/solph/flows/\_shared.py                           |      159 |       18 |       52 |        6 |     84.83% |178, 185, 424-448, 467-495, 620-\>619, 648-\>647 |
| src/oemof/solph/flows/\_simple\_flow\_block.py              |      127 |       15 |       66 |        7 |     85.49% |337, 350-352, 368-375, 443-\>442, 456-\>469, 475, 484-488, 495-500 |
| src/oemof/solph/helpers.py                                  |       20 |        1 |        8 |        2 |     89.29% |28, 37-\>39 |
| src/oemof/solph/processing.py                               |      352 |       41 |      154 |       12 |     87.94% |59, 62-\>exit, 74, 108-110, 158-164, 198-203, 272, 324, 331, 438, 450-455, 499, 546, 672-686, 725-728, 795, 798-801, 935 |
| src/oemof/solph/views.py                                    |      132 |        3 |       50 |        5 |     95.60% |68, 91, 96, 296-\>299, 340-\>342 |
| **TOTAL**                                                   | **3394** |  **488** | **1286** |  **120** | **83.21%** |           |


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