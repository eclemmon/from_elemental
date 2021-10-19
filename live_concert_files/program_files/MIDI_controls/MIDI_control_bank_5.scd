// (
// SynthDef(\square_vocoder, {
// 	arg input=0, output=0, amp=0.1, midi_freq=36, key_code=0, gate=0;
// 	var inA, chainA, inB, chainB, chain, sig, env, noiseGate;
// 	inA = PulseDPW.ar(midi_freq.midicps);
// 	inB = SoundIn.ar(input, 0.5);
// 	noiseGate = Compander.ar(in: inB, thresh: 0.5, slopeBelow: 10, slopeAbove: 1, clampTime: 0.01, relaxTime: 0.01);
// 	chainA = FFT(LocalBuf(2048), inA);
// 	chainB = FFT(LocalBuf(2048), noiseGate);
// 	chain = PV_MagMul(chainA, chainB); // writes into bufferA
// 	env = EnvGen.kr(Env.adsr, gate, doneAction:2);
// 	sig = IFFT(chain) * 0.1 * env;
// 	Out.ar(output, sig.dup);
// }).add;
// )
//
// (
// (
// MIDIdef.noteOn(\noteOnTest, {
// 	arg velocity, note_number, chan, src;
// 	[velocity, note_number].postln;
// 	~notes.put(note_number, Synth.new(
// 		\square_vocoder,
// 		[
// 			\midi_freq, note_number,
// 			\amp, velocity.linexp(1,127,0.01, 0.03),
// 			\gate, 1
// 			// \bend, ~bend.linlin(0, 16383,-2,2)
// 		]
// 		);
// 	);
// });
// );
//
// MIDIdef.noteOff(\noteOffTest, {
// 	arg velocity, note_number;
// 	[velocity, note_number].postln;
// 	~notes.at(note_number).set(\gate, 0);
// 	~notes.put(note_number, nil);
// });
//
// MIDIdef.bend(\bendTest, {
// 	arg val, chan, src;
// 	[val, chan, src].postln;
// 	~bend = val;
// 	~notes.do{arg synth; synth.set(\bend, val.linlin(0, 16383, -2,2))};
// }, chan:0);
//
// /*
// (
// SynthDef.new(\tone, {
// arg freq=440, amp=0.3, gate=0, bend=0;
// var sig, env;
// sig = SinOsc.ar(freq * bend.midiratio)!2;
// env = EnvGen.kr(Env.adsr, gate, doneAction:2);
// sig = sig * env * amp;
// Out.ar(0, sig);
//
// }).add;
// );*/
//
// ~notes = Array.fill(128, nil);
// )