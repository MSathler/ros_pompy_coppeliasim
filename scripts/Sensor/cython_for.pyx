import math
def read_sensor(_points,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
        
        for i in range(len(_intensity)):

            if ((_points[i].x >= (_sensor_x - _sensor_dimention)) and (_points[i].x <= (_sensor_x + _sensor_dimention)) and (_points[i].y >= (_sensor_y - _sensor_dimention)) and (_points[i].y <= (_sensor_y + _sensor_dimention))):
                
                #for j in range(len(_intensity)): 

                    #if ((_points[j].y >= (_sensor_y - _sensor_dimention)) and (_points[j].y <= (_sensor_y + _sensor_dimention))):
                        
                        #_xy_reads.append(self._intensity[i])
                        #_pos_reads.append(i)
                _sum_reads += _intensity[i]          
                        #print(self._sum_reads)              
                        
        
        return _sum_reads


def cython_distance(_points,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
    
    for i in range(len(_points)):
        dist = math.sqrt(math.pow(_points[i].x - _sensor_x, 2) + math.pow(_points[i].y - _sensor_y, 2))
        if (dist < 0.05):
            _sum_reads += _intensity[i]
    return _sum_reads