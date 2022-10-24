MIDIClient.init;
MIDIIn.connectAll;

MIDIFunc.trace(false);
MIDIFunc.trace(true);

(
(
MIDIdef.noteOn(\noteOnTest, {
	arg velocity, note_number, chan, src;
	[velocity, note_number].postln;
	~notes.put(note_number, Synth.new(
		\tone,
		[
			\freq, note_number.midicps,
			\amp, velocity.linexp(1,127,0.01, 0.03),
			\gate, 1
			// \bend, ~bend.linlin(0, 16383,-2,2)
		]
	);
	);
});
);


MIDIdef.noteOff(\noteOffTest, {
	arg velocity, note_number;
	[velocity, note_number].postln;
	~notes.at(note_number).set(\gate, 0);
	~notes.put(note_number, nil);
});

MIDIdef.bend(\bendTest, {
	arg val, chan, src;
	[val, chan, src].postln;
	~bend = val;
	~notes.do{arg synth; synth.set(\bend, val.linlin(0, 16383, -2,2))};
}, chan:0);


(
SynthDef.new(\tone, {
	arg freq=440, amp=0.3, gate=0, bend=0;
	var sig, env;
	sig = SinOsc.ar(freq * bend.midiratio)!2;
	env = EnvGen.kr(Env.adsr, gate, doneAction:2);
	sig = sig * env * amp;
	Out.ar(0, sig);

}).add;
);

~notes = Array.fill(128, nil);
)