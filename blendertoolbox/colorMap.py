# Copyright 2020 Hsueh-Ti Derek Liu
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# the color maps are copied from the amazing colorbrewer website https://colorbrewer2.org/

import numpy as np

def colorMap(val, colormap = "default", cmin=None, cmax=None):
	if colormap == "heat":
		baseColor = np.array([[255,255,204],
			[255,237,160],[254,217,118],
			[254,178,76],[253,141,60],
			[ 252,78,43],[ 227,26,28],
			[  189, 0,38],[  128, 0,38]])
	elif colormap == "red_error":
		baseColor = np.array([[255,245,240], [254,230,206], [253,208,162], [253,174,107], [253,141,60] , [241,105,19], [217,72,1], [166,54,3], [127,39,4]])
	elif colormap == "RdBu":
		baseColor = np.array([[178,24,43],[214,96,77],[244,165,130],[253,219,199],[247,247,247],[209,229,240],[146,197,222],[67,147,195],[33,102,172]])
	elif colormap == "YlGn":
		baseColor = np.array([[255,255,229], [247,252,185], [217,240,163], [173,221,142], [120,198,121], [65,171,93], [35,132,67], [0,104,55], [0,69,41]])
	elif colormap == "YlGnBu":
		baseColor = np.array([[255,255,217], [237,248,177], [199,233,180], [127,205,187], [65,182,196], [29,145,192], [34,94,168], [37,52,148], [8,29,88]])
	elif colormap == "GnBu":
		baseColor = np.array([[247,252,240], [224,243,219], [204,235,197], [168,221,181], [123,204,196], [78,179,211], [43,140,190], [8,104,172], [8,64,129]])
	elif colormap == "BuGn":
		baseColor = np.array([[247,252,253], [229,245,249], [204,236,230], [153,216,201], [102,194,164], [65,174,118], [35,139,69], [0,109,44], [0,68,27]])
	elif colormap == "PuBuGn":
		baseColor = np.array([[255,247,251], [236,226,240], [208,209,230], [166,189,219], [103,169,207], [54,144,192], [2,129,138], [1,108,89], [1,70,54]])
	elif colormap == "PuBu":
		baseColor = np.array([[255,247,251], [236,231,242], [208,209,230], [166,189,219], [116,169,207], [54,144,192], [5,112,176], [4,90,141], [2,56,88]])
	elif colormap == "BuPu":
		baseColor = np.array([[247,252,253], [224,236,244], [191,211,230], [158,188,218], [140,150,198], [140,107,177], [136,65,157], [129,15,124], [77,0,75]])
	elif colormap == "RdPu":
		baseColor = np.array([[255,247,243], [253,224,221], [252,197,192], [250,159,181], [247,104,161], [221,52,151], [174,1,126], [122,1,119], [73,0,106]])
	elif colormap == "PuRd":
		baseColor = np.array([[247,244,249], [231,225,239], [212,185,218], [201,148,199], [223,101,176], [231,41,138], [206,18,86], [152,0,67], [103,0,31]])
	elif colormap == "OrRd":
		baseColor = np.array([[255,247,236], [254,232,200], [253,212,158], [253,187,132], [252,141,89], [239,101,72], [215,48,31], [179,0,0], [127,0,0]])
	elif colormap == "YlOrRd":
		baseColor = np.array([[255,255,204], [255,237,160], [254,217,118], [254,178,76], [253,141,60], [252,78,42], [227,26,28], [189,0,38], [128,0,38]])
	elif colormap == "YlOrBr":
		baseColor = np.array([[255,255,229], [255,247,188], [254,227,145], [254,196,79], [254,153,41], [236,112,20], [204,76,2], [153,52,4], [102,37,6]])
	elif colormap == "Purples":
		baseColor = np.array([[252,251,253], [239,237,245], [218,218,235], [188,189,220], [158,154,200], [128,125,186], [106,81,163], [84,39,143], [63,0,125]])
	elif colormap == "Blues":
		baseColor = np.array([[247,251,255], [222,235,247], [198,219,239], [158,202,225], [107,174,214], [66,146,198], [33,113,181], [8,81,156], [8,48,107]])
	elif colormap == "Greens":
		baseColor = np.array([[247,252,245], [229,245,224], [199,233,192], [161,217,155], [116,196,118], [65,171,93], [35,139,69], [0,109,44], [0,68,27]])
	elif colormap == "Oranges":
		baseColor = np.array([[255,245,235], [254,230,206], [253,208,162], [253,174,107], [253,141,60], [241,105,19], [217,72,1], [166,54,3], [127,39,4]])
	elif colormap == "Reds":
		baseColor = np.array([[255,245,240], [254,224,210], [252,187,161], [252,146,114], [251,106,74], [239,59,44], [203,24,29], [165,15,21], [103,0,13]])
	elif colormap == "Greys":
		baseColor = np.array([[255,255,255], [240,240,240], [217,217,217], [189,189,189], [150,150,150], [115,115,115], [82,82,82], [37,37,37], [0,0,0]])
	else: # default
		baseColor = np.array([[215,48,39],
			[244,109,67],[253,174,97],
			[254,224,144],[255,255,191],
			[224,243,248],[171,217,233],
			[116,173,209],[69,117,180]])
	x = np.copy(val)

	if cmin is None or cmax is None:
		x -= x.min()
		x /= (x.max()+1e-16)
	else:
		x -= cmin
		x /= (cmax-cmin)

	xp = np.linspace(0,1,num = baseColor.shape[0])

	r_fp = baseColor[:,0]
	g_fp = baseColor[:,1]
	b_fp = baseColor[:,2]

	r = np.interp(x, xp, r_fp)
	g = np.interp(x, xp, g_fp)
	b = np.interp(x, xp, b_fp)
	color = np.concatenate((r[:,None],g[:,None],b[:,None]), 1) / 256.0
	return color



