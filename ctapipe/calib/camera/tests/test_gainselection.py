import numpy as np
from ctapipe.calib.camera.gainselection import ManualGainSelector, \
    ThresholdGainSelector, GainChannel, GainSelector


class TestGainSelector(GainSelector):
    def select_channel(self, waveforms):
        return GainChannel.HIGH


def test_gain_selector():
    shape = (2, 2048, 128)
    waveforms = np.indices(shape)[1]
    waveforms[1] *= 2

    gs = TestGainSelector()
    waveforms_gs = gs(waveforms)
    np.testing.assert_equal(waveforms[GainChannel.HIGH], waveforms_gs)
    waveforms_gs = gs(waveforms[0])
    np.testing.assert_equal(waveforms_gs, waveforms[0])
    waveforms_gs = gs(waveforms[[0]])
    np.testing.assert_equal(waveforms_gs, waveforms[0])


def test_manual_gain_selector():
    shape = (2, 2048, 128)
    waveforms = np.indices(shape)[1]
    waveforms[1] *= 2

    gs_high = ManualGainSelector(channel="HIGH")
    waveforms_gs_high = gs_high(waveforms)
    np.testing.assert_equal(waveforms[GainChannel.HIGH], waveforms_gs_high)

    gs_high = ManualGainSelector(channel="LOW")
    waveforms_gs_low = gs_high(waveforms)
    np.testing.assert_equal(waveforms[GainChannel.LOW], waveforms_gs_low)


def test_threshold_gain_selector():
    shape = (2, 2048, 128)
    waveforms = np.zeros(shape)
    waveforms[1] = 1
    waveforms[0, 0] = 100

    gs = ThresholdGainSelector(threshold=50)
    waveforms_gs = gs(waveforms)
    assert (waveforms_gs[0] == 1).all()
    assert (waveforms_gs[np.arange(1, 2048)] == 0).all()
