// CHECK SETTINGS OF COMP
ServerOptions.outDevices;
ServerOptions.inDevices;
MIDIFunc.trace(true);
MIDIFunc.trace(false);

(
// Server.default.options.inDevice_("new_music_for_strings");
/*Server.default.options.outDevice_("MacBook Pro Speakers");
Server.default.options.inDevice_("MacBook Pro Microphone");*/
// Server.default.options.inDevice_("Scarlett 2i2 USB");
// Server.default.options.outDevice_("Scarlett 2i2 USB");
// Server.default.options.outDevice_("SuperCollider Out");

// Set hardware in device
// Server.default.options.inDevice_("Scarlett 2i2 USB");
// Server.default.options.inDevice_("Scarlett 18i8 USB");
// Set hardware out device
// Server.default.options.outDevice_("Scarlett 18i8 USB");

~server = Server.default;
~server.options.numOutputBusChannels_(8);
~server.options.numInputBusChannels_(8);
~server.waitForBoot(
	{
		// Set Global Monitor and Input
		~monitor = [0,1];
		~input = [6,7];
		// ~input = [0,1];

		// LOAD PATHS TO MIDI BANKS
		~midi_paths = PathName.new(thisProcess.nowExecutingPath.dirname +/+ "MIDI_controls/");

		// LOAD SYNTH DEFS
		thisProcess.interpreter.executeFile(thisProcess.nowExecutingPath.dirname +/+ "synthdefs.scd");

		// LOAD GUI STYLES
		thisProcess.interpreter.executeFile(thisProcess.nowExecutingPath.dirname +/+ "GUI_files/GUI_Styles.scd");

		// LOAD GUI CONSTRUCTOR
		thisProcess.interpreter.executeFile(thisProcess.nowExecutingPath.dirname +/+ "GUI_files/GUI_Constructor.scd");

		// START SAMPLE TRIGGER GUI
		thisProcess.interpreter.executeFile(thisProcess.nowExecutingPath.dirname +/+ "GUI_files/sample_trigger_GUI.scd");
		~server.sync;

		// BOOT AND CONNECT MIDI CLIENT
		MIDIClient.init;
		MIDIIn.connectAll;

		// SELECT MIDIDef BANK
		MIDIIn.sysex = {
			arg src, data;
			if (data.size == 9) {
				data[7].postln;
				if (~window != nil, {
					{~window.close}.defer;
				});
				if (~midi_paths.entries[data[7]] != nil) {
					MIDIdef.freeAll;
					~midi_paths.entries[data[7]].fullPath.postln;
					thisProcess.interpreter.executeFile(~midi_paths.entries[data[7]].fullPath);
				};

			};
		};

		// Set a recording duration length for buffer creation and create buffers.
		~recording_duration = 5;
		~sampleRate = Server.default.sampleRate;

		// Set global memory storage
		~gm = Dictionary.new();
		~gm.put(\knob_note_numbers, [112, 74, 71, 76, 77, 93, 73, 75, 114, 18, 19, 16, 17, 91, 79, 72]);
		~gm.put(\buttons, [44, 45, 46, 47, 48, 49, 50, 51])

	};
);
)

