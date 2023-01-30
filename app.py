from dash import Dash
from dash import dcc
from dash import html, Input, Output
import pandas as pd
import numpy as np
google_sheet_id = "1SioYuKsX0MhM7gA6XVs4UoMnfD_KXSyIOnT0ofwwk1A"
sheet_name = "Form responses 1"
google_sheet_url = "https://docs.google.com/spreadsheets/d/{}/gviz/tq?tqx=out:csv&sheet={}".format(google_sheet_id, sheet_name) #converts the google sheet to csv
google_sheet_url= google_sheet_url.replace(" ","%20")
Seven_form = pd.read_csv(google_sheet_url)
list_of_months = ["empty","January","Feburary","March","April","May","June","July","August","Spetember","October","November","December"]
x_interim = Seven_form[["Timestamp","Order Amount","Order Quantity","Email"]]
x = []
for i in x_interim["Timestamp"]:
     x1 = list_of_months[int(str(i).split("/",3)[1])]
     x.append(x1)

x_interim["Month"] = x
new_data =pd.DataFrame(x_interim.groupby(["Email"])["Order Amount","Order Quantity","Email"].count())

app = Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1(children= "24Seven order from data",),
        html.P(children= "Display data based on initial business requirement",),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": x,
                        "y": Seven_form["Order Amount"],
                        "type": "bar"
                    },    
                ],
                "layout": {"title": "Order Quantity by month"}
            }
        ),
        html.H4(children = "Summary"),
        html.Span(children= "GMV: {:,}".format(round(np.sum(Seven_form["Order Amount"]))),className="border border-success",style={"border":"border border-success"}), html.Br(),
        html.Span(children="Average Order qunatity: {}".format(round(np.mean(Seven_form["Order Quantity"]),0)),className="border border-success"), html.Br(),
        html.Span(children="Average Order value: {:,}".format(round(np.mean(Seven_form["Order Amount"]),0)),className="border border-success"), html.Br(),
        html.Span(children="Number of users: {}".format(np.count_nonzero(new_data["Email"])),className="border border-success"),
        html.Div(
            children = [
            html.H4(children="Data by month"),
            html.P(children="Select the month and the type of data you want to see"),
            dcc.Dropdown(
                id= "my_drop",
                options= list_of_months,
                value= list_of_months[1]
            ),
            dcc.RadioItems(
                id="my_radio",
                options = ["sum","mean","standard deviation","minimum","maximum"],
                value = "sum"
            )   
        ]),
        html.Br(),
        html.Div(id = "my_output", style={'width': '48%', 'float': 'left', 'display': 'inline-block'})
    ]
)

@app.callback(
  Output(component_id="my_output", component_property="children"),
  Input(component_id="my_drop", component_property="value"),
  Input(component_id="my_radio", component_property="value") 
)
def data_by_month (Month,Method):
  "The function will return the Order Amount and Quantity based on the" 
  "selected month. The predeined methods are: sum, mean, standdard deviation, minimum, and maximum"

  mean_data = x_interim.groupby(["Month"])["Order Amount","Order Quantity","Email"].mean()
  sum_data = x_interim.groupby(["Month"])["Order Amount","Order Quantity","Email"].sum()
  std_data = x_interim.groupby(["Month"])["Order Amount","Order Quantity","Email"].std()
  min_data = x_interim.groupby(["Month"])["Order Amount","Order Quantity","Email"].min()
  max_data = x_interim.groupby(["Month"])["Order Amount","Order Quantity","Email"].max()
  if Method == "mean":
    main_data = mean_data
  elif Method == "sum":
      main_data = sum_data
  elif Method == "standard deviation":
      main_data = std_data
  elif Method == "minimum":
      main_data = min_data
  elif Method == "maximum":
      main_data = max_data
  result_data = ["Order Amount: {:,}".format(round(main_data["Order Amount"][Month]),0), html.Br(),
  "Order Quantity: {:,}".format(round(main_data["Order Quantity"][Month]),0)]
  return result_data

if __name__ == "__main__":
    app.run_server(debug = True)