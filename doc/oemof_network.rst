.. _oemof_network_label:

~~~~~~~~~~~~~~~~~~~~~~
oemof-network
~~~~~~~~~~~~~~~~~~~~~~

The modeling of energy supply systems and its variety of components has a cleary structured approach within the oemof framework. Thus, energy supply systems with different levels of complexity can be based on equal basic module blocks. Those form an universal basic structure.

An *node* is either a *bus* or a *component*. A bus is always connected with one or several components. Likewise components are always connected with one or several buses. Based on their characteristics they are divided into several sub types. *Transformers* have input and output, e.g. a gas turbine takes from a bus of type 'gas' and feeds into a bus of type 'electricity'. With additional information like parameters and transfer functions input and output can be specified. Using the example of a gas turbine the resource consumption (input) is related to the provided end energy (output) by means of an conversion factor. Components of type *transformer* can also be used to model transmission lines. A *sink* has only an input but no output. With *sink* consumers like households can be modeled. A *source* has exactly one output but no input. Thus for example, wind energy and photovoltaic plants can be modeled.

Components and buses can be combined to an energy system. Buses are nodes, connected among each other through edges which are the inputs and outputs of the components. Such a model can be interpreted mathematically as bipartite graph as buses are solely connected to components and vice versa. Thereby the in- and outputs of the components are the directed edges of the graph. The buses themselves are the nodes of the graph.

Besides the use of the basic components one has the possibility to develop more specified components on the base of the basic components. The following figure illustrates the setup of a simple energy system and the basic structure explained before.

Example
------------------

An example of a simple energy system shows the usage of the nodes for 
real world representations.

*Region1:*

components: wind turbine (wt1), electrical demand (dm1), gas turbine (gt1), cable to region2 (cb1)
buses: gas pipeline (r1_gas), electrical grid (r1_el)

*Region2:*

components: coal plant (cp2), chp plant (chp2), electrical demand (dm2), cable to region2 (cb2), p2g-facility (ptg2)
buses: electrical grid (r2_el), local heat network (r2_th), coal reservoir (r2_coal), gas pipeline (r2_gas)


In oemof this would look as follows::

                input/output  r1_gas   r1_el   r2_el   r2_th   r2_coal   r2_gas
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
       wt1(Source)   |------------------>|       |       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
         dm1(Sink)   |<------------------|       |       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
  gt1(Transformer)   |<---------|        |       |       |       |         |
                     |------------------>|       |       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
  cb1(Transformer)   |          |        |------>|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
  cp2(Transformer)   |<------------------------------------------|         |
                     |-------------------------->|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
 chp2(Transformer)   |<----------------------------------------------------|
                     |-------------------------->|       |       |         |
                     |---------------------------------->|       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
         dm2(Sink)   |<--------------------------|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
  cb2(Transformer)   |          |        |<------|       |       |         |
                     |          |        |       |       |       |         |
                     |          |        |       |       |       |         |
 ptg2(Transformer)   |<--------------------------|       |       |         |
                     |---------------------------------------------------->|

