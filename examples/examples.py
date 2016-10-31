from .solph.csv_reader.investment_example.investment_example import run_investment_example
from .solph.flexible_modelling.add_constraints import run_add_constraints_example
from .solph.simple_least_costs.simple_least_costs import run_simple_least_costs_example
from .solph.storage_optimization.storage_invest import run_storage_invest_example
from .solph.csv_reader.operational_example.operational_example import run_operational_example

import argparse
import sys

def examples():
    parser = argparse.ArgumentParser(
        description='Choose one of the examples below listed examples!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        List of examples

         * storage_invest
         * simple_least_costs
         * investment
         * flexible_modelling
         * operational_example
         ''')
    parser.add_argument('example', type=str,
                    help='Example name (from list of examples)')

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    example = args.example

    if example == 'investment':
        run_investment_example()
    elif example == 'flexible_modelling':
        run_add_constraints_example()
    elif example == 'simple_least_costs':
        run_simple_least_costs_example()
    elif example == 'storage_invest':
        run_storage_invest_example()
    elif example == 'operational_example':
        run_operational_example()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    pass