from nose.tools import assert_raises, eq_, ok_

from oemof.network import Node

class Node_Tests:
    def test_that_attributes_cannot_be_added(self):
        node = Node()
        with assert_raises(AttributeError):
            node.foo = "bar"

    def test_symmetric_input_output_assignment(self):
        n1 = Node(label="<N1>")

        n2 = Node(label="<From N1>", inputs=[n1])
        ok_(n1 in n2.inputs,
            "{0} not in {1}.inputs, ".format(n1, n2) +
            "although it should be by construction.")
        ok_(n2 in n1.outputs,
            "{0} in {1}.inputs but {1} not in {0}.outputs.".format(n1, n2))

        n3 = Node(label="<To N1>", outputs=[n1])
        ok_(n1 in n3.outputs,
            "{0} not in {1}.outputs, ".format(n1, n3) +
            "although it should be by construction.")
        ok_(n3 in n1.inputs,
            "{0} in {1}.outputs but {1} not in {0}.inputs.".format(n1, n3))


