# -*- coding: utf-8 -*-

"""
Example showing the difference between constant charging and SOC-dependent
charging of a storage.

Dependencies:
    * matplotlib
    * oemof-tools

Licence
-------
`MIT licence <https://github.com/oemof/oemof-solph/blob/dev/LICENSE>`_

"""

import logging

from matplotlib import pyplot as plt
from oemof.tools import logger

from oemof import solph


def plotting(results):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes = axes.flatten()
    n = 0
    for storage in results["storage_content"].sort_index(axis=1).columns:
        storage = storage.label
        s = len(results["flow"])
        ax1 = (
            results["flow"][
                [c for c in results["flow"].columns if storage in str(c[1])]
            ]
            .reset_index(drop=True)
            .plot(ax=axes[n], color="tab:green")
        )
        ax1.set_ylim(0, 10)
        ax1.set_xlim(0, s)
        ax2 = axes[n].twinx()
        ax2.set_ylim(0, 100)
        ax2.set_title(storage)
        results["storage_content"][storage].reset_index(drop=True).plot(ax=ax2)
        value = results["storage_content"][storage].max()
        text = f"Final storage level: {value:.0f}%"
        props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
        axes[n].text(
            0.25,
            0.75,
            text,
            transform=axes[n].transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=props,
        )

        lines1, labels1 = axes[n].get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        axes[n].legend(
            lines1 + lines2,
            ["Charging power (left)", "Storage Content (right)"],
            loc="upper left",
        )
        n += 1

    for i in range(2, len(axes)):
        axes[i].axis("off")
    plt.tight_layout()
    plt.show()


def optimise_storage():
    """A minimal storage model, that just loads the storages."""
    logger.define_logging()
    logging.info("Initialize the energy system")

    energysystem = solph.EnergySystem(
        timeindex=solph.create_time_index(2012, number=20),
        infer_last_interval=False,
    )

    logging.info("Create oemof objects")
    bel = solph.Bus(label="electricity", balanced=False)
    energysystem.add(bel)

    storage = solph.components.GenericStorage(
        label="Constant Charging Power",
        inputs={bel: solph.Flow(10, variable_costs=-1, maximum=0.5)},
        outputs={bel: solph.Flow(10, variable_costs=2)},
        nominal_capacity=100,
        balanced=False,
    )
    storage_new = solph.components.GenericStorage(
        label="SOC-dependent Charging Power",
        inputs={bel: solph.Flow(10, variable_costs=-1, maximum=0.5)},
        outputs={bel: solph.Flow(10, variable_costs=2)},
        nominal_capacity=100,
        balanced=False,
        constant_soc_until=0.2,
        fraction_saturation_charging=0.3,
    )
    energysystem.add(storage, storage_new)

    logging.info("Optimise the energy system")
    om = solph.Model(energysystem)
    om.solve(solver="cbc", solve_kwargs={"tee": False})

    return solph.Results(om)


if __name__ == "__main__":
    plotting(optimise_storage())
