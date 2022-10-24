// GUI for MIDI_control_bank_8.scd

(

s.waitForBoot(
	{
		~window = ~build_window_nmfs.value("MIDI CONTROL BANK 8", ~style_1, 970, 700);
		~top_level = ~build_top_level_nmfs.value(~window, 950, 600, ~style_1);
		~header = ~build_header_nmfs.value(~top_level, 925, 80, ~style_1, "MIDI CONTROL BANK 8");
		~bend_slider = ~build_bend_slider_nmfs.value(~top_level, ~style_1, 240);
		~slider = ~build_volume_slider_nmfs.value(~top_level, ~style_1, 240);
		~knobs = ~build_knobs_nmfs.value(~top_level, ~style_1, "Gran PBS", "Grai Size", 240,  740);
		~buttons = ~build_buttons_nmfs.value(~top_level, ~style_1, 925, 1000/8, "Grain Bank");
		CmdPeriod.add({~window.close;});

});

)