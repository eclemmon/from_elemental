VSTPlugin.search;

QuarksGui.new;

Platform.userExtensionDir;
VSTPlugin.search;

(
SynthDef(\input, {
	arg input=0, output=99;
	var in = SoundIn.ar(input);
	Out.ar(output, in);
}).add;

SynthDef(\vocoder, {
	arg input=99, output=0;
	var in = In.ar(input);
	Out.ar(output, VSTPlugin.ar(in, 2, id: \vocoder));
}).add;
)

~vocoderBus = Bus.audio(s, 2);

~vocoder = VSTPluginController(Synth(\vocoder, [\in, ~vocoderBus, \out, 0]), id: \vocoder);
~vocoder.open("TAL-Vocoder-2", editor: true, verbose:true);
~vocoder.editor;

Synth(\input, [\output, ~vocoderBus]);

(
if ((~grable != nil), {
	"true".postln;
}, {
	"false".postln;
});
)

MIDIFunc.trace(false);

(
SynthDef('help-dynKlank', { |out,
    freqs (#[100, 200, 300, 400]),
    amps (#[1, 0.3, 0.2, 0.05]),
    rings (#[1, 1, 1, 2])|

    Out.ar(out, DynKlank.ar(`[freqs, amps, rings], WhiteNoise.ar * 0.001))
}).add
)
a = Synth('help-dynKlank');
a.setn(\freqs, Array.rand(4, 500, 2000));
{ Out.kr(102, MouseX.kr(1, 2) * Array.rand(4, 500, 2000)) }.play;
a.mapn(\freqs, 102, 4);

(
z = {
    BLowPass.ar(
        WhiteNoise.ar,
        MouseX.kr(10, 20000, \exponential), // cutoff freq.
        MouseY.kr(0.0, 1.0, \linear), // rq
        0.5); // mul
}.play
)
Array.fill([2, 2, 3], { arg i, j, k;  i * 100 + (j * 10) + k });
(
z = {
RLPF.ar(
		WhiteNoise.ar,
		MouseX.kr(20, Server.default.sampleRate/2, 1),
		MouseY.kr(0.2, 1),
		mul: 1/MouseY.kr(0.5,1).sqrt
	);

}.play)

{ WhiteNoise.ar }.play;

{Disintegrator.ar(SinOsc.ar([400, 404], 0, 0.2), MouseX.kr(0, 1), MouseY.kr(0, 1))}.play
(
var freq_array = [100, 200, 400, 800, 1600, 3200, 6400, 20];
var rq_array = [0.1] ++ Array.fill(7, {arg i; 0.9});
{ var noise = WhiteNoise.ar; Out.ar(99, noise) }.play;
// Synth(\filterBank, [\freq_array, freq_array, \rq_array, rq_array]);
Synth(\hpf, [\freq, freq_array[6], \rq, rq_array[0], \amp, 0.2, \output, 98]);
Synth(\lpf, [\freq, freq_array[0], \rq, rq_array[0], \amp, 0.2, \output, 0]);
)

(
SynthDef("help-Synth-get", { | out, freq = 440|
    Out.ar(out, SinOsc.ar(freq, 0, 0.1));
}).add;
)
x = Synth("help-Synth-get");
x.set(\freq, 220 + 440.rand);
y = x.get(\freq, { arg value; value; });
y.postln
x.free;

