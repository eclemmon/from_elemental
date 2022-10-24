s = Server.default.boot;

SynthDef(\peep,{
	arg freq=100, amp=0.5, out=0;
	var snd = SinOsc.ar(freq);
	snd = snd * EnvGen.ar(Env.perc(0.001,0.25), doneAction:2) * amp;
	Out.ar(out, snd ! 2);
}).add;



(
var buttonsize=50, columns=16, rows=8, array, instrument=\default, pattern, window, butCompView, guiTitle, topLevel, sliderCompView, slider, sliderLabel, numberbox, popUpMenu, popUpMenuLabel, volumeSliderLabel, volumeSlider, volumeNumberBox, instrumentPopUp, instrumentLabel, clearButton, clearButtonLabel, control2CompView, octaveLabel, minusOctBut, plusOctBut, currentOctave, p_degree_array, quantLabel, quantSlider, quantNumberBox, reverbLabel, reverbButton, mixLabel, mixKnob, roomLabel, roomKnob, dampLabel, dampKnob;

// Window
window = Window("sequencer", Rect(0, 0, buttonsize*columns+400, buttonsize*rows+200));

// Top Level
topLevel = CompositeView(window,  Rect(0, 0, buttonsize*columns+400, buttonsize*rows+200));
topLevel.background = Color.rand;
topLevel.addFlowLayout(10@10);
topLevel.decorator.gap_(10@10);

// GUI Title
guiTitle = StaticText(topLevel, Rect(10, 10, buttonsize*columns+380, 80));
guiTitle.string = "Sequencer";
guiTitle.background = Color.rand;
guiTitle.font = Font("Monaco", 24);
guiTitle.align = \center;

// Button Composite View
butCompView = CompositeView(topLevel, Rect(0, 0, buttonsize*columns+20, buttonsize*rows+20));
butCompView.background = Color.rand;

// Sequencer Buttons
array = 0!columns!rows;

array.do{ |rows, i|
	rows.do{ |cell, j|
		// var buttonsize=50;
		Button(butCompView, Rect(j*buttonsize+10, i*buttonsize+10, buttonsize, buttonsize))
		.states_([
			["", Color.black, Color.white],
			["", Color.white, Color.black],
		])
		.action_{ |v|
			array[i][j] = v.value;
		};
	};
};


// Slider Composite View
sliderCompView = CompositeView(topLevel, Rect(0, 0, 150, buttonsize*rows+50));
sliderCompView.background = Color.rand;
sliderCompView.addFlowLayout(10@10);
sliderCompView.decorator.gap_(10@10);

// Sequencer Speed Control Label
sliderLabel = StaticText(sliderCompView, Rect(0, 10, 60, 30))
.string_("Speed")
.font_(Font("Monaco", 16))
.align_(\left);
sliderLabel.background = Color.rand;

// Volume Label
volumeSliderLabel = StaticText(sliderCompView, Rect(65, 10, 60, 30))
.string_("Volume")
.font_(Font("Monaco", 16))
.align_(\left);
volumeSliderLabel.background = Color.rand;

// Sequencer Speed Control Slider
slider = Slider(sliderCompView, Rect(0, 10, 60, 150));
slider.value = 0.1;

// Volume Control Slider
volumeSlider = Slider(sliderCompView, Rect(65, 10, 60, 150));
volumeSlider.value = 1;

sliderCompView.decorator.nextLine;

// sliderCompView.decorator.nextLine;
numberbox = NumberBox(sliderCompView, Rect(20, 20, 60, 20));
numberbox.value = 0.1;

volumeNumberBox = NumberBox(sliderCompView, Rect(20, 20, 60, 20));
volumeNumberBox.value = 0.7;

// Sequencer Speed Slider Control Action
slider.action_({
	var control;
	control = ControlSpec(0.05, 2, \exp, 0.01);
	~dur = control.map(slider.value);
	Pdefn(\lol).quant = ~dur*16;
	Pdefn(\p_dur, ~dur);
	numberbox.value_(control.map(slider.value));
});

// Slider Control
volumeSlider.action_({
	var control;
	control = ControlSpec(0, 0.7, \linear, 0.01);
	~amp = control.map(volumeSlider.value);
	Pdefn(\p_amp, ~amp);
	volumeNumberBox.value_(control.map(volumeSlider.value));
});

sliderCompView.decorator.nextLine;

// Scale Selection label
popUpMenuLabel = StaticText(sliderCompView, Rect(0, 10, 130, 30))
.string_("Scale Type")
.font_(Font("Monaco", 16))
.align_(\left);
popUpMenuLabel.background = Color.rand;

sliderCompView.decorator.nextLine;

// Scale Selection Menu
popUpMenu = PopUpMenu(sliderCompView, Rect(0, 10, 130, 30));
popUpMenu.items = Scale.names;
popUpMenu.value_(Scale.names.indexOf(\major));
popUpMenu.action_({
	arg menu;
	~scale = menu.item;
	Pdefn(\p_scale, Scale.at(~scale));
});

sliderCompView.decorator.nextLine;

// Instrument Selection Label
instrumentLabel = StaticText(sliderCompView, Rect(0, 10, 130, 30))
.string_("Instrument")
.font_(Font("Monaco", 16))
.align_(\left);
instrumentLabel.background = Color.rand;

sliderCompView.decorator.nextLine;

// Instrument Selection Label
instrumentPopUp = PopUpMenu(sliderCompView, Rect(0, 10, 130, 30));
instrumentPopUp.items = [\default, \peep];
instrumentPopUp.value_(1);
instrumentPopUp.action_({
	arg menu;
	[menu.item, menu.value].postln;
	~instrument = menu.item;
	Pdefn(\p_instrument, ~instrument);
	Pdefn(\p_out, ~pattern_out);
});

sliderCompView.decorator.nextLine;

// Clear Button
clearButton = Button(sliderCompView, Rect(0, 10, 130, 30));
clearButton.string = "clear sequencer";

clearButton.action_({
	butCompView.children(Button).do({
		arg item, i;
		if(item.value == 1, {item.valueAction = 0;})});
});

// Control Comp View 2
control2CompView = CompositeView(topLevel, Rect(0, 0, 190, buttonsize*rows+50));
control2CompView.background = Color.rand;
control2CompView.addFlowLayout(10@10);
control2CompView.decorator.gap_(10@10);

// Octave  Label
octaveLabel = StaticText(control2CompView, Rect(0, 0, 170, 30))
.string_("Octave")
.font_(Font("Monaco", 16))
.align_(\center);
octaveLabel.background = Color.rand;

control2CompView.decorator.nextLine;

// Octave Buttons
minusOctBut = Button(control2CompView, 80@40);
minusOctBut.string = "-";

plusOctBut = Button(control2CompView, 80@40);
plusOctBut.string = "+";

~currentOctave = 0;
~scale = Scale.major;
~instrument = instrument;
~dur = 0.1;
~amp = 0.7;
~pattern_out = 0;

minusOctBut.action_({
	~currentOctave =  ~currentOctave - 7;

	Pdefn(\pattern, Ppar(array.collect({
		arg c, r;
		Pbind(
			\instrument, Pdefn(\p_instrument, ~instrument),
			\scale, Pdefn(\p_scale, Scale.at(~scale)),
			\degree, Pif(Pseq(array[r], inf).coin, array.size-r-1+~currentOctave, \rest),
			\dur, Pdefn(\p_dur, ~dur),
			\amp, Pdefn(\p_amp, ~amp),
			\out, Pdefn(\p_out, ~pattern_out);
	)}), inf))
});

plusOctBut.action_({
	~currentOctave = ~currentOctave + 7;
	Pdefn(\pattern, Ppar(array.collect({
		arg c, r;
		Pbind(
			\instrument, Pdefn(\p_instrument, ~instrument),
			\scale, Pdefn(\p_scale, Scale.at(~scale)),
			\degree, Pif(Pseq(array[r], inf).coin, array.size-r-1+~currentOctave, \rest),
			\dur, Pdefn(\p_dur, ~dur),
			\amp, Pdefn(\p_amp, ~amp),
			\out, Pdefn(\p_out, ~pattern_out);
	)}), inf))
});

control2CompView.decorator.nextLine;

// QUANTIZATION SLIDER LABEL
quantLabel = StaticText(control2CompView, Rect(0, 0, 170, 30))
.string_("Quantization")
.font_(Font("Monaco", 16))
.align_(\center);
quantLabel.background = Color.rand;

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
Pdefn(\pattern).quant;

// QUANTIZATION SLIDER NUMBER BOX
quantNumberBox =  NumberBox(control2CompView, Rect(0, 20, 40, 30));
quantNumberBox.value = 0;

/*// REVERB LABEL
reverbLabel = StaticText(control2CompView, Rect(0, 0, 170, 30))
.string_("Reverb")
.font_(Font("Monaco", 16))
.align_(\center);
reverbLabel.background = Color.rand;*/

// REVERB BUTTON ON/OFF
reverbButton = Button(control2CompView, 170@30)
.states_([["Turn Reverb On", Color.white, Color.black], ["Turn Reverb Off", Color.white, Color.red]])
.action_({
	if (reverbButton.value == 1, {
		~pattern_out = 99;

	}, {
		~pattern_out = 0;
	});
	Pdefn(\p_out, ~pattern_out);
});

// REVERB LABELS
["Mix", "Room", "Damp"].do({
	arg item, i;
	var label;
	label = StaticText(control2CompView, Rect(0, 0, 170-20/3, 30))
	.string_(item)
	.font_(Font("Monaco", 16))
	.align_(\center);
	label.background = Color.rand;
});

// REVERB CONTROL KNOBS
mixKnob = Knob.new(control2CompView, Rect(0, 0, 170-20/3, 170-20/3));
mixKnob.mode =\vert;
mixKnob.value = 0.5;
mixKnob.action_({
	~reverb.set(\mix, mixKnob.value);
});

roomKnob = Knob.new(control2CompView, Rect(0, 0, 170-20/3, 170-20/3));
roomKnob.mode =\vert;
roomKnob.value = 0.5;
roomKnob.action_({
	~reverb.set(\room, roomKnob.value);
});

dampKnob = Knob.new(control2CompView, Rect(0, 0, 170-20/3, 170-20/3));
dampKnob.mode =\vert;
dampKnob.value = 0.5;
dampKnob.action_({
	~reverb.set(\damp, dampKnob.value);
});

CmdPeriod.doOnce {window.close};

window.front;

~reverb = Synth(\reverb, [\input, 99, \output, 0, \mix, 0.5, \room, 0.5, \damp, 0.5]);

pattern = Pdefn(\pattern, Ppar(array.collect({
	arg c, r;
	Pbind(
		\instrument, Pdefn(\p_instrument, instrument),
		\scale, Pdefn(\p_scale, Scale.major),
		\degree, Pif(Pseq(array[r], inf).coin, array.size-r-1, \rest),
		\dur, Pdefn(\p_dur, 0.1),
		\amp, Pdefn(\p_amp, 0.7),
		\out, Pdefn(\p_out, ~pattern_out);
)}), inf)).play;
~pattern = pattern;
)


Pdefn(\lol).quant = nil;
Pdefn(\lol).quant.postln;
Pdefn(\p_degree_0, Pseq([0,1], inf));

Pbindef(\p_degree_7, \degree, Pseq([0,1], inf));

Scale.names.indexOf(\aeolian);

~pattern.valueArray;
Pbindef("p_degree_7").asStream.nextN(20);

Pbindef(\p_degree_0, \degree, 10)

g = PdefGui();


(
w = Window.new("soundfile test", Rect(200, 300, 800, 100));
a = SoundFileView.new(w, Rect(10,10, 80, 60));

f = SoundFile.new;
f.openRead(Platform.resourceDir +/+ "sounds/a11wlk01.wav");
// f.inspect;

a.soundfile = f;
a.read(0, f.numFrames);

a.timeCursorOn = true;
a.timeCursorColor = Color.red;
a.timeCursorPosition = 2050;
a.drawsWaveForm = true;
a.gridOn = true;
a.gridResolution = 0.2;

w.front;
)
