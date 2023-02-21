#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: multi_fm_transmit
# Author: matthias
# GNU Radio version: 3.10.5.0

from gnuradio import analog
from gnuradio import audio
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time




class polyphase(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "multi_fm_transmit", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.num_banks = num_banks = 30
        self.mod_rate = mod_rate = 200000
        self.taps_rs = taps_rs = firdes.low_pass_2(25.0, 25.0, 0.1, 0.1, 60, window.WIN_KAISER, 7.0)
        self.taps = taps = firdes.low_pass_2(8, num_banks*mod_rate, 120e3, 50e3, 80, window.WIN_BLACKMAN_HARRIS)
        self.aud_rate = aud_rate = 48000

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_fff(
                interpolation=25,
                decimation=6,
                taps=taps_rs,
                fractional_bw=0.3)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=25,
                decimation=6,
                taps=taps_rs,
                fractional_bw=0.3)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=25,
                decimation=6,
                taps=taps_rs,
                fractional_bw=0.3)
        self.pfb_synthesizer_ccf_0 = filter.pfb_synthesizer_ccf(
            num_banks,
            taps,
            False)
        self.pfb_synthesizer_ccf_0.set_channel_map([1,9,8])
        self.pfb_synthesizer_ccf_0.declare_sample_delay(0)
        self.osmosdr_sink_1 = osmosdr.sink(
            args="numchan=" + str(1) + " " + "buffers=1"
        )
        self.osmosdr_sink_1.set_sample_rate(mod_rate*num_banks)
        self.osmosdr_sink_1.set_center_freq(96000000, 0)
        self.osmosdr_sink_1.set_freq_corr(0, 0)
        self.osmosdr_sink_1.set_gain(0, 0)
        self.osmosdr_sink_1.set_if_gain(0, 0)
        self.osmosdr_sink_1.set_bb_gain(0, 0)
        self.osmosdr_sink_1.set_antenna('', 0)
        self.osmosdr_sink_1.set_bandwidth(0, 0)
        self.audio_source_0 = audio.source(aud_rate, 'plughw:UMC1820', False)
        self.analog_wfm_tx_0_0_0 = analog.wfm_tx(
        	audio_rate=mod_rate,
        	quad_rate=mod_rate,
        	tau=(75e-6),
        	max_dev=75e3,
        	fh=10e3,
        )
        self.analog_wfm_tx_0_0 = analog.wfm_tx(
        	audio_rate=mod_rate,
        	quad_rate=mod_rate,
        	tau=(75e-6),
        	max_dev=75e3,
        	fh=10e3,
        )
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=mod_rate,
        	quad_rate=mod_rate,
        	tau=(75e-6),
        	max_dev=75e3,
        	fh=10e3,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.pfb_synthesizer_ccf_0, 0))
        self.connect((self.analog_wfm_tx_0_0, 0), (self.pfb_synthesizer_ccf_0, 1))
        self.connect((self.analog_wfm_tx_0_0_0, 0), (self.pfb_synthesizer_ccf_0, 2))
        self.connect((self.audio_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.audio_source_0, 1), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.audio_source_0, 2), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.pfb_synthesizer_ccf_0, 0), (self.osmosdr_sink_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_wfm_tx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.analog_wfm_tx_0_0_0, 0))


    def get_num_banks(self):
        return self.num_banks

    def set_num_banks(self, num_banks):
        self.num_banks = num_banks
        self.set_taps(firdes.low_pass_2(8, self.num_banks*self.mod_rate, 120e3, 50e3, 80, window.WIN_BLACKMAN_HARRIS))
        self.osmosdr_sink_1.set_sample_rate((self.mod_rate*self.num_banks))

    def get_mod_rate(self):
        return self.mod_rate

    def set_mod_rate(self, mod_rate):
        self.mod_rate = mod_rate
        self.set_taps(firdes.low_pass_2(8, self.num_banks*self.mod_rate, 120e3, 50e3, 80, window.WIN_BLACKMAN_HARRIS))
        self.osmosdr_sink_1.set_sample_rate((self.mod_rate*self.num_banks))

    def get_taps_rs(self):
        return self.taps_rs

    def set_taps_rs(self, taps_rs):
        self.taps_rs = taps_rs
        self.rational_resampler_xxx_0.set_taps(self.taps_rs)
        self.rational_resampler_xxx_0_0.set_taps(self.taps_rs)
        self.rational_resampler_xxx_0_0_0.set_taps(self.taps_rs)

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps
        self.pfb_synthesizer_ccf_0.set_taps(self.taps)

    def get_aud_rate(self):
        return self.aud_rate

    def set_aud_rate(self, aud_rate):
        self.aud_rate = aud_rate




def main(top_block_cls=polyphase, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start(200000)

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
