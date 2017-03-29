# Economic-Resilience-Guide
An interface for communities to aid in working through NIST's Community Resilience Economic Decision Guide, http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1197.pdf

The uncertainty branch is dedicated to adding an element of uncertainty to the program.
Anticipated changes:
    - Info page
        to add a distribution type to hazard recurrence and hazard magnitude
    - Additional Uncertainty Pages:
        - Benefits Uncertainties
        - Externalities Uncertainties
        - Cost Uncertainties
        - Non-Disaster Benefits Uncertainties
        entire new pages to define a distribution for all costs and benefits involved
    - Analysis page
        - Add \pm to all costs and benefits where the \pm \neq 0
    - Calculations.py
        - May need to restructure how data is held to maintain order as number of variables increases.
        - Will need to change the file read in/out of a save file so that uncertainty data can be saved.
        - Will need to change file export to include uncertainty data and calculations

Completed changes:
    - Info page
        to add a distribution type to hazard recurrence and hazard magnitude
    - Additional Uncertainty Pages:
        - Benefits Uncertainties

The approach is as follows:
    - Add pages and input fields
    - File save
    - Calculations
    - Change Analysis page
    - Export