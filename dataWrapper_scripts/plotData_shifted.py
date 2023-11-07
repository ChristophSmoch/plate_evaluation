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

def accumulate_data_pesopt(data_list, x_key, y_key, strh, h):
    x_values_all = []
    y_values_all = []
    names_all = []

    for entry in data_list:
        if entry[strh] == h:
            if y_key == "l2_2D_max_disp":
                x_values = entry[x_key]
                y_values = entry["linf_2D"]
                name = entry.get('name', [])

            else:
                x_values = entry[x_key]
                y_values = entry[y_key]
                name = entry.get('name', [])

            x_values_all.append(x_values)
            y_values_all.append(y_values)
            names_all.append(name)
    return x_values_all, y_values_all, names_all

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
def accumulate_data_polyfem_g(data_list, x_key, y_key, strH, H, strg, g):
    x_values_all = []
    y_values_all = []
    names_all = []

    for entry in data_list:
        if entry[strH] == H and entry[strg] == g:
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
    file_path3 = 'polyfem_tet_data.json'
    file_path4 = 'pesopt_data.json'


    x_key = input("Enter key for x-axis data: ")
    y_key = input("Enter key for y-axis data: ")

    data_list1 = load_data_from_json(file_path1)
    data_list2 = load_data_from_json(file_path2)
    data_list3 = load_data_from_json(file_path3)
    data_list4 = load_data_from_json(file_path4)

    inplaneRes = [2.**(-i) for i in range(5,6)]
    thickness = [2.**(-i) for i in range(6,14)]
    fig = go.Figure()
    if x_key == "h":
        for H in inplaneRes:
            x_values1, y_values1, name1 = accumulate_data_polyfem(data_list1, x_key, y_key, "H", H)
            x_values2, y_values2, name2 = accumulate_data_polyfem(data_list2, x_key, y_key, "H", H)
            x_values3, y_values3, name3 = accumulate_data_polyfem_g(data_list3, x_key, y_key, "H", H, "g", 1)
            x_values4, y_values4, name4 = accumulate_data_pesopt(data_list4, x_key, y_key, "H", 2**-8)

            fig.add_trace(go.Scatter(x=-np.log2(x_values4), y=y_values4[:8], mode= 'lines+markers',
                                            name="2D_H=2^-8"  , text="2D_H=2^-8", marker=dict(size=10)))

            fig.add_trace(go.Scatter(x=-np.log2(x_values3), y=y_values3[:8], mode= 'lines+markers',
                                            name="tet_H=2^" + str(np.log2(H))  , text="tet_H=2^" + str(np.log2(H)) , marker=dict(size=10)))
            
            fig.add_trace(go.Scatter(x=-np.log2(x_values2), y=y_values2[:8], mode= 'lines+markers',
                                            name="reg_hex_H=2^" + str(np.log2(H))  , text="reg_hex_H=2^" + str(np.log2(H)) , marker=dict(size=10)))
            fig.add_trace(go.Scatter(x=-np.log2(x_values1), y=y_values1[:8], mode= 'lines+markers',
                                            name="shift_hex_H=2^" + str(np.log2(H)) , text="shift_hex_H=2^" + str(np.log2(H)) , marker=dict(size=10)))
            fig.update_xaxes(
            ticktext=["2^-" + str(i ) for i in range(6,14)],
            tickvals=np.arange(6,14) )
    if x_key == "H":
        for h in thickness:
            x_values1, y_values1, name1 = accumulate_data_polyfem(data_list1, x_key, y_key, "h", h)
            x_values2, y_values2, name2 = accumulate_data_polyfem(data_list2, x_key, y_key, "h", h)

            
            fig.add_trace(go.Scatter(x=x_values1, y=y_values1, mode= 'lines+markers',
                                            name="shift_h=2^" + str(np.log2(h)) , text="shift_h=2^" + str(np.log2(h)) , marker=dict(size=10)))
            fig.add_trace(go.Scatter(x=x_values2, y=y_values2, mode= 'lines+markers',
                                            name="reg_h=2^" + str(np.log2(h))  , text="reg_h=2^" + str(np.log2(h)) , marker=dict(size=10)))

    
    
    
    
    fig.update_layout(title='regular vs shift',
                    xaxis_title=x_key,
                    yaxis_title=y_key,
                    hovermode='closest',
                    yaxis_type='log'
                    )

    fig.show()



 