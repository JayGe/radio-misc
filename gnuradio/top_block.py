#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Sat Sep 27 00:08:20 2014
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 8e6
        self.lo = lo = 0
        self.level = level = 1
        self.hi = hi = 0
        self.fsk_deviation_hz = fsk_deviation_hz = 186000
        self.channel_freq = channel_freq = 433910000
        self.centre_freq = centre_freq = 432000000

        ##################################################
        # Blocks
        ##################################################
        _lo_sizer = wx.BoxSizer(wx.VERTICAL)
        self._lo_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_lo_sizer,
        	value=self.lo,
        	callback=self.set_lo,
        	label="Low",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._lo_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_lo_sizer,
        	value=self.lo,
        	callback=self.set_lo,
        	minimum=-1e6,
        	maximum=1e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_lo_sizer)
        _hi_sizer = wx.BoxSizer(wx.VERTICAL)
        self._hi_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_hi_sizer,
        	value=self.hi,
        	callback=self.set_hi,
        	label="High",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._hi_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_hi_sizer,
        	value=self.hi,
        	callback=self.set_hi,
        	minimum=-1e6,
        	maximum=1e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_hi_sizer)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=True,
        	xy_mode=False,
        	num_inputs=4,
        	trig_mode=wxgui.TRIG_MODE_NORM,
        	y_axis_label="Counts",
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        _level_sizer = wx.BoxSizer(wx.VERTICAL)
        self._level_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_level_sizer,
        	value=self.level,
        	callback=self.set_level,
        	label="Level",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._level_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_level_sizer,
        	value=self.level,
        	callback=self.set_level,
        	minimum=0,
        	maximum=10,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_level_sizer)
        self.blocks_throttle_0_1 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(lo, hi, 0)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((10, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "something.sink", True)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(samp_rate, analog.GR_CONST_WAVE, 0, hi, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_CONST_WAVE, 0, lo, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, centre_freq-channel_freq, 1, 0)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/(2*math.pi*fsk_deviation_hz/8.0))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.wxgui_scopesink2_0, 1))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.wxgui_scopesink2_0, 3))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_throttle_0_1, 0))
        self.connect((self.blocks_throttle_0_1, 0), (self.wxgui_scopesink2_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.wxgui_fftsink2_0, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_1.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0))

    def get_lo(self):
        return self.lo

    def set_lo(self, lo):
        self.lo = lo
        self._lo_slider.set_value(self.lo)
        self._lo_text_box.set_value(self.lo)
        self.analog_sig_source_x_0_0.set_amplitude(self.lo)
        self.blocks_threshold_ff_0.set_lo(self.lo)

    def get_level(self):
        return self.level

    def set_level(self, level):
        self.level = level
        self._level_slider.set_value(self.level)
        self._level_text_box.set_value(self.level)

    def get_hi(self):
        return self.hi

    def set_hi(self, hi):
        self.hi = hi
        self._hi_slider.set_value(self.hi)
        self._hi_text_box.set_value(self.hi)
        self.analog_sig_source_x_0_0_0.set_amplitude(self.hi)
        self.blocks_threshold_ff_0.set_hi(self.hi)

    def get_fsk_deviation_hz(self):
        return self.fsk_deviation_hz

    def set_fsk_deviation_hz(self, fsk_deviation_hz):
        self.fsk_deviation_hz = fsk_deviation_hz
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/(2*math.pi*self.fsk_deviation_hz/8.0))

    def get_channel_freq(self):
        return self.channel_freq

    def set_channel_freq(self, channel_freq):
        self.channel_freq = channel_freq
        self.analog_sig_source_x_0.set_frequency(self.centre_freq-self.channel_freq)

    def get_centre_freq(self):
        return self.centre_freq

    def set_centre_freq(self, centre_freq):
        self.centre_freq = centre_freq
        self.analog_sig_source_x_0.set_frequency(self.centre_freq-self.channel_freq)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = top_block()
    tb.Start(True)
    tb.Wait()
