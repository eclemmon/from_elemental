// Cosmos

(
s = Server.default;
s.waitForBoot(
	{
		var knob_note_numbers, root;
		// PRINT WHAT THIS BANK DOES
		"8. PLAYBACK OF BASE SAMPLES ### MIDI_control_bank_2.scd ###".postln;
		root = PathName(PathName(thisProcess.nowExecutingPath.asString.dirname).parentPath).parentPath;

		// Load SynthDefs
		thisProcess.interpreter.executeFile(root +/+ "program_files/synthdefs.scd");

		// Boot GUI
		thisProcess.interpreter.executeFile(root +/+ "program_files/GUI_files/MIDI_control_bank_1_GUI.scd");

		// Constants for Arturia Midi Controller
		knob_note_numbers = ~gm.at(\knob_note_numbers);

		if ((~gm.at(\bank_2_vals) == nil), {
			var current_vals, cosmic_sample;
			// If no \bank_2_vals key, instantiate
			current_vals = ~gm.atFail(\bank_2_vals, {Dictionary.new});
			~gm.put(\bank_2_vals, current_vals);

			// Load path to ether/cosmic sample
			cosmic_sample = PathName.new(root +/+ "sample_files/long_elemental_samples/ether_ecl.wav");

			// Initialize cosmos buffer
			~gm.at(\bank_2_vals).put(\cosmos_buffer, Buffer.read(s, cosmic_sample.fullPath));

			// Wait a little for the buffer to be read
			0.1.wait;

			// Initialize lpf
			~gm.at(\bank_2_vals).put(\lpf, Synth(\lpf_2ch,
				[
					\amp, ~gm.at(\bank_2_vals).atFail(1, 0),
					\input, 98,
					\output, 0,
					\freq, ~gm.at(\bank_2_vals).atFail(\lpf_freq, 20000),
					\rq, ~gm.at(\bank_2_vals).atFail(\lpf_rq, 1)
				]
			));

			~gm.at(\bank_2_vals).put(\audio_router_1, Synth(\audio_router_2ch,
				[
					\amp, ~gm.at(\bank_2_vals).atFail(1, 0),
					\input, 100,
					\output, 98
				]
			));

			// Initialize delays
			~gm.at(\bank_2_vals).put(\delays,
				Array.fill(3, {
					arg i;
					var item = (i + 1) * 0.5;
					Synth(\delay_2ch,
						[
							\amp, ~gm.at(\bank_2_vals).atFail(1, 0),
							\input, 100,
							\output, 98,
							\delaytime, item
						]
					);
				});
			);

			// Initialize cosmos synth
			~gm.at(\bank_2_vals).put(\cosmos_play_buf,
				Synth(\playBuf_2ch,
					[
						\buffer, ~gm.at(\bank_2_vals).at(\cosmos_buffer),
						\loop, 1,
						\amp, ~gm.at(\bank_2_vals).atFail(1, 0),
						\gate, -1,
						\output, 100
					]
			));

			~gm.at(\bank_2_vals).put(\cosmos_pb_gate, -1);
		});
	};
);

MIDIdef.noteOn(\noteOn, {
	arg velocity, note_number, chan, src;
	var array_index = note_number-48;
	var cosmos_pb_gate = ~gm.at(\bank_2_vals).at(\cosmos_pb_gate);
	[velocity, note_number, chan, src].postln;
	// Plays back a recorded file
	if ((cosmos_pb_gate <= 0), {
		~gm.at(\bank_2_vals).at(\cosmos_play_buf).set(\gate, 1);
		~gm.at(\bank_2_vals).put(\cosmos_pb_gate, 1);
	}, {
		~gm.at(\bank_2_vals).at(\cosmos_play_buf).set(\gate, -1);
		~gm.at(\bank_2_vals).put(\cosmos_pb_gate, -1);
	});
}, (48..82));

MIDIdef.cc(\volume_control, {
	arg val, note_number, chan, src;
	~gm.at(\bank_2_vals).put(note_number, val);
	~gm.at(\bank_2_vals).at(\cosmos_play_buf).set(\amp, ~gm.at(\bank_2_vals).at(note_number));
	~gm.at(\bank_2_vals).at(\lpf).set(\amp, ~gm.at(\bank_2_vals).at(note_number));
	~gm.at(\bank_2_vals).at(\audio_router_1).set(\amp, ~gm.at(\bank_2_vals).at(note_number));
	{
		~volume_midi_control.value(~slider, val);
	}.defer;
}, 1);

MIDIdef.cc(\knob_control, {
	arg val, note_number, chan, src;
	{
		~knob_midi_control.value(~knobs, ~gm.at(\knob_note_numbers).indexOf(note_number), val);
	}.defer;
}, ~gm.at(\knob_note_numbers));

MIDIdef.cc(\lpf_freq_control, {
	arg val, note_number, chan, src;
	~gm.at(\bank_2_vals).put(\lpf_freq, val.linexp(0, 127, 20, 2700));
	~gm.at(\bank_2_vals).at(\lpf).set(\freq, ~gm.at(\bank_2_vals).at(\lpf_freq));
}, ~gm.at(\knob_note_numbers)[0]);

MIDIdef.cc(\lpf_rq_control, {
	arg val, note_number, chan, src;
	~gm.at(\bank_2_vals).put(\lpf_rq, val.linexp(0, 127, 0.5, 8));
	~gm.at(\bank_2_vals).at(\lpf).set(\rq, ~gm.at(\bank_2_vals).at(\lpf_rq));
}, ~gm.at(\knob_note_numbers)[8]);

MIDIdef.cc(\lpf_freq_control, {
	arg val, note_number, chan, src;
	~gm.at(\bank_2_vals).put(\lpf_freq, val.linexp(0, 127, 20, 2700));
	~gm.at(\bank_2_vals).at(\lpf).set(\freq, ~gm.at(\bank_2_vals).at(\lpf_freq));
}, ~gm.at(\knob_note_numbers)[0]);

3.do({
	arg i;
	var time_name = \delay_ ++ i ++ "_time";
	var amp_name = \delay_ ++ i ++ "_amp";
	MIDIdef.cc(time_name ++ "_control", {
		arg val, note_number, chan, src;
		~gm.at(\bank_2_vals).put(time_name, val.linlin(0, 127, 0.5, 8));
		~gm.at(\bank_2_vals).at(\delays)[i].set(\delay_time, ~gm.at(\bank_2_vals).at(time_name));
	}, ~gm.at(\knob_note_numbers)[i+1]);

	MIDIdef.cc(amp_name ++ "_control", {
		arg val, note_number, chan, src;
		~gm.at(\bank_2_vals).put(amp_name, val.linlin(0, 127, 0, 1));
		~gm.at(\bank_2_vals).at(\delays)[i].set(\amp, ~gm.at(\bank_2_vals).at(amp_name));
	}, ~gm.at(\knob_note_numbers)[i+9]);
}
);

MIDIdef.noteOff(\noteOff, {
	arg velocity, note_number;
	var array_index = note_number-36;
	// [velocity, note_number].postln;
});

// MIDIdef to control synth selection
MIDIdef.cc(\synth_select, {
	arg val, note_number, chan, src;
	var index = note_number - 44;
	if (val == 127, {
		{
			~button_midi_control.value(~buttons, index);
		}.defer;
	});
}, ~gm.at(\buttons));


)

