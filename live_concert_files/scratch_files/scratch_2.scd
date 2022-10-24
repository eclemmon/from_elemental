SynthDef(\phase_mod, {
	arg amp, freq, mod_freq, mod_mul;
	var env, sig, carrier, modulator;
	env = EnvGen.kr(Env.perc(releaseTime: 20), doneAction: 2);
	modulator = SinOsc.ar(MouseX.kr(20, 15000, 1), mul: MouseY.kr(0.1, 100));
	carrier = SinOsc.ar(freq, phase: modulator);
	sig = carrier * env * amp;
	Out.ar(0, sig!2);
}).add;

Synth(\phase_mod, [\amp, 0.2, \freq, 440]);


SynthDef(\fog_horn, {
	arg out=0, dur=15, amp, attack=0.1, release=0.1, decay_time=0.1, decay_amp=0.7, freq=440, fmod_freq=533, fmod_mul=200, sustain_freq=660, pos=0, trig=0, filter_env_start_freq=880, filter_env_end_freq=440, filter_sus_dur=15, filter_decay_dur=0.1, filter_release_time=0.1, tail_length=4, tail_length_level=0.1;
	var pan, sig, env, filter, carrier, modulator, fmod_env, filter_env;

	// Control Envelopes
	env = EnvGen.kr(
		Env([0,1,decay_amp,1,0],
			[attack, decay_time, dur-attack-release-decay_time-tail_length, tail_length],
			curve: ['wel', -2.0, -3, 0, -4]),
		gate: trig,
		doneAction: Done.freeSelf);
	fmod_env = EnvGen.kr(
		Env([0,1,1,tail_length_level,tail_length_level, 0],
			[attack, (dur/2)-attack-(tail_length/2)-0.1, tail_length, (dur/2)-(tail_length/2), 0.1],
			curve: 'wel'), gate: trig);
	filter_env = EnvGen.kr(
		Env([0.1, filter_env_start_freq, sustain_freq, sustain_freq, filter_env_end_freq],
			[attack, filter_decay_dur, filter_sus_dur-attack-filter_decay_dur-release, filter_release_time],
			curve: -3), gate: trig);

	// Modulator and Carrier
	modulator = SinOsc.ar(fmod_freq, mul: fmod_mul) * fmod_env;

	carrier = SinOsc.ar(freq, modulator);

	// Build signal
	sig = carrier * env;
	filter = LPF.ar(sig, filter_env);
	pan = Pan2.ar(filter, pos: pos, level: amp);
	Out.ar(out, pan);
}).add;

SynthDef(\phase_mod, {
	arg amp, out=0, dur=15, attack=0.1, release=0.1, decay_time=0.1, decay_amp=0.7, freq=440, fmod_freq=533, fmod_mul=12, sustain_freq=660, pos=0, gate=0, filter_env_start_freq=880, filter_env_end_freq=440, filter_sus_dur=15, filter_decay_dur=0.1, filter_release_time=0.1, tail_length=4, tail_length_level=0.1, mRatio=1, cRatio=1;
	var pan, sig, env, filter, carrier, modulator, fmod_env, filter_env;

	// Control Envelopes
	env = EnvGen.kr(
		Env([0,1,decay_amp,1,0],
			[attack, decay_time, dur-attack-release-decay_time-tail_length, tail_length],
			curve: ['wel', -2.0, -3, 0, -4],
			releaseNode: 3
		),
		gate: gate,
		doneAction: Done.freeSelf);
	fmod_env = EnvGen.kr(
		Env([0,1,1,tail_length_level,tail_length_level, 0],
			[attack, (dur/2)-attack-(tail_length/2)-0.1, tail_length, (dur/2)-(tail_length/2), 0.1],
			curve: 'wel',
			releaseNode: 2
		),
		gate: gate);
	filter_env = EnvGen.kr(
		Env([0.1, filter_env_start_freq, sustain_freq, sustain_freq, filter_env_end_freq],
			[attack, filter_decay_dur, filter_sus_dur-attack-filter_decay_dur-release, filter_release_time],
			curve: -3,
			releaseNode: 2
		),
		gate: gate);

	// Modulator and Carrier
	modulator = SinOsc.ar(freq * mRatio, mul: fmod_mul) * fmod_env;
	carrier = SinOsc.ar(freq * cRatio, modulator.wrap(0,4pi));

	// Build signal
	sig = carrier * env;
	filter = LPF.ar(sig, filter_env);
	pan = Pan2.ar(filter, pos: pos, level: amp);
	Out.ar(out, pan);
}).add;

~test = Synth(\phase_mod, [\amp, 1, \gate, 1, \freq, 24.midicps, \out, 99]);
~test.set(\gate, 0);



Synth(\ringModOctaver, [\amp, 0.2, \octave, 0.33]);

