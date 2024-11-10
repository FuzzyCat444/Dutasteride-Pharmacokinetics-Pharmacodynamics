# Introduction

Dutasteride is a medication used to treat BPH and male pattern hair loss by lowering levels of the hormone dihydrotestosterone (DHT) in the body. It does this by competitively and irreversibly binding to the type 1 and type 2 5-alpha-reductase isoenzymes. This repository includes a single python script which predicts dutasteride levels in blood over time, DHT levels in blood over time, and scalp DHT levels at steady-state. This simulation is entirely based on two papers, both by Gisleskog et al.:

1) [The pharmacokinetic modelling of GI198745 (dutasteride),
a compound with parallel linear and nonlinear elimination](https://bpspubs.onlinelibrary.wiley.com/doi/epdf/10.1046/j.1365-2125.1999.00843.x)

2) [A model for the turnover of dihydrotestosterone in the presence of the irreversible 5a-reductase inhibitors G1198745 and finasteride](https://sci-hub.st/10.1016/s0009-9236(98)90054-6)

This model is based on population averages. It will not exactly predict values for individuals because every person's body is different. The predictions provided by this application should not be used as a basis for making medical decisions. Do not modify your dosage or alter your dosing schedule based on the information from this application. Always consult your doctor before making any changes to your medication regimen.

# Installing

You either download the Windows prebuilt executable and simply open it, or you can download the python script and run it manually. If you use the script, you will need Python installed, as well as the NumPy and mplcursors packages. You can then open a console and type:

```
python dutasteride_modeling.py
```

You will need to use the console to enter dosing schedules.

# How to Use

