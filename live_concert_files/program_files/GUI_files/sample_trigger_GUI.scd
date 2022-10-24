// Samples GUI
(
~server.waitForBoot(
	{
		var sf_file_names, cea_file_names, gui_width, gui_height, root;
		// PRINT WHAT THIS BANK DOES
		"PLAYBACK OF BASE SAMPLES ### MIDI_control_bank_2.scd ###".postln;
		root = PathName(PathName(thisProcess.nowExecutingPath.asString.dirname).parentPath).parentPath;
		// Buffer.freeAll;
		// Load SynthDefs
		root.postln;
		thisProcess.interpreter.executeFile(root +/+ "program_files/synthdefs.scd");

		// Load path to base samples
		~base_samples_path = PathName.new(root +/+ "sample_files/base_samples/");

		// Load path to composed and elemental and aggregated samples
		~compd_elem_agg_path = PathName.new(root +/+ "sample_files/long_elemental_samples/");

		// Load GUI Constructor
		thisProcess.interpreter.executeFile(root +/+ "program_files/GUI_files/GUI_Constructor.scd");

		// Initialize (or re-initialize record buf synths)
		~base_sample_bufs = List.new();
		~base_samples_path.filesDo{
			arg file;
			var sound_file = SoundFile.new;
			sound_file.openRead(file.fullPath);
			if (sound_file.numChannels == 1, {
				~base_sample_bufs.add(Buffer.readChannel(~server, file.fullPath, channels: [0]));
			}, {
				~base_sample_bufs.add(Buffer.readChannel(~server, file.fullPath, channels: [0, 1]));
			})
		};

		~compd_elem_agg_bufs = List.new();
		~compd_elem_agg_path.filesDo{
			arg file;
			var sound_file = SoundFile.new;
			sound_file.openRead(file.fullPath);
			if (sound_file.numChannels == 1, {
				~compd_elem_agg_bufs.add(Buffer.readChannel(~server, file.fullPath, channels: [0]));
			}, {
				~compd_elem_agg_bufs.add(Buffer.readChannel(~server, file.fullPath, channels: [0, 1]));
			})

		};

		// Fill an list with nils so that granulation synths can be set, and any triggers of empty synths pass silently
		~pb_buf_synths = List.fill(~base_samples_path.entries.size, {arg i;
			nil});
		~cea_buf_synths = List.fill(~base_samples_path.entries.size, {arg i;
			nil});

		// Fill a list with file names for button texts
		sf_file_names = Array.fill(~base_samples_path.entries.size, {arg i; ~base_samples_path.entries[i].fileName});
		cea_file_names = Array.fill(~compd_elem_agg_path.entries.size, {arg i; ~compd_elem_agg_path.entries[i].fileName});

		// GUI Size variables
		gui_height = 800;
		gui_width = 900;

		// Build GUI
		~sf_gui = ~build_window_nmfs.value("Sample File Playback", ~style_1, gui_width, gui_height);
		~sf_top_level = ~build_top_level_nmfs.value(~sf_gui, gui_width-20, gui_height-20, ~style_1);
		~sf_header_1 = ~build_sf_header_nmfs.value(~sf_top_level, gui_width-45, 80, ~style_1, "BASE SAMPLE FILE PLAYBACK");
		~sf_buttons = ~build_sf_buttons_nmfs.value(~sf_top_level, ~style_1, ~base_samples_path.entries.size, sf_file_names, gui_width-45, 340, ~base_sample_bufs, ~pb_buf_synths);
		~sf_header_2 = ~build_sf_header_nmfs.value(~sf_top_level, gui_width-45, 80, ~style_1, "COMP AND AGG SAMPLE FILE PLAYBACK");
		~cea_buttons = ~build_sf_buttons_nmfs.value(~sf_top_level, ~style_1, ~compd_elem_agg_path.entries.size, cea_file_names, gui_width-45, 230, ~compd_elem_agg_bufs, ~cea_buf_synths);
		CmdPeriod.add({~sf_gui.close;});
	};
);
)
