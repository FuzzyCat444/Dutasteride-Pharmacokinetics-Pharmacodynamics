# Introduction

Dutasteride is a medication used to treat BPH and male pattern hair loss by lowering levels of the hormone dihydrotestosterone (DHT) in the body. It does this by competitively and irreversibly binding to the type 1 and type 2 5-alpha-reductase isoenzymes. This repository includes a single python script which predicts dutasteride levels in blood over time, DHT levels in blood over time, and scalp DHT levels at steady-state when dutaseride is taken orally. This simulation is entirely based on two papers:

1) Gisleskog, P. O., Hermann, D., Hammarlund-Udenaes, M., Karlsson., M. O. (2001). The pharmacokinetic modelling of GI198745 (dutasteride),
a compound with parallel linear and nonlinear elimination. British Journal of Clinical Pharmacology. https://doi.org/10.1046/j.1365-2125.1999.00843.x

2) Gisleskog, P. O., Hermann, D., Hammarlund-Udenaes, M., Karlsson., M. O. (1998). A model for the turnover of dihydrotestosterone in the presence of the irreversible 5a-reductase inhibitors G1198745 and finasteride. Clinical Pharmacology and Therapeutics. https://doi.org/10.1016/S0009-9236(98)90054-6

It uses the systems of differential equations provided by the authors to predict what the next values will be by employing numerical integration techniques. A timestep of 0.01 hours (36 seconds) ensures the accuracy and stability of the simulation.

This model is based on population averages. It will not exactly predict values for individuals because every person's body is different. The predictions provided by this application should not be used as a basis for making medical decisions. Do not modify your dosage or alter your dosing schedule based on the information from this application. Always consult your doctor before making any changes to your medication regimen.

Note: The Scalp DHT Suppression (%) plot is my own addition based on paper #2 as well as the Olsen et al. study on scalp DHT reduction. This scalp DHT plot shows *projected* scalp DHT suppression if the *current* dutasteride blood concentration stayed constant over time. It does not represent real-time scalp DHT suppression but predicts what those levels would look like at steady-state serum dutasteride concentration. Only when the dutasteride serum concentration stabilizes (plateaus) can you interpret these values as true scalp DHT suppression. There was no data available that modeled the rate of clearance of DHT from scalp skin, so it is not known exactly how long it takes for scalp DHT to reflect serum dutasteride levels. At low doses of dutasteride (< 0.5 mg/day), there is likely to be higher person-to-person variation for scalp DHT suppression. Take this prediction with a grain of salt.

#### Scalp DHT Study:
- Olsen, E. A., Hordinsky, M., Whiting, D., Stough, D., Hobbs, S., Ellis, M. L., Wilson, T., Rittmaster, R. S. (2006). The importance of dual 5alpha-reductase inhibition in the treatment of male pattern hair loss: results of a randomized placebo-controlled study of dutasteride versus finasteride. Journal of the American Academy of Dermatology. https://doi.org/10.1016/j.jaad.2006.05.007

# Installing

The Windows prebuilt executable can be found under the releases section to the right of this page. You can either download the executable and simply open it, or you can download the python script and run it manually. If you use the script, you will need Python installed, as well as the NumPy and mplcursors packages. You can then open a console and type:

```
python dutasteride_modeling.py
```

You will need to use the console to enter dosing schedules.

# How to Use

Dosing schedules are entered into the console when the program is running. Once the graph is produced and a window opens to display it, the window may then be closed and the user will be prompted to enter another dosing schedule. Type 'q' to quit the program. Make sure to try the pan and zoom tools at the bottom left of the graph; you can click and drag using both the left and right mouse buttons for different effects. The home icon will reset the view.

### Format Examples:

Note: Time units can be any of: h, d, w, mo, y (hours, days, weeks, months, years). No unit provided = days. Schedules may be nested as deeply as needed using brackets to create complex regimens.

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
| [[0.5, MWF] x 3w, [0.5, MTh] x 1w] x 6mo | 0.5 mg on Monday Wednesday Friday for 3 weeks, then 0.5 mg on Monday Thursday for 1 week. Repeat this whole schedule for 6 months. |

If you want a smoother graph, you can simply choose an equivalent dose but with more frequency:

|                 |   |                      |  |                      |
| --------------- | - | -------------------- |- | -------------------- |
| [0.5, 1d] x 6mo | = | [0.125, 6h] x 6mo |  = | [0.02083, 1h] x 6mo |


# Scalp DHT Prediction at Steady State:

[Visit the desmos page for scalp DHT suppression predictions based on *daily* dose](https://www.desmos.com/calculator/y0comobcij). S(D) predicts scalp DHT suppression at steady state, given dose D in milligrams per day:

![scalp DHT](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/scalp_dht.PNG?raw=true)

<table>
<tr><th>Variables </th><th>Scalp DHT Suppression Predictions</th></tr>
<tr><td>

|       Variable:          |   |         Values             |
| --------------- | - | -------------------- |
| k<sub>23</sub> | = | 0.1936 |
| k<sub>32</sub> | = | 0.09911 |
| k<sub>20</sub> | = | 0.00337 |
| K<sub>m</sub> | = | 0.957 |
| V<sub>c</sub> | = | 173 |
| V<sub>max</sub> | = | 5.91 |
| FAR<sub>2</sub> | = | 0.358 |
| k<sub>1</sub> | = | 16.403 |
| k<sub>2</sub> | = | 2.436 |
| ko<sub>1G</sub> | = | 0.000594 |
| ko<sub>2G</sub> | = | 0.0357 |

</td><td>

|       *Daily* Dose (mg)          |   |        Scalp DHT Reduction (%)          |
| --------------- | - | -------------------- |
| 0.1 | = | 32% (known) |
| 0.5 | = | 51% (known) |
| 2.5 | = | 79% (known) |
| 1 | = | 63% |
| 1.5 | = | 70% |
| 2 | = | 75% |
| 3 | = | 82% |
| 5 | = | 88% |
| 10 | = | 93% |
| 15 | = | 95.4% |
| 20 | = | 96.5% |
| 30 | = | 97.6% |
| 40 | = | 98.2% |

</td></tr></table>

# Screenshots:

Note: Downsampling of the plot makes the serum dutasteride look more irregular than it is.

### Blood absorption curve after 0.5 mg administration
![screenshot 5](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/screenshot5.png?raw=true)

### Taking 0.5 mg daily for 90 days:
![screenshot 1](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/screenshot1.png?raw=true)

### Adding one 0.5 mg dose per week until reaching 0.5 mg/day:
![screenshot 2](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/screenshot2.png?raw=true)

### Taking 2.5 mg/day for a month, then stopping:
![screenshot 3](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/screenshot3.png?raw=true)

### Loading dose of 2 mg/day for a week, then 0.5 mg/day for 3 months:
![screenshot 4](https://github.com/FuzzyCat444/Dutasteride-Pharmacokinetics-Pharmacodynamics/blob/main/screenshots/screenshot4.png?raw=true)
