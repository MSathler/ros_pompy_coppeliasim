def cython_pc(_conc_array,pose):
	x = []	
	y = []
	z = []
	inten = []
	dictionary = {}
	for i in range(_conc_array.T.shape[0]):
		for j in range(_conc_array.T.shape[1]):

			if (_conc_array.T[i][j] != 0):
				dictionary[]
				x.append((j*0.01) + pose.position.x)
				y.append((i*0.01) + pose.position.y)
				z.append(pose.position.z)
				inten.append(_conc_array.T[i][j]*0.001)
	for h in range(len(x)):
		dictionary[h] = (x[h],y[h],inten[h])
	return x,y,z,inten
