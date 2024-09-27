from dash import Dash, dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

###################
### initialization
###################

df = pd.read_csv('https://raw.githubusercontent.com/Stochastic1017/Body_Fat_Study/refs/heads/main/dataset/BodyFat.csv')
app = Dash(__name__)

############################
### plot correlation matrix
############################

correlation_matrix = df.iloc[:, 1:len(df.columns)].corr()

sorted_columns = correlation_matrix.sum().sort_values().index
sorted_corr_matrix = correlation_matrix.loc[sorted_columns, sorted_columns]

heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Inferno'
    )
)

########################
### describe app layout
########################

app.layout = [
    html.H1("Body Fat Estimation Made Easy: A Data-Driven Approach", 
            style={'text-align': 'center', 'color': '#ee6c4d'}),

    html.H2("Authors: Shrivats Sudhir, Jiren Lu, Will Wang, Zekai Xu", 
            style={'text-align': 'center', 'color': '#807A79', 'font-size': 15}),

    html.H3("Introduction:", 
            style={'text-align': 'left', 'color': '#293241'}),

    html.P("Accurate measurement of body fat can often be inconvenient or costly. "
           "However, it is important to have methods that make it easy to estimate body fat "
           "without these barriers. This project presents a simple, robust, and accurate model "
           "for estimating body fat percentage using measurements that are readily available in clinical settings.",
           style={'text-align': 'left', 'color': '#333'}),

    html.P("Based on a dataset of 252 men, which includes measurements of their body fat percentage "
           "and various body circumference measurements (such as chest, abdomen, and thigh), we aim to develop "
           "a 'rule-of-thumb' for estimating body fat. This model is designed to be practical and applicable "
           "to a wide range of clinical contexts, providing a reliable estimate without the need for specialized equipment.",
           style={'text-align': 'left', 'color': '#333'}),

    html.H3("About the Dataset:", 
            style={'text-align': 'left', 'color': '#293241'}),

    html.P("A variety of popular health books suggest that the readers assess their health, at least in "
           "part, by estimating their percentage of body fat. In Bailey (1994), for instance, the reader "
           "can estimate body fat from tables using their age and various skin-fold measurements "
           "obtained by using a caliper. Other texts give predictive equations for body fat using body "
           "circumference measurements (e.g. abdominal circumference) and/or skin-fold "
           "measurements. See, for instance, Behnke and Wilmore (1974), pp. 66-67; Wilmore "
           "(1976), p. 247; or Katch and McArdle (1977), pp. 120-132).",
           style={'text-align': 'left', 'color': '#333'}),

    html.P("Percentage of body fat for an individual can be estimated once body density has been "
           "determined. Folks (e.g. Siri (1956)) assume that the body consists of two components - "
           "lean body tissue and fat tissue. Letting",
           style={'text-align': 'left', 'color': '#333'}),

    dcc.Markdown('''
* $D=$ Body Density ($\\text{gm}/\\text{cm}^3$)
* $A=$ Proportion of Lean Body Tissue
* $B=$ Proportion of Fat Tissue ($A+B=1$)
* $a=$ Density of Lean Body Tissue ($\\text{gm}/\\text{cm}^3$)
* $b=$ Desntiy of Fat Tissue ($\\text{gm}/\\text{cm}^3$)

we have:

$$D = \\frac{1}{(A/a) + (B/b)}$$

Solving for $B$, we find:

$$B=\\frac{1}{D} \\times \\bigg[\\frac{ab}{(a-b)}\\bigg] - \\bigg[\\frac{b}{a-b}\\bigg]$$

Using the estimes $a=1.10\\text{ gm}/\\text{cm}^3$ and $b=0.90\\text{ gm}/\\text{cm}^3$  (see Katch and McArdle (1977), p. 111 or Wilmore (1976), p. 123) we come up with "Siri's equation":

$$\\text{Percentage of Body Fat (i.e. 100 $\\times B$)}=\\frac{495}{D}-450$$

The technique of underwater weighing "computes body volume as the difference between body weight measured in air and weight measured during water submersion. 
In other words, body volume is equal to the loss of weight in water with the appropriate
temperature correction for the water's density" (Katch and McArdle (1977), p. 113).

Using this technique:
                 
$$\\text{Body Density} = \\frac{\\text{WA}}{[(\\text{WA} - \\text{WW})/\\text{c.f.} - \\text{LV}]}$$

where (Katch and McArdle (1977), p. 115)
                 
* $\\text{WA}=$ Weight in air (kg)
* $\\text{WW}=$ Weight in water (kg)                 
* $\\text{c.f.}=$ Water correction factor ($=1$ at $39.2$ deg $F$ as one-gram of water occupies exactly on $\\text{cm}^3$ at this temperature, $=0.997$ at $76-78$ deg $F$)
* $\\text{LV}=$ Residual Lung Volume (liters)

Other methods of determining body volume are given in Behnke and Wilmore (1974), p.
22 ff.

Unfortunately, the above process of determining body volume by underwater submersion,
while accurate, can be cumbersome and difficult to use by doctors who want to and easily
quickly determine a patient’s body fat percentage based on commonly available
measurements, even if it means sacrificing some accuracy guaranteed by underwater
measurements.
                 
The commonly available measurements include age, weight, height, bmi, and various
body circumference measurements. In particular, the variables listed below (from left to
right in the data set) are:

* ID number of individual: `IDNO`
* Percent body fat from Siri's (1956) equation: `BODYFAT`
* Density determined from underwater weighing: `DENSITY`
* Age (years): `AGE`
* Weight (lbs): `WEIGHT`
* Height (inches): `HEIGHT`
* Adioposity (bmi): `ADIPOSITY`
* Neck circumference (cm): `NECK`
* Chest circumference (cm): `CHEST`
* Abdomen 2 circumference (cm): `ABDOMEN`
* Hip circumference (cm): `HIP`
* Thigh circumference (cm): `THIGH`
* Knee circumference (cm): `KNEE`
* Ankle circumference (cm): `ANKLE`
* Biceps (extended) circumference (cm): `BICEPS`
* Forearm circumference (cm): `FOREARM`
* Wrist circumference (cm): `WRIST`   

Measurement standards are listed in Benhke and Wilmore (1974), pp. 45-48 where, for
instance, the abdomen 2 circumference is measured "laterally, at the level of the iliac
crests, and anteriorly, at the umbilicus."                      
''', mathjax=True),

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 15,
        style_header={
        'color': 'white',
        'backgroundColor': '#293241',
        'fontWeight': 'bold',
        'textAlign': 'center'},
        style_cell={
        'textAlign': 'center'},
    ),
]


#---------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)