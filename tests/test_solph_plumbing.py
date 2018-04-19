from nose.tools import eq_, assert_raises
from oemof.solph.plumbing import sequence


class Sequence_Mathematical_Tests:
    def setup(self):
        # Default sequence
        self.sd = sequence(2)

        # Changed default sequence [3, 2, 3, ...]
        self.sdc = sequence(3)
        self.sdc[1] = 2

        # Long changed default sequence [3, 3, 3, 3, 3, 3, 3, 2, 3, ...]
        self.sdcl = sequence(3)
        self.sdcl[7] = 2

        # Real sequence
        self.sr = sequence([1, 2, 3])

    def test_addition_of_2_defaults(self):
        eq_((self.sd + self.sd).default, 4)

    def test_addition_with_default_changed(self):
        addition_sd_sdc = self.sd + self.sdc
        eq_(addition_sd_sdc, [5, 4])
        eq_(addition_sd_sdc[3], 5)

        addition_sdc_sd = self.sdc + self.sd
        eq_(addition_sdc_sd, [5, 4])
        eq_(addition_sdc_sd[3], 5)
        eq_(addition_sdc_sd, [5, 4, 5, 5])

        sdc2 = sequence(4)  # [4, 4, 4, 4, 4, 1, 4, ...]
        sdc2[2] = 1
        addition_sdc_sdc = self.sdc + sdc2
        eq_(addition_sdc_sdc, [7, 6, 4])
        eq_(addition_sdc_sdc[4], 7)
        eq_(addition_sdc_sdc, [7, 6, 4, 7, 7])

    def test_addition_with_real_list(self):
        add_sd_sr = self.sd + self.sr
        eq_(add_sd_sr, [3, 4, 5])
        with assert_raises(IndexError):
            eq_(add_sd_sr[3], None)

        add_sdc_sr = self.sr + self.sdc
        eq_(add_sdc_sr, [4, 4, 6])
        with assert_raises(IndexError):
            eq_(add_sd_sr[3], None)

        with assert_raises(IndexError):
            _ = self.sr + self.sdcl

        add_sr_sr = self.sr + self.sr
        eq_(add_sr_sr, [2, 4, 6])

    def test_multiplication_of_2_defaults(self):
        eq_((self.sd * self.sd).default, 4)

    def test_multiplication_with_default_changed(self):
        mul_sd_sdc = self.sd * self.sdc
        eq_(mul_sd_sdc, [6, 4])
        eq_(mul_sd_sdc[3], 6)

        mul_sdc_sd = self.sdc * self.sd
        eq_(mul_sdc_sd, [6, 4])
        eq_(mul_sdc_sd[3], 6)
        eq_(mul_sdc_sd, [6, 4, 6, 6])

        sdc2 = sequence(4)  # [4, 4, 4, 4, 4, 1, 4, ...]
        sdc2[2] = 1
        mul_sdc_sdc = self.sdc * sdc2
        eq_(mul_sdc_sdc, [12, 8, 3])
        eq_(mul_sdc_sdc[4], 12)
        eq_(mul_sdc_sdc, [12, 8, 3, 12, 12])
