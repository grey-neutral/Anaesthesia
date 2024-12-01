# Anaesthesia
This Python application helps to identify the right type of Articaine-based anaesthesia (Ultracain) by evaluating contraindications based on patient medical conditions and calculates the maximum allowable dosage based on the patient's body weight.

You'll find further in-depth descriptions of what each segment of code is meant to do in the #comments

The anaesthesia_info dictionary is based on the following document (in German):
https://www.unimedizin-mainz.de/fileadmin/kliniken/zahnerhaltung/Dokumente/lokalanaesthetika.pdf


This code is for informational purposes only, not intended for medical use!

## Features

- Interactive patient condition screening
- Contraindication checking for three types of Ultracain anaesthesia
- Precise dosage calculation based on patient weight

## Supported Anaesthesia Types

- Ultracain D- without Adrenaline
- Ultracain D-S 1:200,000
- Ultracain D-S forte 1:100,000

## Prerequisites

- Python 3.12.7 (for optimal use)

## Usage

Run the script directly:
```
python project.py
```

Follow the prompts to:
- Input patient medical conditions
- Enter patient's body weight
- Receive recommended anaesthesia type and maximum dosage

## Running Tests

Execute the test suite:
```
pytest test_project.py
```

## Project Components

### project.py

This is the main script where all the logic resides. It consists of three primary functions:

#### get_patient_conditions:
This function collects patient medical conditions interactively. The user is prompted to confirm or deny the presence of each contraindication by answering "y" for yes or "n" for no. It stores the patient's conditions in a set, ensuring duplicate conditions are not checked multiple times.

#### which_anaesthesia:
This function takes the set of patient conditions and determines which types of anaesthesia are allowed. It compares the conditions against the contraindications of each anaesthesia type and returns a list of compatible options.

#### calculate_max_dosage:
This function calculates the maximum allowable dosage for the patient. The user is prompted to input the patient's body weight (in kilograms). The program validates the input to ensure it falls within the acceptable range (1–300 kg). Using the weight and the specific dosage limits for each anaesthesia type, it calculates the maximum dosage in milligrams and milliliters, providing results for each allowed anaesthesia type.

Finally, the main function brings all of these components together, prompting the user to enter conditions, determining allowed anaesthesia types, and calculating dosages. If no anaesthesia is suitable, it informs the user appropriately. The programme is designed in a way that it only calculates


### test_project.py
This file contains unit tests to validate the functionality of the program. It uses Python's unittest and unittest.mock modules to test each function individually. It doesn't however check whether the maximum dosage in mg and ml is calculated correctly.

#### test_get_patient_conditions:
Mocks user inputs to simulate different patient scenarios and verifies the correctness of the returned set of conditions.

#### test_which_anaesthesia:
Tests whether the program correctly identifies allowed anaesthesia types based on input conditions. It uses a series of predefined test cases resulting in either all three, one or none types of anaesthesia being allowed. Note that the contraindications of two of the anaesthesia types are identical, therefore there is no case where only two types of anaesthesia would be marked as allowed.

#### test_invalid_weight:
Verifies that the calculate_max_dosage function correctly handles invalid weight inputs. It tests various invalid inputs, such as:

Negative numbers, unrealistic weights (e.g., 1000 kg), or zero.
Non-numerical inputs, such as "cat" or "fifty."
Empty or whitespace-only inputs.

Using mock inputs, the test ensures:

The function re-prompts the user when an invalid input is provided.
An appropriate error message, such as "Please enter a valid weight between 1 and 300 kg," is printed for invalid inputs.
After providing a valid weight (e.g., 70 kg), the function calculates the correct dosage without further error messages.

#### test_valid_weight:
Verifies if calculate_max_dosage() accepts valid weight inputs, and doesn't result in an error message/ rempromt.
It uses valid weights at both normal and edge values, such as 50 kg, 100 kg, 1 kg (minimum), and 300 kg (maximum).

The test ensures:

No error messages are printed for valid inputs.
The function proceeds to calculate the correct maximum dosage for the provided weight and anaesthesia type.

## Limitations:

- The programme only focuses on absolute contraindications, not relative contraindications
- The programme doesn't take into consideration the length or type of the procedure,
  which would be e.g. relevant for deciding whether to use Ultracain D-S 1:200,000 vs Ultracain D-S forte 1:100,000;
  the latter of which has a longer lasting effect
- The programme only takes into account 3 types of local anaesthesia, all of which are Articaine-based.
  While Articaine is commonly used in European countries, Lidocaine, Prilocaine, Mepivacaine, and Bupivacaine are also used for dental anaesthesia
- The programme only allows input in kg, not other weight units


## Safety Notes

This tool is for informational purposes only, not intended for medical use.

## License

This project is licensed under the MIT License.

## Author

GitHub @grey_neutral
