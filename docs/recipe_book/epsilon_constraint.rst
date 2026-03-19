.. _epsilon_constraint_label:

################################################
:math:`\epsilon`-constraint and the Pareto Front 
################################################
A possible usecase of Multiobjective Optimization
=================================================

What is a Pareto Front?
-----------------------

The Pareto Front is a method to achieve a balance between two conflicting 
optimization goals, commonly used in multiobjective optimization. A typical use
case in energy system optimization is balancing costs and emissions. It's 
crucial that the two objectives are not correlated to derive a meaningful 
Pareto Front.

.. 	figure:: /_files/pareto.png
   :alt: Pareto Front example
   :align: center
   :figclass: only-light

To calculate the Pareto Front, follow these steps:

**Step 1:** Optimize your problem using :math:`obj1` as the objective function. 
Calculate the value :math:`value_{obj2}` for :math:`obj2` from the results.

**Step 2:** Re-optimize using :math:`obj1` as the objective, adding an 
:math:`\epsilon`-constraint:

.. math::

    obj2 \le \epsilon \cdot value_{obj2}

where :math:`\epsilon \in [0,1]` determines the step size for approximating the
Pareto Front.. 

**Step 3:** Repeat Steps 1 and 2 until a termination condition is met. Examples
for Termination conditions include:

- The problem becomes infeasible.
- The optimal value for :math:`obj2` is reached. Therefore you first need to 
  optimize with :math:`obj2` as the objective and than chose :math:`\epsilon` 
  accordingly.
- A time limit is reached.

The real Pareto Front?
^^^^^^^^^^^^^^^^^^^^^^

The described method may not yield the exact Pareto Front. A potentially more 
optimal :math:`value_{obj2}` can be found by fixing the optimal value of 
:math:`obj1` and then optimizing for :math:`obj2`. This is computationally 
expensive and mainly used for scientific purposes. For more on augmented 
:math:`\epsilon` constraints, see 
`this article <https://doi.org/10.1016/j.apenergy.2022.120521>`_ .

How to realise it in Code
-------------------------

.. code-block:: python

    # create your energy system normally but give the flows the 
    # to set other key words the just varible costs you could pass one with the flow
    ... solph.Flow(variable_costs=...,
                    keyword_set_on_the_flow=...,
                )
    # Optimize your energy system normally using obj1 
    optimization_model.solve(..)

    # read the vaule of obj2 from your results
    obj2= ...

    # store all results needed

    While termination_condition:       
        # add the epsilon constraint to you model
        optimisation_model = solph.constraints.generic_integral_limit(
            optimisation_model, "keyword_set_on_the_flow", limit= step_size * obj2
        )

        # solve the model with the epsilon constaint
        solver_results = optimisation_model.solve(
            ...
        )

        #store obj2
        obj2=...

        # store all results needed

        # set termination condition 
        # this could be when the model gets infeasible, when the optimal for 
        # obj2 is reached (therefore you need to optimize your problem with obj2 
        # as objective function once), a time limit,...
        termination_condition=...


