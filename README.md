# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/oemof/oemof-solph/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                        |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|------------------------------------------------------------ | -------: | -------: | -------: | -------: | ---------: | --------: |
| src/oemof/solph/\_\_init\_\_.py                             |       19 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/\_console\_scripts.py                       |       33 |        0 |        6 |        0 |    100.00% |           |
| src/oemof/solph/\_energy\_system.py                         |      146 |        7 |       70 |        7 |     92.59% |91-\>93, 189-190, 264-\>267, 270-\>273, 335, 381-385, 391-395 |
| src/oemof/solph/\_groupings.py                              |       28 |        0 |       12 |        3 |     92.50% |69-\>72, 83-\>86, 95-\>98 |
| src/oemof/solph/\_helpers.py                                |       26 |        2 |       10 |        0 |     94.44% |   118-120 |
| src/oemof/solph/\_models.py                                 |      223 |        0 |       90 |        0 |    100.00% |           |
| src/oemof/solph/\_options.py                                |      165 |        2 |       30 |        1 |     97.44% |   168-169 |
| src/oemof/solph/\_plumbing.py                               |      101 |        0 |       26 |        0 |    100.00% |           |
| src/oemof/solph/\_results.py                                |      141 |        5 |       60 |        4 |     95.52% |103, 105, 256, 268-\>266, 292-293 |
| src/oemof/solph/buses/\_\_init\_\_.py                       |        2 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/buses/\_bus.py                              |       38 |        0 |       16 |        2 |     96.30% |53-\>55, 55-\>57 |
| src/oemof/solph/components/\_\_init\_\_.py                  |       13 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/components/\_converter.py                   |       55 |        2 |       24 |        1 |     96.20% |107-\>110, 246-247 |
| src/oemof/solph/components/\_extraction\_turbine\_chp.py    |        9 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/components/\_generic\_chp.py                |      152 |       15 |       20 |        8 |     86.63% |133-\>135, 177, 215-219, 350, 492, 506-514, 528-534, 549 |
| src/oemof/solph/components/\_generic\_storage.py            |      522 |       14 |      174 |       11 |     94.97% |198-\>200, 633, 706-709, 855-\>862, 857-\>855, 1001-1002, 1583, 1668-\>1675, 1670-\>1668, 1712-1718, 1945-1952 |
| src/oemof/solph/components/\_link.py                        |       60 |        2 |       24 |        5 |     91.67% |96-\>98, 177, 190-\>exit, 191-\>190, 192-\>191, 205 |
| src/oemof/solph/components/\_offset\_converter.py           |      126 |       28 |       34 |        3 |     80.62% |192, 210, 260-302, 361 |
| src/oemof/solph/components/\_sink.py                        |       10 |        0 |        4 |        0 |    100.00% |           |
| src/oemof/solph/components/\_source.py                      |       10 |        0 |        4 |        0 |    100.00% |           |
| src/oemof/solph/components/\_variable\_split\_converter.py  |      105 |        0 |       38 |        0 |    100.00% |           |
| src/oemof/solph/constraints/\_\_init\_\_.py                 |       12 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/constraints/equate\_flows.py                |       20 |        0 |       10 |        1 |     96.67% |   50-\>46 |
| src/oemof/solph/constraints/equate\_variables.py            |        7 |        0 |        2 |        1 |     88.89% |   91-\>94 |
| src/oemof/solph/constraints/flow\_count\_limit.py           |       30 |        0 |       14 |        1 |     97.73% |   99-\>91 |
| src/oemof/solph/constraints/integral\_limit.py              |       31 |        6 |       20 |        5 |     78.43% |132-138, 141, 159-\>165, 166, 206 |
| src/oemof/solph/constraints/investment\_limit.py            |       26 |       15 |       14 |        0 |     37.50% |     33-55 |
| src/oemof/solph/constraints/shared\_limit.py                |       15 |        0 |        4 |        0 |    100.00% |           |
| src/oemof/solph/constraints/storage\_level.py               |       76 |       38 |       20 |        2 |     50.00% |114-179, 192, 263-329, 342 |
| src/oemof/solph/flows/\_\_init\_\_.py                       |        2 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/flows/\_flow.py                             |      132 |        0 |       52 |        1 |     99.46% | 250-\>256 |
| src/oemof/solph/flows/\_invest\_non\_convex\_flow\_block.py |      104 |        1 |       24 |        2 |     97.66% |140-\>exit, 308 |
| src/oemof/solph/flows/\_investment\_flow\_block.py          |      114 |        9 |       46 |        3 |     90.00% |209-\>exit, 449-456, 467-475, 486-492, 593 |
| src/oemof/solph/flows/\_non\_convex\_flow\_block.py         |       54 |        1 |       10 |        2 |     95.31% |93-\>92, 141 |
| src/oemof/solph/flows/\_shared.py                           |      175 |        4 |       46 |        6 |     95.48% |366, 376, 464, 492, 623-\>622, 651-\>650 |
| src/oemof/solph/flows/\_simple\_flow\_block.py              |       92 |        0 |       40 |        1 |     99.24% | 389-\>388 |
| src/oemof/solph/helpers.py                                  |       20 |        1 |        8 |        2 |     89.29% |28, 37-\>39 |
| src/oemof/solph/processing.py                               |      366 |       65 |      156 |       13 |     82.38% |60, 63-\>exit, 75, 109-111, 159-165, 197-204, 268, 273, 300-310, 325, 332, 422-458, 500, 547, 673-687, 726-729, 829, 832-835, 847-848, 971 |
| src/oemof/solph/views.py                                    |      132 |        3 |       50 |        5 |     95.60% |68, 91, 96, 296-\>299, 340-\>342 |
| **TOTAL**                                                   | **3392** |  **220** | **1158** |   **90** | **92.09%** |           |


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