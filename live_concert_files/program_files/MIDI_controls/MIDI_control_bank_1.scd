// Keyboard with Oscillator Synths
(
s = Server.default;
s.waitForBoot(
	{
		var root = PathName(PathName(thisProcess.nowExecutingPath.asString.dirname).parentPath).parentPath;
		root.postln;
		// PRINT WHAT THIS BANK DOES
		"1. SIMPLE WAVE OSCs ### MIDI_control_bank_1.scd ###".postln;

		// Initialize midi control bank memory
		~gm.atFail(\bank_1_vals, {~gm.put(\bank_1_vals, Dictionary.new)});

		// Initialize sustain to false
		~gm.at(\bank_1_vals).atFail(\sustain, {~gm.at(\bank_1_vals).put(\sustain, false)});
		~gm.at(\bank_1_vals).atFail(\synth_symbols, {~gm.at(\bank_1_vals).put(\synth_symbols, [\sin_tone, \buzzy_bram, \subtract_noise_synth, \sin_fb_synth, \phase_mod])});
		~gm.at(\bank_1_vals).atFail(\synth_index, {~gm.at(\bank_1_vals).put(\synth_index, 0)});
		~gm.at(\bank_1_vals).atFail(\synth_bank_global_amp, {~gm.at(\bank_1_vals).put(\synth_bank_global_amp, 0)});
		~gm.at(\bank_1_vals).atFail(\notes, {~gm.at(\bank_1_vals).put(\notes, Array.fill(128, nil))});

		// Load SynthDefs
		thisProcess.interpreter.executeFile(root +/+ "program_files/synthdefs.scd");

		// Boot GUI
		thisProcess.interpreter.executeFile(root +/+ "program_files/GUI_files/MIDI_control_bank_1_GUI.scd");

		// MIDIdef to control synth sustain.
		MIDIdef.sysex(\sustain_synths, {
			arg data, src;
			if ((data[9] == 47) && (data[10] == 127), {
				if (~gm.at(\bank_1_vals).at(\sustain), {
					~gm.at(\bank_1_vals).put(\sustain, false);
					~gm.at(\bank_1_vals).at(\notes).do({
						arg item, i;
						item.set(\gate, 0);
						~gm.at(\bank_1_vals).at(\notes).put(i, nil);
					});
				}, {
					~gm.at(\bank_1_vals).put(\sustain, true);
				});
			};
			)
		});

		// MIDIdef to control synth selection
		MIDIdef.cc(\synth_select, {
			arg val, note_number, chan, src;
			var index = note_number - 22;
			~gm.at(\bank_1_vals).put(\synth_index, index);
			if (val == 127, {
				{
					~button_midi_control.value(~buttons, index);
				}.defer;
			});
		}, (22..29));

		MIDIdef.cc(\volume_control, {
			arg val, note_number, chan, src;
			var index = note_number - 22;
			~gm.at(\bank_1_vals).put(\synth_bank_global_amp, val.linlin(0,127,0,1));
			// ~synth_bank_global_amp = val.linlin(0,127,0,1);
			~gm.at(\bank_1_vals).at(\notes).do(
				{
					arg item, i;
					item.set(\amp, val.linexp(1,127,0.01,0.03) * ~gm.at(\bank_1_vals).at(\synth_bank_global_amp))
				}
			);
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


		// NoteOn and NoteOff MIDIdef h/T Eli
		MIDIdef.noteOn(\noteOn, {
			arg velocity, note_number, chan, src;
			[velocity, note_number].postln;
			~gm.at(\bank_1_vals).at(\notes).at(note_number).set(\gate, 0);
			// ~notes.at(note_number).set(\gate, 0);
			~gm.at(\bank_1_vals).at(\notes).put(note_number, Synth(
				~gm.at(\bank_1_vals).at(\synth_symbols).at(~gm.at(\bank_1_vals).at(\synth_index)),
				[
					\freq, note_number.midicps,
					\amp, velocity.linexp(1,127,0.02,0.3) * ~gm.at(\bank_1_vals).at(\synth_bank_global_amp),
					\gate, 1
					// \bend, ~bend.linlin(0, 16383,-2,2)
				]
			);
			);

		});

		MIDIdef.noteOff(\noteOff, {
			arg velocity, note_number;
			[velocity, note_number].postln;
			if (~gm.at(\bank_1_vals).at(\sustain), {
			}, {
				~gm.at(\bank_1_vals).at(\notes).at(note_number).set(\gate, 0);
				~gm.at(\bank_1_vals).at(\notes).put(note_number, nil);
			});
		});


});
)
