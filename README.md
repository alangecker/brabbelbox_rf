# brabbelbox_rf

Implements the SDR part of brabbelbox project: Sticking gnuradio blocks together to do a simultaneous multi stream FM transmission.

## System requirements

* Gnuradio 3.8 (but should also run on 3.7)
* osmocom compatible SDR, the code might be tuned for hackrf but should easily be portable

## What does it do
* Take N audio streams from a sound card (N being around 3..8)
* Modulate them on adjustable frequencies in a 6..8 MHz band (even more if you throw enough computing power at it)

## What still needs to be done
* API to set frequencies
* Care about low latency: Provide HackRF patches to lower buffer size
* Use a gnuradio source that provides adaptive resampling (e.g. add zita-resampler to the gr-audio jack source)

## How to use it?
When you open the gnuradio file `polyphase_single.grc` you have a not too complex flow graph:
* variable `aud_rate`: Sets audio sampling rate (suggest to use 48 kHz everywhere)
* variable `mod_rate`: Sets the sampling rate used for modulation (use at least 200 kHz for wide band FM), will also define the channel spacing
* variable `num_banks`: Sets the number of available channels. `mod_rate` x `num_banks` sets the RF bandwidth that will be sent by your SDR. (Suggest to use 4..20 MHz with HackRF)
* variable `taps`: fine tune low pass filter used in polyphase synthesizer. If you want to change something, you already know why and what :-)
* variable `taps_rs`: fine tune low pass filter used in rational resampler (audio -> modulation resampler). Shouldn't need touching as well.
* Audio source on the left: Multi channel audio source
* resampler, WBFM transmit blocks: These out of the box gnuradio blocks perform really good and shouldn't need any modifications.
* polyphase synthesizer: This block performs the magic of combining all the fm signals together.
  * taps: The filter here is responsible to provide a clear channel separation without destroying the usable signal. 
  * Channel map: Define the relationship of the connected channels to the transmission frequencies. Channel 0 is transmitted on 0 Hz (e.g. center frequency), channel 1 on 0+`mod_rate` (e.g. 200 kHz), channel `num_banks`/2 is on both ends of the spectrum (so shouldn't be used) and `num_banks`/2+1 starts at the lower end, whereby `num_banks`-1 is on 0-`mod_rate`, e.g. -200 kHz.
* osmocom sink: Set your SDR parameters here.
  * hackrf likes to transmit a signal at least 2 MHz wide, better a bit wider
  * use the device argument `buffers=1` for a decreased latency
  * set the frequency to your center frequency
  * tune the transmission power with RF gain (0 or 14 dB TX amplifier) and IF Gain (0..42 dB in 1 dB increments)

Never ever connect your SDR to an antenna as this might be illegal in your country! Always use a dummy load or a direct connection to another SDR for receiving (make sure to use a low transmission power to not brick your second SDR).

## Performance figures
* 30 banks, 3 channels use a bit more than 1 core of a Raspberry Pi 4B with full CPU load
  * polyphase synthesizer uses ~75 % of one core
  * each channel uses just under 10 % of one core additionally
  * hack rf data transmission uses another 10 %
