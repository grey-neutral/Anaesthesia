from project import get_patient_conditions, which_anaesthesia, calculate_max_dosage
from unittest.mock import patch # https://docs.python.org/3/library/unittest.mock.html


def test_get_patient_conditions(): # tests that function counts the inputs correctly (only the y input)
    inputs = [
        # first input scenario: Patient has no conditions, 0x yes
        ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
        # patient has some conditions present 2x yes
        ['y', 'n', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n'],
        # Yes to everything, 11 x yes
        ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']
    ]

    for input_scenario in inputs: # each input scenario represents a test case with answers to the 11 anamnesis questions
        with patch('builtins.input', side_effect=input_scenario): # we need patch here, because the programme is expecting user input, I simulated 3 input test cases in the input list
            conditions = get_patient_conditions()
            assert isinstance(conditions, set) #checks if "conditions" variable is a type of set -> set e.g. {"Hypersensitivity to Articaine or other amide-type local anaesthetics","Acute decompensated heart failure"} in scenario 2

            assert len(conditions) == input_scenario.count('y') #checks if number (length) of conditions in set matches the number of yes replies

def test_which_anaesthesia():
    test_cases = [
        #tests that all anaesthesia is allowed, if no contraindications are present
        (set(), 3),
        #tests that only 1 type of anaesthesia is allowed (Ultracain D without adrenaline),
        #if the patient has a condition that is present in the second and third dictionary entry (note: contents are identical) but not the first
        ({"Hypersensitivity to Epinephrine", "Bronchial asthma with sulfite hypersensitivity",
          "Paroxysmal tachycardia or high-frequency absolute arrhythmia",
          "Non-cardioselective beta blockers (e.g., Propranolol)", "Hyperthyroidism",
          "Pheochromocytoma", "Narrow-angle glaucoma"}, 1),

        ({"Hypersensitivity to Epinephrine", "Bronchial asthma with sulfite hypersensitivity", "Narrow-angle glaucoma"}, 1),
        # tests that no anaesthesia is allowed if conditions are present, where Articaine is not allowed
        ({"Hypersensitivity to Articaine or other amide-type local anaesthetics",
            "AV block of second and third degree"}, 0)
    ]
    for conditions, expected_allowed_count in test_cases: #separates conditions from expected number of anaesthesia
        allowed = which_anaesthesia(conditions) #which anaesthesia will output the types of anaesthesia allowed
        assert len(allowed) == expected_allowed_count # this checks if the number (length) of types of anaesthesia allowed matches up with the expected count as specified in test_cases


def test_invalid_weight(): # tests if calculate_max_dosage rejects invalid weight inputs
    invalid_inputs =[
        "-50", #no negative weights
        "1000", #no unrealistic weights
        "0", #edge cases 0 and 300.1
        "300.1",
        "cat", #no nonsensical strings as input
        " ", #no nothing as input
        "",
        "fifty" #no words as input
    ]

    allowed_anaesthesia = ["Ultracain D-S 1:200,000"]

    for invalid_weight in invalid_inputs:
        with patch('builtins.input', side_effect=[invalid_weight, "70"]): # first input should a invalid weight from the list, second input is a valid weight (70 kg) as the code reprompts the user

            #tracks which messages are printed by the function/ whether there is an error if the input is invalid
            #should result in "Please enter a valid weight between 1 and 300 kg." or "Invalid input. Please enter a number." first and the calculated dosage for 70kg the second time
            with patch('builtins.print') as mock_print:
                calculate_max_dosage(allowed_anaesthesia)

                #the error message is added to the call_args_list, then the valid output is added to the list, e.g. "-50" as input:
                #call(("Please enter a valid weight between 1 and 300 kg.",), {})
                #call(("Maximum allowable dosage:",), {})
                #call(("- Ultracain D-S 1:200,000: x mg (~ x ml)",), {})

                #checks if "Please enter" (which is included in both error messages) is in the first argument of each print() call (= call[0][0]),
                #the calls with "Maximum allowable dosage" and the Ultracain dosage will therefore be excluded, only the error message remains

                errors = [call for call in mock_print.call_args_list if "Please enter" in call[0][0]]
                assert len(errors) > 0 # checks if error message was printed

def test_valid_weight(): # tests if calculate_max_dosage accepts valid weight inputs, doesn't result in an error message/ rempromt
    valid_inputs =[
        "50", #actually valid
        "100",
        "1", #corner cases
        "300"
    ]

    allowed_anaesthesia = ["Ultracain D-S 1:200,000"]

    for valid_weight in valid_inputs:
        with patch('builtins.input', side_effect=[valid_weight]):

            #tracks which messages are printed by the function/ whether there is an error
            #should result in "Please enter a valid weight between 1 and 300 kg." or "Invalid input. Please enter a number." first and the calculated dosage for 70kg the second time
            with patch('builtins.print') as mock_print:
                calculate_max_dosage(allowed_anaesthesia)

                #checks if "Please enter" (which is included in both error messages) is printed
                errors = [call for call in mock_print.call_args_list if "Please enter" in call[0][0]]
                assert len(errors) == 0 # checks that no error message was printed
