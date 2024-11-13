# Introduction

Dutasteride is a medication used to treat BPH and male pattern hair loss by lowering levels of the hormone dihydrotestosterone (DHT) in the body. It does this by competitively and irreversibly binding to the type 1 and type 2 5-alpha-reductase isoenzymes. This repository includes a single python script which predicts dutasteride levels in blood over time, DHT levels in blood over time, and scalp DHT levels at steady-state when dutaseride is taken orally. This simulation is entirely based on two papers, both by Gisleskog et al.:

1) [The pharmacokinetic modelling of GI198745 (dutasteride),
a compound with parallel linear and nonlinear elimination](https://bpspubs.onlinelibrary.wiley.com/doi/epdf/10.1046/j.1365-2125.1999.00843.x)

2) [A model for the turnover of dihydrotestosterone in the presence of the irreversible 5a-reductase inhibitors G1198745 and finasteride](https://csclub.uwaterloo.ca/~pbarfuss/gisleskog1998.pdf)

It uses the systems of differential equations provided by the authors to predict what the next values will be by employing numerical integration techniques. A timestep of 0.01 hours (36 seconds) ensures the accuracy and stability of the simulation.

This model is based on population averages. It will not exactly predict values for individuals because every person's body is different. The predictions provided by this application should not be used as a basis for making medical decisions. Do not modify your dosage or alter your dosing schedule based on the information from this application. Always consult your doctor before making any changes to your medication regimen.

Note: The Scalp DHT Suppression (%) plot is my own addition based on paper #2 as well as the Olsen et al. study (not listed) on scalp DHT reduction. This scalp DHT plot shows *projected* scalp DHT suppression if the *current* dutasteride blood concentration stayed constant over time. It does not represent real-time scalp DHT suppression but predicts what those levels would look like at steady-state serum dutasteride concentration. Only when the dutasteride serum concentration stabilizes (plateaus) can you interpret these values as true scalp DHT suppression. There was no data available that modeled the rate of clearance of DHT from scalp skin, so it is not known exactly how long it takes for scalp DHT to reflect serum dutasteride levels. At low doses of dutasteride (< 0.5 mg/day), there is likely to be higher person-to-person variation for scalp DHT suppression. Take this prediction with a grain of salt.

# Installing

The Windows prebuilt executable can be found under the releases section to the right of this page. You can either download the executable and simply open it, or you can download the python script and run it manually. If you use the script, you will need Python installed, as well as the NumPy and mplcursors packages. You can then open a console and type:

```
python dutasteride_modeling.py
```

You will need to use the console to enter dosing schedules.

# How to Use

Dosing schedules are entered into the console when the program is running. Once the graph is produced and a window opens to display it, the window may then be closed and the user will be prompted to enter another dosing schedule. Type 'q' to quit the program. Make sure to try the pan and zoom tools at the bottom left of the graph; you can click and drag using both the left and right mouse buttons for different effects. The home icon will reset the view.

### Format Examples:

Note: Time units can be any of: h, d, w, mo, y (hours, days, weeks, months, years). No unit provided = days.

| Schedule        | Explanation           |
| ------------- | ------------- |
| [0.5, 1d] x 90d      | 0.5 mg daily for 90 days. |
| [1, 2d] x 2mo    | 1 mg every other day for 2 months.      |
| [0.5, 3d, 1, 2d] x 16w | 0.5 mg, wait 3 days, 1 mg, wait 2 days, repeat for 16 weeks.      |
| [2.5, 1w] x 0.5y, [0.5, 1d] x 0.5y |2.5 mg per week for half a year, then 0.5 mg per day for half a year. |
| [0.5, MWF] x 45d | 0.5 mg on Monday Wednesday Friday for 45 days. |
| [1, SaSuTuTh] x 6mo | 1 mg on Saturday Sunday Tuesday Thursday for 6 months.|
| [0.5, 1d] x 1mo, [1, 1d] x 1mo, [1.5, 1d] x 1mo, [2, 1d] x 1mo | Increasing daily dose by 0.5 mg each month. |
| [0.5, MTh] x 3mo, [0, 1d] x 3mo, [0.5, 3d] x 3mo | 0.5 mg on Monday Thursday for 3 months, then stop for 3 months, then 0.5 mg every 3 days for 3 months |

If you want a smoother graph, you can simply choose an equivalent dose but with more frequency:

|                 |   |                      |  |                      |
| --------------- | - | -------------------- |- | -------------------- |
| [0.5, 1d] x 6mo | = | [0.125, 6h] x 6mo |  = | [0.02083, 1h] x 6mo |

# Screenshots:

### [0.5, 1d] x 90d - taking 0.5 mg daily for 90 days:
![screenshot 1](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/%5B0.5,%201d%5D%20x%2090d.png?raw=true)

### [2.5, 1w] x 0.5y, [0.5, 1d] x 0.5y - taking 2.5 mg/week for half a year, then 0.5 mg/day for half a year:
![screenshot 2](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/%5B2.5,%201w%5D%20x%200.5y,%20%5B0.5,%201d%5D%20x%200.5y.png?raw=true)

### [0.5, 1d] x 1mo, [1, 1d] x 1mo, [1.5, 1d] x 1mo, [2, 1d] x 1mo - taking 0.5 mg/day for a month, then 1 mg/day for a month, then 1.5 mg/day for a month, then 2 mg/day for a month:
![screenshot 3](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/%5B0.5,%201d%5D%20x%201mo,%20%5B1,%201d%5D%20x%201mo,%20%5B1.5,%201d%5D%20x%201mo,%20%5B2,%201d%5D%20x%201mo.png?raw=true)

### [0.5, 1d] x 6mo, [0, 1d] x 6mo - taking 0.5 mg/day for 6 months, then stopping for 6 months:
![screenshot 4](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/%5B0.5,%201d%5D%20x%206mo,%20%5B0,%201d%5D%20x%206mo.png?raw=true)

### [2.5, 1d] x 6mo, [0, 1d] x 6mo - taking 2.5 mg/day for 6 months, then stopping for 6 months:
![screenshot 5](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/%5B2.5,%201d%5D%20x%206mo,%20%5B0,%201d%5D%20x%206mo.png?raw=true)
