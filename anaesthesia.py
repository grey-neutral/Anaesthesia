
anaesthesia_info = {
    "Ultracain D- without Adrenaline": {
        "contraindications": [
            "Hypersensitivity to Articaine or other amide-type local anaesthetics",
            "AV block of second and third degree",
            "Acute decompensated heart failure",
            "Severe hypotension"
        ],
        "max_dosage_per_kg": 4  # mg per kg of body weight, as int for calculating
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

def main():
    patient_conditions = get_patient_conditions() # first we ask which conditions the patient has
    allowed_anaesthesia = which_anaesthesia(patient_conditions) # based on this the code will determine which anaesthesia the patient can get

    print("\nDecision:")
    if allowed_anaesthesia:
        print("The following anesthesia types are allowed:")
        for anaesthesia in allowed_anaesthesia:
            print(f"- {anaesthesia}") #lists all the allowed anaesthesia

        # Prompt for body weight and calculate the maximum dosage
        calculate_max_dosage(allowed_anaesthesia)
    else:
        print("No anaesthesia with Articaine is allowed based on the given conditions.")

def get_patient_conditions():

    patient_conditions = set() # keeps track of the conditions of the patient
    asked_conditions = set() # keeps track of duplicates

    print("Please answer with 'y' for yes and 'n' for no.")

    for _, details in anaesthesia_info.items(): #added "_" instead of "anaesthesia" as per pythonic convention, as "anaesthesia" isn't needed in this step

        #loop iterating over all conditions in the dictionary, adding them to the asked conditions set to avoid asking for the same condition twice
        for condition in details["contraindications"]:
            if condition not in asked_conditions:
                asked_conditions.add(condition)

                response = "" # initialised as empty string before it enters the while loop, because the variable needs to exist in advance
                while response not in ["y", "n"]: # ??
                    response = input(f"{condition}: ").strip().lower() #case insensitive input and no issues when the user hits space one too many times
                    if response not in ["y", "n"]:
                        print("Invalid input. Please enter 'y' for yes and 'n' for no." )

                if response == "y":
                    patient_conditions.add(condition)

    return patient_conditions #returns set of contraindications


def which_anaesthesia(patient_conditions): # checks which anaesthesia is allowed based on the conditions entered, then returns a list of allowed anaesthesia types

    allowed_anaesthesia =[]
    for anaesthesia, details in anaesthesia_info.items():
        if not any(cond in patient_conditions for cond in details["contraindications"]):
            allowed_anaesthesia.append(anaesthesia)
    return allowed_anaesthesia


def calculate_max_dosage(allowed_anaesthesia):

    while True:
        try:
            weight = float(input("\nEnter the patient's body weight in kg: ").strip()) # test if the calulation is rounded at the end or you get max dosage of 78.99999903843...
            if weight <= 0 or weight > 300: # accounts for nonsensical input such as 1000 kg or -50
                print("Please enter a valid weight between 1 and 300 kg.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    print("\nMaximum allowable dosage:") #\n for new line for better readability
    for anaesthesia in allowed_anaesthesia:

        # first bracket accesses the dictionary for the specific anaesthetic,
        # second bracket accesses the respective key-value pair with the max dosage in mg per kg of bodyweight
        max_dosage_per_kg = anaesthesia_info[anaesthesia]["max_dosage_per_kg"]

        max_dosage_mg = weight * max_dosage_per_kg
        max_dosage_ml = max_dosage_mg / 40  # 1 ml = 40 mg
        print(f"- {anaesthesia}: {max_dosage_mg:.1f} mg (~{max_dosage_ml:.1f} ml)")

if __name__ == "__main__":
    main()
