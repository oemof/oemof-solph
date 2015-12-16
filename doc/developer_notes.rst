=========================================
 Developer Notes
=========================================

Here we gather important notes for the developing of oemof and elements within
the framework.


Collaboration
-----------------------------------------

We use the collaboration features from Github, see https://github.com/oemof.


h2. Style guidlines

h3. PEP8 (Python Style Guide)

We adhere to “PEP8”:https://www.python.org/dev/peps/pep-0008/ for any
code produced in the framework.

We use pylint to check your code. Pylint is integrated in many IDEs and
Editors. “Check here”:http://docs.pylint.org/ide-integration or ask the
maintainer of your IDE or Editor.

Some IDEs have pep8 checkers, which are very helpful, especially for
python beginners.

h3. Quoted strings

For strings we use double quotes if possible.

.. raw:: html

   <pre><code class="python">
   info_msg = "We use double quotes for strings"
   info_msg = 'This is a string where we need to use "single" quotes'
   </code></pre>

h3. UML class diagrams

We use @pyreverse@ for the creation of UML class diagrams, which will be
integrated in the sphinx documentation (done by Günni). For example:

.. raw:: html

   <pre>
   pyreverse -o png -p components oemof/src/components.py
   </pre>

h2. Naming Conventions

We use plural in the code for modules if there are possibly more than
one child classes (e.g. import transformers AND NOT transformer). Arrays
in the code if there are multiple have to be plural (e.g. @transformers
= [T1, T2,…]@).

Please, follow the following naming conventions!!

| *Type* \| *Public* \| *Internal* \|
| Packages \| lower\_with\_under \| none \|
| Modules \| lower\_with\_under \| \_lower\_with\_under \|
| Classes \| CappedCamelCase \| \_CappedCamelCase \|
| Exception \| CappedCamelCase \| \_CappedCamelCase \|
| Functions \| lower\_with\_under() \| \_lower\_with\_under() \|
| Global/Class Constants \| CAPS\_WITH\_UNDER \| \_CAPS\_WITH\_UNDER \|
| Global/Class Variables \| lower\_with\_under \| \_lower\_with\_under
  \|
| Instance Variables \| lower\_with\_under \| \_lower\_with\_under
  (protected) \_\_lower\_with\_under (private) \|
| Method Names \| lower\_with\_under() \| \_lower\_with\_under()
  (protected) \_\_lower\_with\_under() (private) \|
| Function/Method Parameters \| lower\_with\_under \| none \|
| Local Variables \| lower\_with\_under \| none \|

See also: http://pylint-messages.wikidot.com/messages:c0103

*Use talking names!*

This means: \* Variables/Objects: Name it after the data they describe
(pwer\_line, wind\_speed) \* Functions/Method: Name it after what they
do: *use verbs* (get\_wind\_speed, set\_parameter)

h2. Local files (config, output, csv…)

h3. Hidden folder

-  configuration files (e.g. oemof.cfg)
-  logging fi


Git branching model
-----------------------------------------

So far we adhere mostly to the git branching model by Vincent Driessen, see
http://nvie.com/posts/a-successful-git-branching-model/.

The only difference is to use a different name for the branch origin/develop 
("main branch where the source code of HEAD always reflects a state with the 
latest delivered development changes for the next release. Some would call this 
the integration branch."). The name we use is origin/dev.


Issue-Management
-----------------------------------------

Section about workflow for issues is still missing (when to assign an issue with
what kind of tracker to whom etc.).

