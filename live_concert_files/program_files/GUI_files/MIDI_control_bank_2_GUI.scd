// GUI for MIDI_control_bank_2.scd
(
s.waitForBoot(
	{
		~window = ~build_window.value("MIDI CONTROL BANK", ~style_1, 870, 700);
		~top_level = ~build_top_level.value(~window, 850, 600, ~style_1);
		~header = ~build_header.value(~top_level, 825, 80, ~style_1, "MIDI CONTROL BANK 2");
		~slider = ~build_volume_slider.value(~top_level, ~style_1, 240);
		~knobs = ~build_knobs.value(~top_level, ~style_1, "Ctrl Knob", "Ctrl Knob", 240,  740);
		~buttons = ~build_buttons.value(~top_level, ~style_1, 825, 900/8, "Synth");
		CmdPeriod.add({~window.close;});
});
)