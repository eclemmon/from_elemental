// GRANULATION OF RECORDED BUFFERS

(
var boot;
// s = Server.default;
~server.waitForBoot(
	{
		// PRINT WHAT THIS BANK DOES
		"8. GRANULATION OF RECORDED SOUNDS ### MIDI_control_bank_8.scd ###".postln;

		// Initialize midi control bank memory
		~gm.atFail(\bank_8_vals, {~gm.put(\bank_8_vals, Dictionary.new)});

		// Load SynthDefs
		thisProcess.interpreter.executeFile("/Users/ericlemmon/Desktop/NMFS_collab/sc_files/Live_Concert_Files/program_files/synthdefs.scd");

		// Boot GUI
		thisProcess.interpreter.executeFile("/Users/ericlemmon/Desktop/NMFS_collab/sc_files/Live_Concert_Files/program_files/GUI_files/MIDI_control_bank_8_GUI.scd");

		~buf_list = List.fill(8, {arg i;
			var buffer;
			buffer = Buffer.alloc(~server, ~sampleRate * ~recording_duration, 1);
		});

		// Initialize (or re-initialize record buf synths)
		~record_buf_group.free;
		~record_buf_group = Group.new;
		~record_buf_synths = List.fill(8, {arg i;
			Synth(\recordBuf, [\buffer, ~buf_list[i], \run, 0, \trigger, -1, \input, ~input[0]], ~record_buf_group)
		});

		// Fill an list with nils so that granulation synths can be set, and any triggers of empty synths pass silently
		~grain_buf_synths = List.fill(8, {arg i;
			nil
		});

		// Constants for Arturia Midi Controller
		~current_vals = Dictionary.new;
		~top_row = [112, 74, 71, 76, 77, 93, 73, 75];
		~bottom_row = [114, 18, 19, 16, 17, 91, 79, 72];
	};
);

MIDIdef.noteOn(\noteOn, {
	arg velocity, note_number, chan, src;
	var array_index = note_number-36;
	// [velocity, note_number, chan, src].postln;
	// Begins recording into ~buf_list via \recordbuf synth
	if ((note_number >= 36) && (note_number <= 43), {
	~buf_list[array_index].zero;
	~record_buf_synths[array_index].set(\trigger, -1);
	~record_buf_synths[array_index].set(\run, 1, \trigger, 1);
	});
});

MIDIdef.noteOff(\noteOff, {
	arg velocity, note_number;
	var array_index = note_number-36;
	// [velocity, note_number].postln;
	// Stops recording
	~record_buf_synths[array_index].set(\run, 0, \trigger, -1);
	~record_buf_synths[array_index].set(\trigger, 1);
});

MIDIdef.cc(\knob_control, {
	arg val, note_number, chan, src;
	{
		~knob_midi_control.value(~knobs, ~gm.at(\knob_note_numbers).indexOf(note_number), val);
	}.defer;
}, ~gm.at(\knob_note_numbers));



MIDIdef.cc(\knob_control_top, {
	arg val, note_number, chan, src;
	var idx = ~top_row.indexOf(note_number);
	~gm.at(\bank_8_vals).put(note_number, val);
	~grain_buf_synths[idx].set(\rate, ~gm.at(\bank_8_vals).at(note_number));
/*	~current_vals.put(note_number, val);
	~grain_buf_synths[idx].set(\rate, ~current_vals.at(note_number));*/
}, ~gm.at(\knob_note_numbers)[0..7]);

MIDIdef.cc(\knob_control_bottom, {
	arg val, note_number, chan, src;
	var idx = ~bottom_row.indexOf(note_number);
	~gm.at(\bank_8_vals).put(note_number, val);
	~grain_buf_synths[idx].set(\grainDur, ~gm.at(\bank_8_vals).at(note_number));
/*	~current_vals.put(note_number, val);
	~grain_buf_synths[idx].set(\grainDur, ~current_vals.at(note_number));*/
}, ~gm.at(\knob_note_numbers)[8..]);

MIDIdef.cc(\control_play, {
	arg val, note_number, chan, src;
	var array_index = note_number-44;
	[val, note_number, chan, src].postln;

	// CREATE GRAIN BUFFER SYNTHS AND STORE THEM IN GRAIN BUFF SYNTH
	if (val > 50, {
		if ((note_number >= 44) && (note_number <= 51), {
			~grain_buf_synths[array_index] = Synth(\grainBuf,
				[
					\buffer, ~buf_list[array_index],
					\gate, 1,
					\rate, ~gm.at(\bank_8_vals).at(~top_row[array_index]),
					\grainDur, ~gm.at(\bank_8_vals).at(~bottom_row[array_index]),
					// \grainDur, ~current_vals.at(~bottom_row[array_index]),
					\grainTriggerRate, ~gm.at(\bank_8_vals).at(\bend, val),
					\amp, ~gm.at(\bank_8_vals).at(\synth_bank_global_amp)
				]
			).onFree{
				~grain_buf_synths[array_index] = nil;
			};
		});
	});
});

MIDIdef.bend(\bend, {
	arg val, chan, src;
	[val, chan, src].postln;
	~gm.at(\bank_8_vals).put(\bend, val);
	~grain_buf_synths.do({arg item, i; item.set(\grainTriggerRate, ~gm.at(\bank_8_vals).at(\bend, val))});
/*	~current_vals.put("bend", val);
	~grain_buf_synths.do({arg item, i; item.set(\grainTriggerRate, ~current_vals.at("bend"))});*/
	{
		~bend_midi_control.value(~bend_slider, val);
	}.defer;
});

MIDIdef.cc(\volume_control, {
	arg val, note_number, chan, src;
	// var index = note_number - 22;
	~gm.at(\bank_8_vals).put(\synth_bank_global_amp, val);
	~grain_buf_synths.do({arg item, i; item.set(\amp, ~gm.at(\bank_8_vals).at(\synth_bank_global_amp))});
	{
		~volume_midi_control.value(~slider, val);
	}.defer;
}, 1);
)
