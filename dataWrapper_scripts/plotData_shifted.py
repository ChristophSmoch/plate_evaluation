import numpy as np
import json
import plotly.graph_objects as go

with open("specs.json", "r") as f:
    specs = json.load(f)
    path_to_gmsh_bin = specs["path_to_gmsh_bin"]
    path_to_polyfem_bin = specs["path_to_polyfem_bin"]
    thickness_bounds = specs["thickness_bounds"]
    inplaneRes_bounds = specs["inplaneRes_bounds"]
    outofplaneRes_bounds = specs["outofplaneRes_bounds"]

thickness = [ 2.**( - i ) for i in range( thickness_bounds[0], thickness_bounds[1] ) ]
inplaneRes = [ 2.**( -i ) for i in range(inplaneRes_bounds[0], inplaneRes_bounds[1] ) ]
outofplaneRes = [ 2**( i ) for i in range(outofplaneRes_bounds[0] , outofplaneRes_bounds[1]  ) ]

poissonRatios = [0.0] 

def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data_list = json.load(file)
    return data_list

def accumulate_data_polyfem(data_list, x_key, y_key, strH, H):
    x_values_all = []
    y_values_all = []
    names_all = []

    for entry in data_list:
        if entry[strH] == H:
            x_values = entry[x_key]
            y_values = entry[y_key]
            name = entry.get('name', [])

            x_values_all.append(x_values)
            y_values_all.append(y_values)
            names_all.append(name)

    return x_values_all, y_values_all, names_all                

if __name__ == "__main__":
    file_path1 = 'polyfem_hexahedral_regular_shifted_data.json'
    file_path2 = 'polyfem_hexahedral_regular_data.json'


    x_key = input("Enter key for x-axis data: ")
    y_key = input("Enter key for y-axis data: ")

    data_list1 = load_data_from_json(file_path1)
    data_list2 = load_data_from_json(file_path2)

    inplaneRes = [2.**(-i) for i in range(5,8)]
    if x_key == "h":
        for H in inplaneRes:
            x_values1, y_values1, name1 = accumulate_data_polyfem(data_list1, x_key, y_key, "H", H)
            x_values2, y_values2, name2 = accumulate_data_polyfem(data_list2, x_key, y_key, "H", H)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_values1, y=y_values1, mode= 'lines+markers',
                                            name="shift_H=2^" + str(np.log2(H)) , text="shift_H=2^" + str(np.log2(H)) , marker=dict(size=10)))
            fig.add_trace(go.Scatter(x=x_values2, y=y_values2, mode= 'lines+markers',
                                            name="reg_H=2^" + str(np.log2(H))  , text="reg_H=2^" + str(np.log2(H)) , marker=dict(size=10)))

    
    
    
    
    fig.update_layout(title='regular vs shift',
                    xaxis_title=x_key,
                    yaxis_title=y_key,
                    hovermode='closest',
                    xaxis_type='log',
                    yaxis_type='log'
                    )

    fig.show()



 