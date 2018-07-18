from .network import Bus, Component, Edge

import xarray as xr


def graph(nodes):
    edges = [n for n in nodes if isinstance(n, Edge)]
    variables = {'edges': xr.DataArray(data=edges,
        dims=["inputs", "outputs"],
        coords={"inputs": [e.input.label for e in edges],
                "outputs": [e.output.label for e in edges]})}

    non_edges = [n for n in nodes if not isinstance(n, Edge)]
    variables['nodes'] = xr.DataArray(data=non_edges,
        dims=["labels"],
        coords={"labels": [e.label for e in non_edges]})

    return xr.Dataset(data_vars=variables)

