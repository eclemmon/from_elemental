//// GUI CONSTRUCTOR
(
~build_window = {
	arg window_title, style, width, height;
	Window(window_title, Rect(10, 10, width, height))
	.background_(style.at("window_color"))
	.front;
};

~build_top_level = {
	arg window, width, height, style;
	var compView = CompositeView(window, Rect(10, 10, width, height))
	.background_(style.at("top_level_frame_color"));
	compView.addFlowLayout(10@10);
	compView.decorator.gap_(10@10);
	compView;
};

~build_header = {
	arg top, hwidth, hheight, style, string;
	var compView, label, twidth;
	twidth = hwidth-125;
	compView = CompositeView(top, Rect(0, 0, hwidth, hheight))
	.background_(style.at("header_frame_color"));
	compView.addFlowLayout(325@0);
	label = StaticText(compView, twidth@hheight)
	.string_(string)
	.font_(style.at("header_font"))
	.align(\center);
	compView;
};

~build_volume_slider = {
	arg top, style, frame_height;
	var compView, label, slider, numberbox;
	compView = CompositeView(top, Rect(0, 0, 70, frame_height))
	.background_(style.at("bank_frame_color"));
	compView.addFlowLayout(10@10);
	compView.decorator.gap_(10@10);
	// Build Label
	label = StaticText(compView, Rect(10, 10, 50, 20))
	.string_("VOLUME")
	.font_(style.at("subheader_font"))
	.align_(\left);
	// Next Line
	compView.decorator.nextLine;
	// Build Slider
	slider = Slider(compView, Rect(0, 0, 50, frame_height-80));
	// Next Line
	compView.decorator.nextLine;
	numberbox = NumberBox(compView, Rect(20, 20, 50, 20));
	compView;
};

~build_bend_slider = {
	arg top, style, frame_height;
	var compView, label, slider, numberbox;
	compView = CompositeView(top, Rect(0, 0, 70, frame_height))
	.background_(style.at("bank_frame_color"));
	compView.addFlowLayout(10@10);
	compView.decorator.gap_(10@10);
	// Build Label
	label = StaticText(compView, Rect(10, 10, 50, 20))
	.string_("BEND")
	.font_(style.at("subheader_font"))
	.align_(\center);
	// Next Line
	compView.decorator.nextLine;
	// Build Slider
	slider = Slider(compView, Rect(10, 10, 50, frame_height-80));
	// Next Line
	compView.decorator.nextLine;
	numberbox = NumberBox(compView, Rect(20, 20, 50, 20));
	compView;
};

~build_knobs = {
	arg top, style, bank_one_string, bank_two_string, frame_height, frame_width;
	var compView, knobs_one_text, knobs_two_text, knobs_one, knobs_two;
	// Build Composite View (Frame)
	compView = CompositeView(top, Rect(0,0,frame_width,frame_height))
	.background_(style.at("bank_frame_color"));
	compView.addFlowLayout(10@10);
	compView.decorator.gap_(10@10);
	// Build Text Descriptors of Knobs Bank 1
	knobs_one_text = Array.fill(8, {
		arg i;
		var string = format("% %", bank_one_string, i+1);
		StaticText(compView, 80@15)
		.string_(string)
		.font_(style.at("text_font"))
		.align_(\center);
	});
	// Next Line
	compView.decorator.nextLine;
	// Build Knob Bank 1
	knobs_one = Array.fill(8, {
		arg i;
		Knob.new(compView, Rect(0, 0, 80, 80));
	});
	// Next Line
	compView.decorator.nextLine;
	// Build Text Descriptors of Knobs Bank 2
	knobs_two_text = Array.fill(8, {
		arg i;
		var string = format("% %", bank_two_string, i+9);
		StaticText(compView, 80@15)
		.string_(string)
		.font_(style.at("text_font"))
		.align_(\center);
	});
	// Next Line
	compView.decorator.nextLine;
	// Build Knob Bank 2
	knobs_two = Array.fill(8, {
		arg i;
		Knob.new(compView, Rect(0, 0, 80, 80));
	});
	compView;
};


~build_buttons = {
	arg top, style, frame_width, frame_height, button_text;
	var compView, buttons;
	// Make Composite View
	compView = CompositeView(top, Rect(0,0, frame_width, frame_height))
	.background_(style.at("bank_frame_color"));
	compView.addFlowLayout(10@10);
	compView.decorator.gap_(10@10);
	// Make Buttons
	buttons = Array.fill(8, {
		arg i;
		// Button Size
		var button_side_size = (frame_width - 95) / 8;
		// Make Button And Define States
		var button = Button(compView, Rect(0, 0, button_side_size, button_side_size))
		.font_(style.at("text_font"));
		var string = format("% %", button_text, i+1);
		button.states = [
			[string, style.at("text_color"), Color.white],
			[string, Color.white, style.at("text_color")]
		];

		// This function turns off all other buttons when a button has been pressed
		button.action_({
			arg button;
			buttons.do({
				arg item, i;
				if (button != item, {
					if (item.value == 1,
						{ item.value = 0 }
					);
				}, {
					button.value = 1;
				});
			});
		});
		button;
	});
	compView;
};

~build_sf_buttons = {
	arg top, style, num_buttons, button_texts, frame_width, frame_height, base_sample_bufs, pb_buf_synths;
	var compView, buttons, sliders;

	// Make Composite View
	compView = CompositeView(top, Rect(0,0, frame_width, frame_height))
	.background_(style.at("bank_frame_color"));
	compView.addFlowLayout(10@10);
	compView.decorator.gap_(10@10);

	// Make Buttons
	num_buttons.do{
		arg i;

		// Button Size
		var button_side_size = (frame_width - 95) / 6;

		// Make Button And Define States
		var button = Button(compView, Rect(0, 0, button_side_size, 45))
		.font_(style.at("text_font"));
		var string = format("%", button_texts[i]);

		// Create Slider
		var slider = Slider(compView, Rect(0, 0, 45, 45)).value_(0);

		// Style Button Action
		button.states = [
			[string, style.at("text_color"), Color.white],
			[string, Color.white, style.at("text_color")]
		];

		// Add Button action
		button.action_({
			if (button.value == 1, {
				if (base_sample_bufs[i].numChannels == 1, {
					pb_buf_synths[i] = Synth(\playBuf, [\buffer, base_sample_bufs[i], \amp, 0, \mono_stereo, 2, \lag_time, 0.1]).onFree{
						pb_buf_synths[i] = nil;
					};
				}, {
					pb_buf_synths[i] = Synth(\playBuf_2ch, [\buffer, base_sample_bufs[i], \amp, 0, \lag_time, 0.1]).onFree{
						pb_buf_synths[i] = nil;
					};
				});
			}, {
				pb_buf_synths[i].set(\amp, 0);
			});
		});

		// Add Slider action
		slider.action_({
			pb_buf_synths[i].set(\amp, slider.value.linlin(0, 1, 0, 127));
		});


	};
	compView;
};

~build_sf_header = {
	arg top, hwidth, hheight, style, string;
	var compView, label, twidth;
	twidth = hwidth-125;
	compView = CompositeView(top, Rect(0, 0, hwidth, hheight))
	.background_(style.at("header_frame_color"));
	compView.addFlowLayout(20@5);
	label = StaticText(compView, twidth@hheight)
	.string_(string)
	.font_(style.at("header_font"))
	.align(\left);
	compView;
};

~build_sequencer_header = {
	arg top, hwidth, hheight, style, string;
	var guiTitle;
	guiTitle = StaticText(top, Rect(10, 10, hwidth, hheight));
	guiTitle.string = "Sequencer";
	guiTitle.background = style.at("header_frame_color");
	guiTitle.font = style.at("header_font");
	guiTitle.align = \center;
};

~build_sequencer_buttons = {
	arg top, hwidth, hheight, style, columns, rows, buttonsize;
	var butCompView, array, sequencer_button_data;

	// Button Composite View
	butCompView = CompositeView(top, Rect(0, 0, buttonsize*columns+20, buttonsize*rows+20));
	butCompView.background = style.at("bank_frame_color");

	// Sequencer Buttons
	array = 0!columns!rows;

	array.do{ |rows, i|
		rows.do{ |cell, j|
			// var buttonsize=50;
			Button(butCompView, Rect(j*buttonsize+10, i*buttonsize+10, buttonsize, buttonsize))
			.states_([
				["", style.at("text_color"), Color.white],
				["", Color.white, style.at("text_color")],
			])
			.action_{ |v|
				array[i][j] = v.value;
			};
		};
	};

	sequencer_button_data = [butCompView, array];
};

~build_sequencer_control_panel_1 = {
	arg top, hwidth, hheight, style, instruments=[\default], butCompView, memory;
	var compView, speedSliderLabel, volumeSliderLabel, speedSlider, volumeSlider, speedNumberBox, volumeNumberBox, scaleMenuLabel, scaleMenu, instrumentLabel, instrumentMenu, clearButton;
	// Slider Composite View
	compView = CompositeView(top, Rect(0, 0, hwidth, hheight));
	compView.background = style.at("bank_frame_color");
	compView.addFlowLayout(10@10);
	compView.decorator.gap_(10@10);

	// Sequencer Speed Control Label
	speedSliderLabel = StaticText(compView, Rect(0, 10, 60, 30))
	.string_("Speed")
	.font_(style.at("text_font"))
	.align_(\center);
	speedSliderLabel.background = style.at("window_color");
	speedSliderLabel.stringColor  = Color.white;

	// Volume Label
	volumeSliderLabel = StaticText(compView, Rect(65, 10, 60, 30))
	.string_("Volume")
	.font_(style.at("text_font"))
	.align_(\center);
	volumeSliderLabel.background = style.at("window_color");
	volumeSliderLabel.stringColor = Color.white;

	// Sequencer Speed Control Slider
	speedSlider = Slider(compView, Rect(0, 10, 60, 150));
	speedSlider.value = 0.1;

	// Volume Control Slider
	volumeSlider = Slider(compView, Rect(65, 10, 60, 150));
	volumeSlider.value = 1;

	compView.decorator.nextLine;

	// sliderCompView.decorator.nextLine;
	speedNumberBox = NumberBox(compView, Rect(20, 20, 60, 20));
	speedNumberBox.value = 0.1;

	volumeNumberBox = NumberBox(compView, Rect(20, 20, 60, 20));
	volumeNumberBox.value = 0.7;

	// Sequencer Speed Slider Control Action
	speedSlider.action_({
		var control;
		control = ControlSpec(0.05, 2, \exp, 0.01);
		Pdefn(\p_dur, control.map(speedSlider.value));
		speedNumberBox.value_(control.map(speedSlider.value));
	});

	// Slider Control
	volumeSlider.action_({
		var control;
		control = ControlSpec(0, 0.7, \linear, 0.01);
		Pdefn(\p_amp, control.map(volumeSlider.value));
		volumeNumberBox.value_(control.map(volumeSlider.value));
	});

	compView.decorator.nextLine;

	// Scale Selection label
	scaleMenuLabel = StaticText(compView, Rect(0, 10, 130, 30))
	.string_("Scale Type")
	.font_(style.at("text_font"))
	.align_(\center);
	scaleMenuLabel.background = style.at("window_color");
	scaleMenuLabel.stringColor = Color.white;

	compView.decorator.nextLine;

	// Scale Selection Menu
	scaleMenu = PopUpMenu(compView, Rect(0, 10, 130, 30));
	scaleMenu.items = Scale.names;
	scaleMenu.value_(Scale.names.indexOf(\major));
	scaleMenu.action_({
		arg menu;
		Pdefn(\p_scale, Scale.at(menu.item));
	});

	compView.decorator.nextLine;

	// Instrument Selection Label
	instrumentLabel = StaticText(compView, Rect(0, 10, 130, 30))
	.string_("Instrument")
	.font_(style.at("text_font"))
	.align_(\center);
	instrumentLabel.background = style.at("window_color");
	instrumentLabel.stringColor = Color.white;

	compView.decorator.nextLine;

	// Instrument Selection Label
	instrumentMenu = PopUpMenu(compView, Rect(0, 10, 130, 30));
	instrumentMenu.items = instruments;
	instrumentMenu.value_(0);
	instrumentMenu.action_({
		arg menu;
		// [menu.item, menu.value].postln;
		memory.at(\seq_mem).put(\instrument, menu.item);
		Pdefn(\p_instrument, menu.item);
	});

	compView.decorator.nextLine;

	// Clear Sequencer Button
	clearButton = Button(compView, Rect(0, 10, 130, 30));
	clearButton.string = "clear sequencer";

	clearButton.action_({
		butCompView.children(Button).do({
			arg item, i;
			if(item.value == 1, {item.valueAction = 0;})});
	});

	compView;
};

~build_sequencer_control_panel_2 = {
	arg top, hwidth, hheight, style, buttonsize, memory, array, reverb;
	var control2CompView, octaveLabel, minusOctBut, plusOctBut, quantLabel, quantSlider, quantNumberBox, mixKnob, roomKnob, dampKnob, reverbButton;

	// Control Comp View 2
	control2CompView = CompositeView(top, Rect(0, 0, hwidth, hheight));
	control2CompView.background = style.at("bank_frame_color");
	control2CompView.addFlowLayout(10@10);
	control2CompView.decorator.gap_(10@10);

	// Octave  Label
	octaveLabel = StaticText(control2CompView, Rect(0, 0, hwidth-20, 30))
	.string_("Octave")
	.font_(style.at("text_font"))
	.align_(\center);
	octaveLabel.background = style.at("window_color");
	octaveLabel.stringColor = Color.white;

	control2CompView.decorator.nextLine;

	// Octave Buttons
	minusOctBut = Button(control2CompView, 80@40);
	minusOctBut.string = "-";

	plusOctBut = Button(control2CompView, 80@40);
	plusOctBut.string = "+";

	// Octave Button Actions
	minusOctBut.action_({
		memory.at(\seq_mem).put(\currentOctave, memory.at(\seq_mem).at(\currentOctave) - 7);

		Pdefn(\pattern, Ppar(array.collect({
			arg c, r;
			var currentOctaveDegree = array.size - r - 1 + memory.at(\seq_mem).at(\currentOctave);
			Pbind(
				\instrument, Pdefn(\p_instrument, memory.at(\seq_mem).at(\instrument)),
				\scale, Pdefn(\p_scale, Scale.at(memory.at(\seq_mem).at(\scale))),
				\degree, Pif(Pseq(array[r], inf).coin, currentOctaveDegree, \rest),
				\dur, Pdefn(\p_dur, memory.at(\seq_mem).at(\dur)),
				\amp, Pdefn(\p_amp, memory.at(\seq_mem).at(\amp)),
				\out, Pdefn(\p_out, memory.at(\seq_mem).at(\pattern_out));
		)}), inf));
	});

	plusOctBut.action_({
		memory.at(\seq_mem).put(\currentOctave, memory.at(\seq_mem).at(\currentOctave) + 7);

		Pdefn(\pattern, Ppar(array.collect({
			arg c, r;
			var currentOctaveDegree = array.size - r - 1 + memory.at(\seq_mem).at(\currentOctave);
			Pbind(
				\instrument, Pdefn(\p_instrument, memory.at(\seq_mem).at(\instrument)),
				\scale, Pdefn(\p_scale, Scale.at(memory.at(\seq_mem).at(\scale))),
				\degree, Pif(Pseq(array[r], inf).coin, currentOctaveDegree, \rest),
				\dur, Pdefn(\p_dur, memory.at(\seq_mem).at(\dur)),
				\amp, Pdefn(\p_amp, memory.at(\seq_mem).at(\amp)),
				\out, Pdefn(\p_out, memory.at(\seq_mem).at(\pattern_out));
		)}), inf))
	});

	control2CompView.decorator.nextLine;

	// QUANTIZATION SLIDER LABEL
	quantLabel = StaticText(control2CompView, Rect(0, 0, 170, 30))
	.string_("Quantization")
	.font_(style.at("text_font"))
	.align_(\center);
	quantLabel.background = style.at("window_color");
	quantLabel.stringColor = Color.white;

	control2CompView.decorator.nextLine;

	// QUANTIZATION SLIDER
	quantSlider = Slider(control2CompView, Rect(0, 0, 120, 30));
	quantSlider.orientation = \horizontal;
	quantSlider.step = 1.0/4;
	quantSlider.action_({
		quantNumberBox.value_(quantSlider.value * 4);
		if (quantSlider.value == 0, {
			Pdefn(\pattern).quant = nil;
		}, {
			Pdefn(\pattern).quant = quantSlider.value * 4;
		});

	});

	// QUANTIZATION SLIDER NUMBER BOX
	quantNumberBox =  NumberBox(control2CompView, Rect(0, 20, 40, 30));
	quantNumberBox.value = 0;

	// REVERB BUTTON ON/OFF
	reverbButton = Button(control2CompView, 170@30)
	.states_([["Turn Reverb On", Color.white, style.at("text_color")], ["Turn Reverb Off", Color.white, Color.red]])
	.action_({
		if (reverbButton.value == 1, {
			memory.at(\seq_mem).put(\pattern_out, 99);

		}, {
			memory.at(\seq_mem).put(\pattern_out, 0);
		});
		Pdefn(\p_out, memory.at(\seq_mem).at(\pattern_out));
	});

	// REVERB LABELS
	["Mix", "Room", "Damp"].do({
		arg item, i;
		var label;
		label = StaticText(control2CompView, Rect(0, 0, 170-20/3, 30))
		.string_(item)
		.font_(style.at("text_font"))
		.align_(\center);
		label.background = style.at("bank_frame_color");
	});

	// REVERB CONTROL KNOBS
	mixKnob = Knob.new(control2CompView, Rect(0, 0, 170-20/3, 170-20/3));
	mixKnob.mode =\vert;
	mixKnob.value = 0.5;
	mixKnob.action_({
		reverb.set(\mix, mixKnob.value);
	});

	roomKnob = Knob.new(control2CompView, Rect(0, 0, 170-20/3, 170-20/3));
	roomKnob.mode =\vert;
	roomKnob.value = 0.5;
	roomKnob.action_({
		reverb.set(\room, roomKnob.value);
	});

	dampKnob = Knob.new(control2CompView, Rect(0, 0, 170-20/3, 170-20/3));
	dampKnob.mode =\vert;
	dampKnob.value = 0.5;
	dampKnob.action_({
		reverb.set(\damp, dampKnob.value);
	});
};

~volume_midi_control = {
	arg object, val;
	object.children().at(1).value_(val/127);
	object.children().at(2).value_(val/127);
};

~knob_midi_control = {
	arg object, index, val;
	object.children(Knob).at(index).value_(val/127);
};

~button_midi_control = {
	arg object, index;
	object.children(Button).at(index).doAction;
};

~bend_midi_control = {
	arg object, val;
	object.children().at(1).value_(val/16383);
	object.children().at(2).value_(val/16383);
};
)


