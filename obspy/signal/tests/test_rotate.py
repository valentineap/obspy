#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The Rotate test suite.
"""

from obspy.signal import rotate_NE_RT, rotate_RT_NE, rotate_ZNE_LQT, \
    rotate_LQT_ZNE
import numpy as np
import os
import unittest


class RotateTestCase(unittest.TestCase):
    """
    Test cases for Rotate.
    """
    def setUp(self):
        # directory where the test files are located
        self.path = os.path.join(os.path.dirname(__file__), 'data')

    def test_rotate_NE_RTVsPitsa(self):
        """
        Test horizontal component rotation against PITSA.
        """
        # load test files
        data_n = np.loadtxt(os.path.join(self.path, 'rjob_20051006_n.gz'))
        data_e = np.loadtxt(os.path.join(self.path, 'rjob_20051006_e.gz'))
        #test different angles, one from each sector
        for angle in [30, 115, 185, 305]:
            # rotate traces
            datcorr_r, datcorr_t = rotate_NE_RT(data_n, data_e, angle)
            # load pitsa files
            data_pitsa_r = np.loadtxt(os.path.join(self.path,
                'rjob_20051006_r_%sdeg.gz' % angle))
            data_pitsa_t = np.loadtxt(os.path.join(self.path,
                'rjob_20051006_t_%sdeg.gz' % angle))
            # Assert.
            np.testing.assert_allclose(datcorr_r, data_pitsa_r, rtol=1E-3,
                atol=1E-5)
            np.testing.assert_allclose(datcorr_t, data_pitsa_t, rtol=1E-3,
                atol=1E-5)

    def test_rotate_ZNE_LQTVsPitsa(self):
        """
        Test LQT component rotation against PITSA. Test back-rotation.
        """
        # load test files
        data_z = np.loadtxt(os.path.join(self.path, 'rjob_20051006.gz'))
        data_n = np.loadtxt(os.path.join(self.path, 'rjob_20051006_n.gz'))
        data_e = np.loadtxt(os.path.join(self.path, 'rjob_20051006_e.gz'))
        # test different backazimuth/incidence combinations
        for ba, inci in ((60, 130), (210, 60)):
            # rotate traces
            data_l, data_q, data_t = \
                rotate_ZNE_LQT(data_z, data_n, data_e, ba, inci)
            # rotate traces back to ZNE
            data_back_z, data_back_n, data_back_e = \
                rotate_LQT_ZNE(data_l, data_q, data_t, ba, inci)
            # load pitsa files
            data_pitsa_l = np.loadtxt(os.path.join(self.path,
                'rjob_20051006_l_%sba_%sinc.gz' % (ba, inci)))
            data_pitsa_q = np.loadtxt(os.path.join(self.path,
                'rjob_20051006_q_%sba_%sinc.gz' % (ba, inci)))
            data_pitsa_t = np.loadtxt(os.path.join(self.path,
                'rjob_20051006_t_%sba_%sinc.gz' % (ba, inci)))
            # Assert the output. Has to be to rather low accuracy due to
            # rounding error prone rotation and single precision value.
            np.testing.assert_allclose(data_l, data_pitsa_l, rtol=1E-3,
                atol=1E-5)
            np.testing.assert_allclose(data_q, data_pitsa_q, rtol=1E-3,
                atol=1E-5)
            np.testing.assert_allclose(data_t, data_pitsa_t, rtol=1E-3,
                atol=1E-5)
            np.testing.assert_allclose(data_z, data_back_z, rtol=1E-3,
                atol=1E-5)
            np.testing.assert_allclose(data_n, data_back_n, rtol=1E-3,
                atol=1E-5)
            np.testing.assert_allclose(data_e, data_back_e, rtol=1E-3,
                atol=1E-5)

    def test_rotate_NE_RT_NE(self):
        """
        Rotating there and back with the same back-azimuth should not change
        the data.
        """
        # load the data
        data_n = np.loadtxt(os.path.join(self.path, 'rjob_20051006_n.gz'))
        data_e = np.loadtxt(os.path.join(self.path, 'rjob_20051006_e.gz'))
        # Use double precision to get more accuracy for testing.
        data_n = np.require(data_n, "float64")
        data_e = np.require(data_e, "float64")
        ba = 33.3
        new_n, new_e = rotate_NE_RT(data_n, data_e, ba)
        new_n, new_e = rotate_RT_NE(new_n, new_e, ba)
        np.testing.assert_allclose(data_n, new_n, rtol=1E-7, atol=1E-12)
        np.testing.assert_allclose(data_e, new_e, rtol=1E-7, atol=1E-12)


def suite():
    return unittest.makeSuite(RotateTestCase, 'test')


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
