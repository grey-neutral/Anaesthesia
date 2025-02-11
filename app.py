import streamlit as st

# --------------------------------------
# 1. Dictionary containing all info
# --------------------------------------
anaesthesia_info = {
    "Ultracain D- without Adrenaline": {
        "contraindications": [
            "Hypersensitivity to Articaine or other amide-type local anaesthetics",
            "AV block of second and third degree",
            "Acute decompensated heart failure",
            "Severe hypotension"
        ],
        "max_dosage_per_kg": 4  # mg per kg of body weight
    },
    "Ultracain D-S 1:200,000": {
        "contraindications": [
            "Hypersensitivity to Articaine or other amide-type local anaesthetics",
            "Hypersensitivity to Epinephrine",
            "Bronchial asthma with sulfite hypersensitivity",
            "AV block of second and third degree",
            "Acute decompensated heart failure",
            "Severe hypotension",
            "Non-cardioselective beta blockers (e.g., Propranolol)",
            "Paroxysmal tachycardia or high-frequency absolute arrhythmia",
            "Hyperthyroidism",
            "Pheochromocytoma",
            "Narrow-angle glaucoma"
        ],
        "max_dosage_per_kg": 7
    },
    "Ultracain D-S forte 1:100,000": {
        "contraindications": [
            "Hypersensitivity to Articaine or other amide-type local anaesthetics",
            "Hypersensitivity to Epinephrine",
            "Bronchial asthma with sulfite hypersensitivity",
            "AV block of second and third degree",
            "Acute decompensated heart failure",
            "Severe hypotension",
            "Non-cardioselective beta blockers (e.g., Propranolol)",
            "Paroxysmal tachycardia or high-frequency absolute arrhythmia",
            "Hyperthyroidism",
            "Pheochromocytoma",
            "Narrow-angle glaucoma"
        ],
        "max_dosage_per_kg": 7
    }
}

# --------------------------------------
# 2. Helper functions
# --------------------------------------
def which_anaesthesia(patient_conditions):
    """
    Returns a list of anaesthesia types allowed
    based on the patient's conditions.
    """
    allowed = []
    for anaesthesia, details in anaesthesia_info.items():
        # If NONE of the contraindications match the patient's conditions,
        # that anaesthesia is allowed.
        if not any(cond in patient_conditions for cond in details["contraindications"]):
            allowed.append(anaesthesia)
    return allowed


def calculate_max_dosage(allowed_anaesthesia, weight):
    """
    Given the allowed anaesthesia list and the patient's weight,
    calculates the maximum dosage in mg and ml.
    """
    results = []
    for anaesthesia in allowed_anaesthesia:
        max_dosage_per_kg = anaesthesia_info[anaesthesia]["max_dosage_per_kg"]
        max_dosage_mg = weight * max_dosage_per_kg
        max_dosage_ml = max_dosage_mg / 40.0  # 1 ml = 40 mg
        results.append({
            "anaesthesia": anaesthesia,
            "max_dosage_mg": max_dosage_mg,
            "max_dosage_ml": max_dosage_ml
        })
    return results


# --------------------------------------
# 3. Set up session state
# --------------------------------------
# We only initialize these once:
if "selected_conditions" not in st.session_state:
    st.session_state.selected_conditions = set()
if "allowed_anaesthesia" not in st.session_state:
    st.session_state.allowed_anaesthesia = []
if "show_results" not in st.session_state:
    st.session_state.show_results = False


# --------------------------------------
# 4. Main app
# --------------------------------------
def main():
    st.title("Articaine-based Anaesthesia Evaluator (Ultracain)")
    st.write(
        "This Python application helps to identify the right type of Articaine-based anaesthesia (Ultracain) "
        "by evaluating contraindications based on patient medical conditions and calculates the maximum allowable "
        "dosage based on the patient's body weight."
        "This app is for informational purposes only, not intended for medical use!"
    )

    # Collect all unique contraindications from the dictionary
    all_contraindications = set()
    for info in anaesthesia_info.values():
        for c in info["contraindications"]:
            all_contraindications.add(c)

    # Sort them for consistent display
    sorted_contraindications = sorted(all_contraindications)

    st.subheader("1. Patient Conditions")
    st.write("Check all contraindications that apply to the patient:")

    # Let the user select the contraindications via checkboxes
    temp_selected = []
    for condition in sorted_contraindications:
        # Pre-check the box if it was selected before (stored in session_state)
        is_checked = condition in st.session_state.selected_conditions
        if st.checkbox(condition, value=is_checked):
            temp_selected.append(condition)

    # This ephemeral list is for the current run; store the final set in session state
    st.session_state.selected_conditions = set(temp_selected)

    # Button to evaluate
    if st.button("Check Allowed anaesthesia"):
        st.session_state.allowed_anaesthesia = which_anaesthesia(st.session_state.selected_conditions)
        st.session_state.show_results = True

    # If no anaesthesia is allowed, show a warning (only if the user clicked the button)
    # or if the user has indicated they want results
    if st.session_state.show_results:
        if len(st.session_state.allowed_anaesthesia) == 0:
            st.error("No Articaine-based anaesthesia is allowed for the given conditions.")
        else:
            st.success("The following anaesthesia types are allowed:")
            for anaesthesia in st.session_state.allowed_anaesthesia:
                st.write(f"• {anaesthesia}")

            # Now let the user input weight
            st.subheader("2. Patient Weight")
            weight = st.number_input(
                "Enter the patient's body weight (kg):", 
                min_value=1.0, 
                max_value=300.0, 
                value=70.0, 
                step=0.5
            )

            # Calculate the dosage
            results = calculate_max_dosage(st.session_state.allowed_anaesthesia, weight)
            st.subheader("3. Maximum Allowable Dosage")
            for item in results:
                st.write(
                    f"**{item['anaesthesia']}**: "
                    f"{item['max_dosage_mg']:.1f} mg (~{item['max_dosage_ml']:.1f} ml)"
                )


if __name__ == "__main__":
    main()
