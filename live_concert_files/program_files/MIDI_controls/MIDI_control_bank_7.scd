// STRAIGHT PLAYBACK OF RECORDED FILES

(
/*s = Server.default;*/
~server.waitForBoot(
	{
		// PRINT WHAT THIS BANK DOES
		"7. RECORDED SOUNDS STRAIGHT PLAYBACK ### MIDI_control_bank_7.scd ###".postln;

		// Load SynthDefs
		thisProcess.interpreter.executeFile("/Users/ericlemmon/Desktop/NMFS_collab/sc_files/Live_Concert_Files/program_files/synthdefs.scd");

		if (~buf_list == nil, {
			~buf_list = List.fill(8, {arg i;
				var buffer;
				buffer = Buffer.alloc(server: ~server, numFrames: ~sampleRate * ~recording_duration, numChannels: 1);
			});

		});

		// Initialize (or re-initialize record buf synths)
		~record_buf_group.free;
		~record_buf_group = Group.new;
		~record_buf_synths = List.fill(8, {arg i;
			Synth(\recordBuf, [\buffer, ~buf_list[i], \run, 0, \trigger, -1, \input, ~input[0]], ~record_buf_group)
		});

		// Fill an list with nils so that recording synths can be set, and any triggers of empty synths pass silently
		~playBuf_synths = List.fill(8, {arg i;
			nil});

		// Constants for Arturia Midi Controller
		~current_vals = Dictionary.new;
		~top_row = [112, 74, 71, 76, 77, 93, 73, 75];
		~bottom_row = [114, 18, 19, 16, 17, 91, 79, 72];
	};
);


MIDIdef.noteOn(\noteOn, {
	arg velocity, note_number, chan, src;
	var array_index = note_number-36;
	[velocity, note_number, chan, src].postln;
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
	[velocity, note_number].postln;
	// Stops recording
	~record_buf_synths[array_index].set(\run, 0, \trigger, -1);
	~record_buf_synths[array_index].set(\trigger, 1);
});

MIDIdef.cc(\control_play, {
	arg val, note_number, chan, src;
	var array_index = note_number-44;
	[val, note_number, chan, src].postln;

	// CREATE GRAIN BUFFER SYNTHS AND STORE THEM IN ~playBuf_synths
	if (val > 50, {
		if ((note_number >= 44) && (note_number <= 51), {
			~playBuf_synths[array_index] = Synth(\playBuf,
				[\buffer, ~buf_list[array_index],
					\amp, ~current_vals.at(1)]).onFree{
				~playBuf_synths[array_index] = nil;
			};
		});
	});

	// SETS THE AMPLITUDE
	if ((note_number == 1), {
		~current_vals.put(note_number, val);
		~playBuf_synths.do({arg item, i; item.set(\amp, ~current_vals.at(note_number))});
	});

/*	// SETS THE SPEED OF PLAYBACK (CAN PLAY IN REVERSE, -2x to 4x speed)
	if (~top_row.includes(note_number), {
		var idx = ~top_row.indexOf(note_number);
		note_number.postln;
		~current_vals.put(note_number, val);
		~grain_buf_synths[idx].set(\rate, ~current_vals.at(note_number));
	});

	// SETS THE DURATION OF THE GRAINS (0.01—length of audio file)
	if (~bottom_row.includes(note_number), {
		var idx = ~bottom_row.indexOf(note_number);
		~current_vals.put(note_number, val);
		~grain_buf_synths[idx].set(\grainDur, ~current_vals.at(note_number));
	});*/
});
)