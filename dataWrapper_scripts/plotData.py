import json
import plotly.graph_objects as go
import numpy as np


params = ["h", "H"]

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

def accumulate_data_pesopt_base(data_list, x_key, y_key):
    x_values_all = []
    y_values_all = []
    names_all = []

    for entry in data_list:
        x_values = entry[x_key]
        y_values = entry[y_key]
        name = entry.get('name', [])

        x_values_all.append(x_values)
        y_values_all.append(y_values)
        names_all.append(name)

    return x_values_all, y_values_all, names_all
def accumulate_data_polyfem(data_list, x_key, y_key, strh, h, strg, g):
    x_values_all = []
    y_values_all = []
    names_all = []

    for entry in data_list:
        if (entry[strh] == h) and entry[strg] == g:
            x_values = entry[x_key]
            y_values = entry[y_key]
            name = entry.get('name', [])

            x_values_all.append(x_values)
            y_values_all.append(y_values)
            names_all.append(name)

    return x_values_all, y_values_all, names_all

def accumulate_data_polyfem_base(data_list, x_key, y_key):
    x_values_all = []
    y_values_all = []
    names_all = []

    for entry in data_list:
        
        x_values = entry[x_key]
        y_values = entry[y_key]
        name = entry.get('name', [])

        x_values_all.append(x_values)
        y_values_all.append(y_values)
        names_all.append(name)

    return x_values_all, y_values_all, names_all

def accumulate_data_polyfem_Hg(data_list, x_key, y_key, strh, h, factorHg):
    x_values_all = []
    y_values_all = []
    names_all = []

    for entry in data_list:
        if (entry[strh] == h):
            x_values = entry[x_key]
            y_values = entry[y_key]
            name = entry.get('name', [])
            if (entry["g_real"] == x_values * factorHg):
                x_values_all.append(x_values)
                y_values_all.append(y_values)
                names_all.append(name)

    return x_values_all, y_values_all, names_all


if __name__ == "__main__":
    colors = ['red', 'blue', 'yellow', 'green', 'orange', 'purple']
    file_path1 = 'pesopt_data.json'
    file_path2 = 'polyfem_tet_data.json'
    file_path3 = 'polyfem_hex_data.json'
    file_path4 = 'polyfem_prism_data.json'

    x_key = input("Enter key for x-axis data: ")
    y_key = input("Enter key for y-axis data: ")

    data_list1 = load_data_from_json(file_path1)
    data_list2 = load_data_from_json(file_path2)
    data_list3 = load_data_from_json(file_path3)
    data_list4 = load_data_from_json(file_path4)

    thickness = [2**(-i) for i in range(6,14)]
    outofplaneRes = [2**(-i) for i in range( 15)]
    outofplaneRes_div =  [2**(i) for i in range(3)]
    # outofplaneRes_div.append(2**(-i) for i in range(4))
    # print(outofplaneRes_div)
    inplaneRes = [2**(-i) for i in range(4,9)]

    fig = go.Figure()
    if x_key == "h":
        for H in inplaneRes:
            # print(accumulate_data_pesopt(data_list1, x_key, y_key, "H", H))
            x_values1, y_values1, name1 = accumulate_data_pesopt(data_list1, x_key, y_key, "H", H)

            fig.add_trace(go.Scatter(x=-np.log2(x_values1), y=y_values1, mode= 'lines+markers',
                                    name="pesopt_H=2^-" + str(int(-np.log2(H))) , text="pesopt_H=2^-" + str(int(-np.log2(H))), marker=dict(size=10)))
            for g in outofplaneRes_div:

                x_values2, y_values2, name2 = accumulate_data_polyfem(data_list2, x_key, y_key, "H", H, "g", g)
                if(len(x_values2) >=3):
                    fig.add_trace(go.Scatter(x=-np.log2(x_values2), y=y_values2, mode= 'lines+markers',
                                    name="polyfem_H=2^-" + str(int(-np.log2(H))) + "_g=" + str(g), text="polyfem_H=2^-" + str(int(-np.log2(H))) + "_g=2^" + str(int(np.log2(g))), marker=dict(size=10)))

                x_values3, y_values3, name3 = accumulate_data_polyfem(data_list3, x_key, y_key, "H", H, "g", g)
                if(len(x_values3) >=3):
                    fig.add_trace(go.Scatter(x=-np.log2(x_values3), y=y_values3, mode= 'lines+markers',
                                        name="polyfem_hex_H=2^-" + str(int(-np.log2(H))) + "_g=" + str(g), text="polyfem_hex_H=2^-" + str(int(-np.log2(H))) + "_g=2^" + str(int(np.log2(g))), marker=dict(size=10)))
                x_values4, y_values4, name4 = accumulate_data_polyfem(data_list4, x_key, y_key, "H", H, "g", g)
                if(len(x_values4) >=3):
                    fig.add_trace(go.Scatter(x=-np.log2(x_values4), y=y_values4, mode= 'lines+markers',
                                        name="polyfem_prism_H=2^-" + str(int(-np.log2(H))) + "_g=" + str(g), text="polyfem_prism_H=2^-" + str(int(-np.log2(H))) + "_g=2^" + str(int(np.log2(g))), marker=dict(size=10)))
        fig.update_xaxes(
        ticktext=["2^-" + str(i ) for i in range(6,17)],
        tickvals=np.arange(6,17) )

    if x_key == "H":
            
        for h in thickness:
            # x_values1, y_values1, name1 = accumulate_data_pesopt(data_list1, x_key, y_key, "h", h)

            # fig.add_trace(go.Scatter(x=-np.log2(x_values1), y=y_values1, mode= 'lines+markers',
            #                         name="pesopt_h=2^-" + str(int(-np.log2(h))) , text="pesopt_h=2^-" + str(int(-np.log2(h))), marker=dict(size=10)))
            for g in outofplaneRes_div:
                x_values2, y_values2, name2 = accumulate_data_polyfem(data_list2, x_key, y_key,"h", h, "g", g)

                if(len(x_values2) >=3):
                    fig.add_trace(go.Scatter(x=-np.log2(x_values2), y=y_values2, mode= 'lines+markers',
                                        name="polyfem_tet_h=2^-" + str(int(-np.log2(h))) + "_g=" + str(g), text="polyfem_tet_h=2^-" + str(int(-np.log2(h))) + "_g=2^" + str(int(np.log2(g))), marker=dict(size=10)))
                x_values3, y_values3, name3 = accumulate_data_polyfem(data_list3, x_key, y_key,"h", h, "g", g)

                if(len(x_values3) >=3):
                    fig.add_trace(go.Scatter(x=-np.log2(x_values3), y=y_values3, mode= 'lines+markers',
                                        name="polyfem_hex_h=2^-" + str(int(-np.log2(h))) + "_g=" + str(g), text="polyfem_hex_h=2^-" + str(int(-np.log2(h))) + "_g=2^" + str(int(np.log2(g))), marker=dict(size=10)))
        fig.update_xaxes(
        ticktext=["2^-" + str(i ) for i in range(5,10)],
        tickvals=np.arange(5,10) )
        print(len(["2^-" + str(int(-np.log2(i) + min(-np.log2(x_values2)))) for i in x_values2]))
        print(len(-np.log2(x_values2) ))

    if x_key == "solve_time":
        for h in thickness:
            x_values1, y_values1, name1 = accumulate_data_pesopt(data_list1, x_key, y_key, "h", h)
        
            fig.add_trace(go.Scatter(x=x_values1, y=y_values1, mode= 'lines+markers',
                                name="pesopt_h=2^-" + str(int(-np.log2(h))) , text="pesopt_h=2^-" + str(int(-np.log2(h))), marker=dict(size=10)))
            for g in outofplaneRes_div:
                x_values2, y_values2, name2 = accumulate_data_polyfem(data_list2, x_key, y_key,"h", h, "g", g)

                if(len(x_values2) >=1):

                    fig.add_trace(go.Scatter(x=x_values2, y=y_values2, mode= 'lines+markers',
                                        name="polyfem_h=2^-" + str(int(-np.log2(h))) + "_g=" + str(g), text="polyfem_h=2^-" + str(int(-np.log2(h))) + "_g=" + str(g), marker=dict(size=10)))
                    
                try:
                    x_values3, y_values3, name3 = accumulate_data_polyfem(data_list3, x_key, y_key,"h", h, "g", g)

                    if(len(x_values3) >=1):

                        fig.add_trace(go.Scatter(x=x_values3, y=y_values3, mode= 'lines+markers',
                                            name="polyfem_hex_h=2^-" + str(int(-np.log2(h))) + "_g=" + str(g), text="polyfem_hex_h=2^-" + str(int(-np.log2(h))) + "_g=" + str(g), marker=dict(size=10)))
                        
                except KeyError:
                    continue
                fig.update_xaxes(type = 'log')

    fig.update_layout(title='Interactive Data Plot',
                    xaxis_title=x_key,
                    yaxis_title=y_key,
                    hovermode='closest',
                    yaxis_type='log'
                    )

    fig.show()