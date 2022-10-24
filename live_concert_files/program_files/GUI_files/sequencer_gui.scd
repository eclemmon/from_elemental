// Sequencer
~gm = Dictionary.new;
(
var buttonsize=50, columns=16, rows=8, window, top_level, track_buttons_container, ctrl_panel_container, header, buttons, track, sequencer_tab_buttons, sequencer_ctrl_1, sequencer_ctrl_2, start_instrument=\default, pattern, instruments, memory=~gm;

// Initialize Memory
memory.atFail(\seq_mem, {
	memory.put(\seq_mem, Dictionary.newFrom([
		\currentOctave, 0,
		\scale, Scale.major,
		\instrument, start_instrument,
		\dur, 0.1,
		\amp, 0.7,
		\pattern_out, 0]));
});
memory.at(\seq_mem).put(\reverb, Synth(\reverb, [\input, 99, \output, 0, \mix, 0.5, \room, 0.5, \damp, 0.5]));
instruments = [\default, \peep_sequencer, \sin_tone_sequencer, \buzzy_bram_sequencer, \phase_mod_sequencer];

// Build GUI
// Build window, top_level and header
window = ~build_window.value("Sequencer", ~style_1, buttonsize*columns+440, buttonsize*rows+280);
top_level = ~build_top_level.value(window, buttonsize*columns+420, buttonsize*rows+260, ~style_1);
header = ~build_sequencer_header.value(top_level, buttonsize*columns+380, 80, ~style_1, "Sequencer");
sequencer_tab_buttons = ~build_sequencer_tab_buttons.value(top_level, \stack, ['melody', 'harmony', 'bass']);

/*~build_sequencer_stack_layout.value(top_level, buttonsize*columns+40, (buttonsize) + (buttonsize*rows+20), ~style_1, ['melody', 'harmony', 'bass'], columns, rows, buttonsize);*/


// Build Track, tab, and buttons
track_buttons_container = ~build_track_buttons_container.value(top_level, buttonsize*columns+40, (buttonsize) + (buttonsize*rows+20), ~style_1);
track = ~build_sequencer_track.value(track_buttons_container, buttonsize*columns+20, buttonsize+20, ~style_1, columns, buttonsize);
buttons = ~build_sequencer_buttons.value(track_buttons_container, buttonsize*columns+20, buttonsize*rows+20, ~style_1, columns, rows, buttonsize);

// Built Control panel
ctrl_panel_container = ~build_track_buttons_container.value(top_level, 150+190, buttonsize*rows+50, ~style_1);
sequencer_ctrl_1 = ~build_sequencer_control_panel_1.value(ctrl_panel_container, 150, buttonsize*rows+50, ~style_1, instruments, buttons[0], memory);
sequencer_ctrl_2 = ~build_sequencer_control_panel_2.value(ctrl_panel_container, 190, buttonsize*rows+50, ~style_1, buttonsize, memory, buttons[1], memory.at(\seq_mem).at(\reverb));


Pdefn(\pattern, Ppar(
	buttons[1].collect({
		arg c, r;
		var currentOctaveDegree = buttons[1].size - r - 1 + memory.at(\seq_mem).at(\currentOctave);
		Pbind(
			\instrument, Pdefn(\p_instrument, memory.at(\seq_mem).at(\instrument)),
			\scale, Pdefn(\p_scale, memory.at(\seq_mem).at(\scale)),
			\degree, Pif(Pseq(buttons[1][r], inf).coin, currentOctaveDegree, \rest),
			\dur, Pdefn(\p_dur, memory.at(\seq_mem).at(\dur)),
			\amp, Pdefn(\p_amp, memory.at(\seq_mem).at(\amp)),
			\out, Pdefn(\p_out, memory.at(\seq_mem).at(\pattern_out)),
			\track_index, Pdefn(\p_track_index, Pseq((0..15), inf)),
			\track_func, Pdefn(\p_track_func, Pfunc({|ev| ~update_track.value(ev.track_index, track)}));
)}), inf)).play;



CmdPeriod.add({window.close;});
)
