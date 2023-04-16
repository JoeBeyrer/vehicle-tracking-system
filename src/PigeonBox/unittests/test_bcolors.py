import pytest
from unittest import *
from PigeonBox.bcolors import *

def test_PrintFormat(mocker):
    # Create a mock object for the print function
    mock_print = mocker.patch('builtins.print')
    
    # Call the function with each color status and some text
    PrintFormat("Invalid", "Error: something went wrong")
    PrintFormat("Success", "Task completed successfully")
    PrintFormat("Action", "Performing important action...")
    PrintFormat("Important", "Please read carefully")
    PrintFormat("Warning", "Warning: this action cannot be undone")
    PrintFormat("Purple", "This text is purple")
    PrintFormat("Cyan", "This text is cyan")
    
    # Check that the mock print function was called with the expected arguments for each call
    mock_print.assert_has_calls([
        mocker.call(f"{bcolors.FAIL}Error: something went wrong{bcolors.ENDC}"),
        mocker.call(f"{bcolors.OKGREEN}Task completed successfully{bcolors.ENDC}"),
        mocker.call(f"{bcolors.OKBLUE}Performing important action...{bcolors.ENDC}"),
        mocker.call(f"{bcolors.BOLD}Please read carefully{bcolors.ENDC}"),
        mocker.call(f"{bcolors.WARNING}Warning: this action cannot be undone{bcolors.ENDC}"),
        mocker.call(f"{bcolors.HEADER}This text is purple{bcolors.ENDC}"),
        mocker.call(f"{bcolors.HEADER}This text is cyan{bcolors.ENDC}")
    ])

def test_bcolors(): #not really needed, super straight forward. Included just in case
    assert bcolors.HEADER == '\033[95m'
    assert bcolors.OKBLUE == '\033[94m'
    assert bcolors.OKCYAN == '\033[96m'
    assert bcolors.OKGREEN == '\033[92m'
    assert bcolors.WARNING == '\033[93m'
    assert bcolors.FAIL == '\033[91m'
    assert bcolors.ENDC == '\033[0m'
    assert bcolors.BOLD == '\033[1m'
    assert bcolors.UNDERLINE == '\033[4m'
