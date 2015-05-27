# oemof - The Open Energy Modelling Framework

## Special Dependencies

The `oemof` package depends on [`pvlib`][1], a library for simulating
photovoltaic energy systems. Since this library is a relatively fast
moving target with frequent updates you might want to avoid constantly
reinstalling or upgrading the package but instead work on the bleeding
edge source.

In order to do this, clone the `pvlib` repository into your favourite
folder:

```sh
git clone https://github.com/pvlib/pvlib-python.git /y/f/f
```

and then install the package from this location in [editable mode][2]:

```sh
pip install -e /y/f/f
```

That way you can use the package just as it was installed like any other
Python package but changes to the source tree located at `/y/f/f` (like
pull updates from upstream, checking out different versions for testing
purposes or even custom changes to scratch an itch only you have) will
be picked up immediately without reinstalling the package.

To find out more about editable mode, read the [short description][3]
and/or the longer [historical note][4] about the feature in `pip`'s
predecessor `setuptools`.

[1] https://github.com/pvlib/pvlib-python "The pvlib github repo"
[2] https://pip.pypa.io/en/stable/reference/pip_install.html#install-editable
[3] https://pip.pypa.io/en/stable/reference/pip_install.html#vcs-support
[4] https://pythonhosted.org/setuptools/setuptools.html#development-mode

