
color_hues = {
	'red': 0,
	'orange': 4000,
	'yellow': 13000,
	'green': 23000,
	'seafoam': 27000,
	'blue': 47000,
	'indigo': 48000,
	'violet': 50000,
	'purple': 51000,
	'pink': 58000,
	'fuchsia': 62000,

	'black': 35000,
	'gray': 35000,
	'grey': 35000,
	'white': 35000,
}


def choose_color_hue(color_string):
	hues = []
	for color in color_hues:
		if color in color_string:
			hues.append(color_hues[color])
	if len(hues) < 1:
		return None
	return int(sum(hues) / len(hues))


def guess_color_from_hue(hue):
	color_map = {abs(color_hues[color] - hue): color for color in color_hues}
	return color_map[min(color_map)]