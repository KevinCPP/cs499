# About
This program aims to interpret data from batches of poorly formatted emails. Some sample emails with generic information are provided in the `messages/` and `converted_messages/` directories which will be used for the purposes of discussion.
It includes two features:
1. **preprocessing:** approximately censors information from emails that could be potentially sensitive. The development of this program was a collaborative effort between the developers and the customer who is an optometris. This feature was meant to assist the customer in quickly censoring sensitive information from real patient emails to provide us with more samples, without having to manually censor them all.
2. **analysis:** attempts to divide emails text into individual patients, extract visual acuity data about the left and right eye, extract the patient's age, then generate a graph using `matplotlib` which shows a separate line for each eye correlated against the age.

The structure of the project is as follows:
1. `main.py` is the entrypoint of the application.
2. `ui/` is where all code files related to the user interface of the application are stored. This primarily includes the code for the main menu as well as a UI element factory. Relatively straightforward to modify.
3. `parser/` contains the files which are related to the actual functionality of the program. Most importantly, these include `parser.py` which relates to the analysis feature, and `preprocessor.py` which relates to the preprocessing/censoring feature.
4. `messages/` and `converted_messages/` contain sample emails that are used in preprocessing and analysis respectively

# Setup
To run this code, `python3` is required as well as a few libraries, including:
1. matplotlib
2. pandas
3. PySide6

Installation of python 3 will be completed using your package manager, and the libraries may be installed via pip or via your package manager depending on your python installation details
Upon installing all of the requirements, simply execute `python3 main.py` while in the project's root directory to execute the program.

# Test Cases
To ensure that things are working properly with the preprocessing feature, follow the setup instructions, click the "browse" button, navigate to the `messages/` directory, and select a subset or all of the emails. Confirm your selection, then navigate back to the main menu and click the "Parse" button. Upon doing this, the messages directory will be populated with copies of the emails with censored information. Any emails with a .WARN or .ERROR extension means that the program was probably unable to censor all of the information contained within.
To run a test case on the analysis feature, follow the setup instructions, click the "Browse" button, navigate to the `converted_messages/` directory, and select a subset or all of the emails. Confirm your selection, then navigate back to the main menu and click the "Make Graph" button. Upon doing this, a graph will be displayed that is populated with visual accuity data vs. age; The spikes correspond to incidents that may have occurred which caused patients to have poor eyesight outside of natural deterioration from aging.

Notes:
1. If the `messages/` directory is already populated with emails that have the `.censored` extension, remove these files and perform the test case instructions again to generate new censored emails.
2. Due to the unpredictable nature of the emails, the preprocessing and analysis features are not perfect. Not everything will be censored all the time, and a `.WARN` or `.ERROR` extension isn't *always* included when the program fails. Similarly to a compiler for a compiled programming language, it can catch many instances where the parsing of the email may have failed based off of context clues, however, there are also many which likely slip through the cracks. As for the analysis feature, it *does not* parse data for every patient in every selected email. It has a rigid set of rules which will match a subset of the patients, who have the data which we're trying to plot and where it is formatted in a common way. However, on a large enough sample size, this data can be extrapolated out to give insights into the set of patients as a whole.

