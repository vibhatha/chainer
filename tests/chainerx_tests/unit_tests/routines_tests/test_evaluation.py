import chainer
from chainer import functions as F
import numpy

import chainerx

from chainerx_tests import op_utils


_in_out_eval_dtypes = [
    (('float16', 'int16'), 'float32'),
    (('float32', 'int32'), 'float32'),
    (('float64', 'int64'), 'float64'),
    (('float32', 'int16'), 'float32'),
    (('float64', 'int16'), 'float64'),
    (('float64', 'int32'), 'float64'),
]


class EvalBase(op_utils.ChainerOpTest):

    def generate_inputs(self):
        y_dtype, t_dtype = self.in_dtypes
        y = numpy.random.uniform(-1, 1, self.y_shape).astype(y_dtype)
        targ = numpy.random.randint(
            3, size=self.t_shape).astype(t_dtype)
        return y, targ

    def forward_chainerx(self, inputs):
        return self.forward_xp(inputs, chainerx)

    def forward_chainer(self, inputs):
        return self.forward_xp(inputs, F)

    def forward_xp(self, inputs, xp):
        raise NotImplementedError(
            'Op test implementation must override `forward_xp`.')


@op_utils.op_test(['native:0', 'cuda:0'])
@chainer.testing.parameterize(*(
    chainer.testing.product([
        chainer.testing.from_pytest_parameterize(
            'y_shape,t_shape', [
                ((10, 1), (10,)),
                ((5, 1), (5,)),
                ((10, 3), (10,)),
                ((10, 3, 1), (10,)),
                ((10, 3, 1, 1), (10,)),
                ((10, 3, 5), (10, 5)),
                ((10, 3, 5, 4), (10, 5, 4)),
                ((10, 3, 5, 4, 1), (10, 5, 4)),
                ((10, 3, 5, 4, 1, 1), (10, 5, 4))
            ]),
        chainer.testing.from_pytest_parameterize(
            'in_dtypes,out_dtype', _in_out_eval_dtypes),
        chainer.testing.from_pytest_parameterize(
            'ignore_label', [None, 0])
    ])
))
class TestAccuracy(EvalBase):

    skip_backward_test = True
    skip_double_backward_test = True

    def generate_inputs(self):
        y, t = super().generate_inputs()
        # TODO(aksub99): Improve tests for the case
        # where all labels are ignored.
        if y.shape == (10, 1) or y.shape == (5, 1):
            self.ignore_label = 0
        return y, t

    def forward_xp(self, inputs, xp):
        y, t = inputs
        out = xp.accuracy(y, t, self.ignore_label)
        return out,
