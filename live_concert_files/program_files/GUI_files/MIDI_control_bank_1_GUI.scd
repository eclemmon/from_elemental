// GUI for MIDI_control_bank_1.scd

(

s.waitForBoot(
	{
		~window = ~build_window_nmfs.value("test", ~style_1, 870, 700);
		~top_level = ~build_top_level_nmfs.value(~window, 850, 600, ~style_1);
		~header = ~build_header_nmfs.value(~top_level, 825, 80, ~style_1, "MIDI CONTROL BANK 1");
		~slider = ~build_volume_slider_nmfs.value(~top_level, ~style_1, 240);
		~knobs = ~build_knobs_nmfs.value(~top_level, ~style_1, "Ctrl Knob", "Ctrl Knob", 240,  740);
		~buttons = ~build_buttons_nmfs.value(~top_level, ~style_1, 825, 900/8, "Synth");
		CmdPeriod.add({~window.close;});

});

)