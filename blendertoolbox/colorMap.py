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

import numpy as np

def colorMap(val, colormap = "default"):
	if colormap == "blue":
		baseColor = np.array([[247,251,255],
			[222,235,247],[198,219,239],
			[158,202,225],[107,174,214],
			[ 66,146,198],[ 33,113,181],
			[  8, 81,156],[  8, 48,107]])
	elif colormap == "red":
		baseColor = np.array([[255,255,204],
			[255,237,160],[254,217,118],
			[254,178,76],[253,141,60],
			[ 252,78,43],[ 227,26,28],
			[  189, 0,38],[  128, 0,38]])
	elif colormap == "green":
		baseColor = np.array([[247,252,245],
			[229,245,224],[199,233,192],
			[161,217,155],[116,196,118],
			[ 65,171, 93],[35,139, 69],
			[  0,109, 44],[ 0, 68,27]])
	elif colormap == "gray":
		baseColor = np.array([[0,0,0],
			[255/8.0,255/8.0,255/8.0],[255/4.0,255/4.0,255/4.0],
			[255*3/8.0,255*3/8.0,255*3/8.0],[255/2.0,255/2.0,255/2.0],
			[255*5/8.0,255*5/8.0,255*5/8.0],[255*6/8.0,255*6/8.0,255*6/8.0],
			[255*7/8.0,255*7/8.0,255*7/8.0],[255,255,255]])
	elif colormap == "red_error":
		baseColor = np.array([[255,245,240], [254,230,206], [253,208,162], [253,174,107], [253,141,60] , [241,105,19], [217,72,1], [166,54,3], [127,39,4]])
	elif colormap == "RdBu":
		baseColor = np.array([[178,24,43],[214,96,77],[244,165,130],[253,219,199],[247,247,247],[209,229,240],[146,197,222],[67,147,195],[33,102,172]])
	else: # default
		baseColor = np.array([[215,48,39],
			[244,109,67],[253,174,97],
			[254,224,144],[255,255,191],
			[224,243,248],[171,217,233],
			[116,173,209],[69,117,180]])
	x = np.copy(val)
	x -= x.min()
	x /= (x.max()+1e-16)

	xp = np.linspace(0,1,num = baseColor.shape[0])

	r_fp = baseColor[:,0]
	g_fp = baseColor[:,1]
	b_fp = baseColor[:,2]

	r = np.interp(x, xp, r_fp)
	g = np.interp(x, xp, g_fp)
	b = np.interp(x, xp, b_fp)
	color = np.concatenate((r[:,None],g[:,None],b[:,None]), 1) / 256.0
	return color



