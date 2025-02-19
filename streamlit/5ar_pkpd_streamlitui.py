import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# helper functions
def validate_inputs(dose, duration) -> None:
    """Validates user inputs to ensure they are within acceptable ranges."""
    if dose <= 0:
        raise ValueError("Dose must be greater than 0.")
    if duration <= 0:
        raise ValueError("Duration must be greater than 0.")

def simulate_drug(dose: float, duration:int, decay_rate:float):
    """
    Simulates the serum concentration and DHT suppression for a given drug.

    Parameters:
        dose (float): Initial drug dose in mg.
        duration (int): Duration of simulation in days.
        decay_rate (float): Exponential decay rate of the drug.

    Returns:
        dict: Simulation results containing time, serum concentration, and DHT suppression.
    """
    time = np.linspace(0, duration, 100)
    serum_concentration = dose * np.exp(-decay_rate * time)
    dht_suppression = 100 * (1 - np.exp(-decay_rate * time))
    return {'time': time, 'serum_concentration': serum_concentration, 'dht_suppression': dht_suppression}

def plot_simulation(data:dict, drug_name:str, ax):
    """
    Plots the simulation results for a single drug.

    Parameters:
        data (dict): Simulation results from `simulate_drug`.
        drug_name (str): Name of the drug being simulated.
        ax (matplotlib.axes.Axes): Matplotlib axes object for plotting.
    """
    ax.plot(data['time'], data['serum_concentration'], label=f'{drug_name} Serum Concentration')
    ax.plot(data['time'], data['dht_suppression'], linestyle='--', label=f'{drug_name} DHT Suppression')
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Concentration / Suppression (%)")
    ax.legend()

# streamlit ui compontents 
st.title("Pharmacokinetic Model Simulation")

# userinput section
st.sidebar.header("Simulation Parameters")
drug_model = st.sidebar.selectbox(
    "Select the drug model:",
    ("Dutasteride", "Original Finasteride", "Tweaked Finasteride")
)
dose = st.sidebar.number_input(
    "Enter the dose in mg:",
    min_value=0.1,
    value=0.5,
    step=0.1,
    help="The initial dose of the drug in milligrams."
)
duration = st.sidebar.number_input(
    "Enter the duration in days:",
    min_value=1,
    value=90,
    step=1,
    help="The duration of the simulation in days."
)
compare_simulations = st.sidebar.checkbox("Compare simulations")

if compare_simulations:
    drugs_to_compare = st.sidebar.multiselect(
        "Select drug models to compare:",
        ["Dutasteride", "Original Finasteride", "Tweaked Finasteride"]
    )

# drug models and their decay rates
decay_rates = {
    "Dutasteride": 0.05,
    "Original Finasteride": 0.03,
    "Tweaked Finasteride": 0.1
}

# main logic for the simulation 
try:
    validate_inputs(dose, duration)

    if st.sidebar.button("Simulate"):
        if compare_simulations and drugs_to_compare:
            # Plot comparison of multiple drugs
            fig, ax = plt.subplots(figsize=(10, 6))
            for drug in drugs_to_compare:
                decay_rate = decay_rates[drug]
                data = simulate_drug(dose, duration, decay_rate)
                plot_simulation(data, drug, ax)
            ax.set_title("Comparison of Drug Models")
            st.pyplot(fig)
        else:
            # Simulate and plot a single drug model
            decay_rate = decay_rates[drug_model]
            data = simulate_drug(dose, duration, decay_rate)

            fig, ax = plt.subplots(figsize=(10, 6))
            plot_simulation(data, drug_model, ax)
            ax.set_title(f"Simulation for {drug_model}")
            st.pyplot(fig)

except ValueError as e:
    st.error(f"Input Error: {e}")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")
