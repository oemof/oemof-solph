# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/oemof/oemof-solph/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                        |    Stmts |     Miss |   Branch |   BrPart |      Cover |   Missing |
|------------------------------------------------------------ | -------: | -------: | -------: | -------: | ---------: | --------: |
| src/oemof/solph/\_\_init\_\_.py                             |       19 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/\_console\_scripts.py                       |       33 |        0 |        6 |        0 |    100.00% |           |
| src/oemof/solph/\_energy\_system.py                         |      146 |        7 |       70 |        7 |     92.59% |91-\>93, 189-190, 264-\>267, 270-\>273, 335, 381-385, 391-395 |
| src/oemof/solph/\_groupings.py                              |       28 |        0 |       12 |        3 |     92.50% |69-\>72, 83-\>86, 95-\>98 |
| src/oemof/solph/\_helpers.py                                |       26 |        2 |       10 |        0 |     94.44% |   118-120 |
| src/oemof/solph/\_models.py                                 |      173 |        4 |       70 |        5 |     96.30% |156-\>159, 176-\>exit, 360-\>336, 365-\>336, 391, 556-559 |
| src/oemof/solph/\_options.py                                |       96 |        2 |       30 |        1 |     96.03% |   128-129 |
| src/oemof/solph/\_plumbing.py                               |      113 |        1 |       26 |        1 |     98.56% |       152 |
| src/oemof/solph/\_results.py                                |      118 |       24 |       56 |        1 |     74.14% |77, 94, 207-265 |
| src/oemof/solph/buses/\_\_init\_\_.py                       |        2 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/buses/\_bus.py                              |       38 |        0 |       16 |        2 |     96.30% |53-\>55, 55-\>57 |
| src/oemof/solph/components/\_\_init\_\_.py                  |       13 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/components/\_converter.py                   |       51 |        2 |       24 |        1 |     96.00% |110-\>113, 241-242 |
| src/oemof/solph/components/\_extraction\_turbine\_chp.py    |        9 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/components/\_generic\_chp.py                |      148 |       15 |       20 |        8 |     86.31% |136-\>138, 180, 218-222, 345, 487, 501-509, 523-529, 544 |
| src/oemof/solph/components/\_generic\_storage.py            |      467 |       17 |      174 |       11 |     94.07% |211-\>213, 558, 631-634, 780-\>787, 782-\>780, 926-927, 1507, 1589-\>1596, 1591-\>1589, 1632-1638, 1755-1760, 1864-1871 |
| src/oemof/solph/components/\_link.py                        |       56 |        2 |       24 |        5 |     91.25% |99-\>101, 172, 185-\>exit, 186-\>185, 187-\>186, 200 |
| src/oemof/solph/components/\_offset\_converter.py           |      117 |       28 |       34 |        3 |     79.47% |196, 214, 248-290, 349 |
| src/oemof/solph/components/\_sink.py                        |       10 |        0 |        4 |        0 |    100.00% |           |
| src/oemof/solph/components/\_source.py                      |       10 |        0 |        4 |        0 |    100.00% |           |
| src/oemof/solph/components/\_variable\_split\_converter.py  |       96 |        0 |       38 |        0 |    100.00% |           |
| src/oemof/solph/constraints/\_\_init\_\_.py                 |       12 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/constraints/equate\_flows.py                |       20 |        0 |       10 |        1 |     96.67% |   50-\>46 |
| src/oemof/solph/constraints/equate\_variables.py            |        7 |        0 |        2 |        1 |     88.89% |   91-\>94 |
| src/oemof/solph/constraints/flow\_count\_limit.py           |       30 |        0 |       14 |        1 |     97.73% |   99-\>91 |
| src/oemof/solph/constraints/integral\_limit.py              |       31 |        6 |       20 |        5 |     78.43% |132-138, 141, 159-\>165, 166, 206 |
| src/oemof/solph/constraints/investment\_limit.py            |       26 |       15 |       14 |        0 |     37.50% |     33-55 |
| src/oemof/solph/constraints/shared\_limit.py                |       15 |        0 |        4 |        0 |    100.00% |           |
| src/oemof/solph/constraints/storage\_level.py               |       76 |       38 |       20 |        2 |     50.00% |114-179, 192, 263-329, 342 |
| src/oemof/solph/flows/\_\_init\_\_.py                       |        2 |        0 |        0 |        0 |    100.00% |           |
| src/oemof/solph/flows/\_flow.py                             |       98 |        0 |       52 |        1 |     99.33% | 261-\>267 |
| src/oemof/solph/flows/\_invest\_non\_convex\_flow\_block.py |      104 |        1 |       24 |        2 |     97.66% |140-\>exit, 308 |
| src/oemof/solph/flows/\_investment\_flow\_block.py          |      114 |       19 |       46 |        6 |     76.88% |209-210, 448-455, 466-474, 485-491, 592, 605-606, 625-631, 647-652 |
| src/oemof/solph/flows/\_non\_convex\_flow\_block.py         |       54 |        1 |       10 |        2 |     95.31% |93-\>92, 141 |
| src/oemof/solph/flows/\_shared.py                           |      156 |       18 |       46 |        6 |     84.16% |179, 186, 389-413, 432-460, 585-\>584, 613-\>612 |
| src/oemof/solph/flows/\_simple\_flow\_block.py              |       92 |        0 |       40 |        1 |     99.24% | 383-\>382 |
| src/oemof/solph/helpers.py                                  |       20 |        1 |        8 |        2 |     89.29% |28, 37-\>39 |
| src/oemof/solph/processing.py                               |      352 |       63 |      154 |       13 |     82.21% |59, 62-\>exit, 74, 108-110, 158-164, 196-203, 267, 272, 299-309, 324, 331, 421-457, 499, 546, 672-686, 725-728, 795, 798-801, 935 |
| src/oemof/solph/views.py                                    |      132 |        3 |       50 |        5 |     95.60% |68, 91, 96, 296-\>299, 340-\>342 |
| **TOTAL**                                                   | **3110** |  **269** | **1132** |   **96** | **89.37%** |           |


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