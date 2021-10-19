// Sequencer
~gm = Dictionary.new;
(
var buttonsize=50, columns=16, rows=8, window, top_level, header, buttons, sequencer_ctrl_1, sequencer_ctrl_2, start_instrument=\default, pattern, instruments, memory=~gm;

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
window = ~build_window.value("Sequencer", ~style_1, buttonsize*columns+420, buttonsize*rows+220);
top_level = ~build_top_level.value(window, buttonsize*columns+400, buttonsize*rows+200, ~style_1);
header = ~build_sequencer_header.value(top_level, buttonsize*columns+380, 80, ~style_1, "Sequencer");
buttons = ~build_sequencer_buttons.value(top_level, buttonsize*columns+20, buttonsize*rows+20, ~style_1, columns, rows, buttonsize);
sequencer_ctrl_1 = ~build_sequencer_control_panel_1.value(top_level, 150, buttonsize*rows+50, ~style_1, instruments, buttons[0], memory);
sequencer_ctrl_2 = ~build_sequencer_control_panel_2.value(top_level, 190, buttonsize*rows+50, ~style_1, buttonsize, memory, buttons[1], memory.at(\seq_mem).at(\reverb));

Pdefn(\pattern, Ppar(buttons[1].collect({
	arg c, r;
	var currentOctaveDegree = buttons[1].size - r - 1 + memory.at(\seq_mem).at(\currentOctave);
	Pbind(
		\instrument, Pdefn(\p_instrument, memory.at(\seq_mem).at(\instrument)),
		\scale, Pdefn(\p_scale, memory.at(\seq_mem).at(\scale)),
		\degree, Pif(Pseq(buttons[1][r], inf).coin, currentOctaveDegree, \rest),
		\dur, Pdefn(\p_dur, memory.at(\seq_mem).at(\dur)),
		\amp, Pdefn(\p_amp, memory.at(\seq_mem).at(\amp)),
		\out, Pdefn(\p_out, memory.at(\seq_mem).at(\pattern_out));
)}), inf)).play;

CmdPeriod.add({window.close;});
)