from flask import Flask, render_template, request, redirect
from MyFunctions import opt_func, predict_output, visualise
import numpy as np
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


app = Flask(__name__,template_folder='templates', static_folder='templates/styles')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'About':
            return redirect('/about')
        elif request.form['submit'] == 'Prediction':
            return redirect('/prediction')
        elif request.form['submit'] == 'optimisation':
            return redirect('/optimisation')
        elif request.form['submit'] == 'data visualization':
            return redirect('/dataviz')
    return render_template('Home.html')

@app.route('/about')
def about():
    return render_template('aboutpage.html')

@app.route('/prediction')
def prediction():
    return render_template('predpage.html')

@app.route('/optimisation')
def optimisation():
    return render_template('optpage.html')


@app.route('/dataviz', methods=['GET', 'POST'])
def dataviz():
    if request.method == 'POST':
        selected_option = request.form['figure']
        figure = generate_figure(selected_option)
        graphJSON = pio.to_json(figure)
        return graphJSON
    return render_template('datavizpage.html')

@app.route('/display-figure', methods=['POST'])

def display_figure():
    selected_option = request.form['figure']
    
    figure_data,figure_layout = generate_figure(selected_option)
    
    graphJSON = pio.to_json(dict(data=figure_data, layout=figure_layout))
    return graphJSON

def generate_figure(selected_option):
    # Generate the figure based on the selected option
    # Replace with your code to generate the corresponding figure
    custom_colors = [
    [0.0,  '#ffc42f'],  
    [0.5, '#8adca2'], 
    [1.0,'rgb(119, 182, 207)'] 
    ]
    datelist,powerlist, speedlist, temperaturelist, dplist, feedlist, ratelist, chainlist = visualise()
    if selected_option == 'correlations':
            
            data = [powerlist, speedlist, temperaturelist, dplist, feedlist, ratelist, chainlist]
            labels = ['Mill Power', 'Main Drive Speed', 'Input Temperature', 'DP Mill', 'Coal Mill Feed Rate', 'Exhaust Air Rate', 'Transport Chain Speed']
            
            correlation_matrix = np.corrcoef(data)
            fig = go.Figure(data=go.Heatmap(z=correlation_matrix, colorscale=custom_colors))
            fig.update_layout(
                title='Feature Correlations',
                height=500,
                xaxis=dict(title='Values', tickmode='array', tickvals=list(range(len(labels))), ticktext=labels),
                yaxis=dict(title='Values', tickmode='array', tickvals=list(range(len(labels))), ticktext=labels)
            )  
    elif selected_option == 'millpower':
            

        fig = go.Figure(data=go.Scatter(
            x=datelist,
            y=powerlist,
            mode='markers',
            marker=dict(
                color=powerlist,  
                colorscale=custom_colors, 
                colorbar=dict(title='Power'),  
                showscale=True  
            )
        ))
        fig.update_layout(
            title='Mill Power (2021-2023)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Mill Power')
        )

            
    elif selected_option == 'drivespeed':
            
        fig = go.Figure(data=go.Scatter(
            x=datelist,
            y=speedlist,
            mode='markers',
            marker=dict(
                color=speedlist,  
                colorscale=custom_colors, 
                colorbar=dict(title='Drive Speed'),  
                showscale=True  
            )
        ))
        fig.update_layout(
            title='Main Drive Speed (2021-2023)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Main Drive Speed')
        )

    elif selected_option == "temperature":
        fig = go.Figure(data=go.Scatter(
            x=datelist,
            y=temperaturelist,
            mode='markers',
            marker=dict(
                color=temperaturelist,
                colorscale=custom_colors,
                colorbar=dict(title='Temperature'),
                showscale=True
            )
        ))
        fig.update_layout(
            title='Input Temperature (2021-2023)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Input Temperature')
        )
    elif selected_option == "dpMill":
        fig = go.Figure(data=go.Scatter(
            x=datelist,
            y=dplist,
            mode='markers',
            marker=dict(
                color=dplist,
                colorscale=custom_colors,
                colorbar=dict(title='DP Mill'),
                showscale=True
            )
        ))
        fig.update_layout(
            title='DP Mill (2021-2023)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='DP Mill')
        )
    elif selected_option == "millfeedrate":
        fig = go.Figure(data=go.Scatter(
            x=datelist,
            y=feedlist,
            mode='markers',
            marker=dict(
                color=feedlist,
                colorscale=custom_colors,
                colorbar=dict(title='Mill Feed Rate'),
                showscale=True
            )
        ))
        fig.update_layout(
            title='Coal Mill Feed Rate (2021-2023)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Mill Feed Rate')
        )
    elif selected_option == "air":
        fig = go.Figure(data=go.Scatter(
            x=datelist,
            y=ratelist,
            mode='markers',
            marker=dict(
                color=ratelist,
                colorscale=custom_colors,
                colorbar=dict(title='Exhaust Air Rate'),
                showscale=True
            )
        ))
        fig.update_layout(
            title='Exhaust Air Rate (2021-2023)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Exhaust Air Rate')
        )
    elif selected_option == "speed":
        fig = go.Figure(data=go.Scatter(
            x=datelist,
            y=speedlist,
            mode='markers',
            marker=dict(
                color=speedlist,
                colorscale=custom_colors,
                colorbar=dict(title='Transport Chain Speed'),
                showscale=True
            )
        ))
        fig.update_layout(
            title='Transport Chain Speed (2021-2023)',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Transport Chain Speed')
        )

                
    else:
            data = [powerlist, speedlist, temperaturelist, dplist, feedlist, ratelist, chainlist]
            labels = ['Mill Power', 'Main DriveSpeed', 'Input Temperature', 'DP Mill', 'Coal Mill Feed Rate', 'Exhaust Air Rate', 'Transport Chain Speed']
            
            correlation_matrix = np.corrcoef(data)
            fig = go.Figure(data=go.Heatmap(z=correlation_matrix, colorscale='Viridis'))
            fig.update_layout(
                title='Feature Correlations',
                height=500,
                xaxis=dict(title='Values', tickmode='array', tickvals=list(range(len(labels))), ticktext=labels),
                yaxis=dict(title='Values', tickmode='array', tickvals=list(range(len(labels))), ticktext=labels)
            )  
    
    return fig.data, fig.layout




@app.route('/enter-target',methods = ['POST'])
def target():
   # if request.method == 'POST':
   thisform = request.form
   thisdict = thisform.to_dict(flat=True)
   out1 = float(thisdict['millpowertarget'])
   out2 = float(thisdict['drivespeedtarget'])
   outs = opt_func(out1,out2)
   out3, out4, out5 = outs

   return render_template("displayopt.html",
                           out1 =int(out1),
                           out2 = int(out2), 
                           out3=int(out3), 
                           out4 =int(out4),
                           out5 = int(out5) )


@app.route('/enter-inputs',methods = ['POST'])
def pred():
   # if request.method == 'POST':
   
   thisform = request.form
   thisdict = thisform.to_dict(flat=True)
   # out1 = float(thisdict['Inputtemperature'])
   # out2 = float(thisdict['DPmill'])
   # out3 = float(thisdict['Millfeedrate'])
   # out4 = float(thisdict['Exhaustairflowrate'])
   # out5 = float(thisdict['Raclettechainspeed'])
   out1 = thisdict['Inputtemperature']
   out2 = thisdict['Exhaustairflowrate']
   out3 = thisdict['Transportchainspeed']


   out4,out5 = predict_output(out1,out2,out3)

   return render_template("displaypred.html",
                           out1 =int(out1),
                           out2 = int(out2), 
                           out3=int(out3), 
                           out4 =int(out4),
                           out5 = int(out5))

if __name__ == '__main__':
   app.run(debug = True)