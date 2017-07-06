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
        - Add a way to display uncertainties
    - A complete restructure of the way data is held.
        - Will need to change the file read in/out of a save file so that uncertainty data can be saved.
        - Will need to change file export to include uncertainty data and calculations

Completed changes:
    - Info page
        to add a distribution type to hazard recurrence and hazard magnitude
    - Analysis Uncertainties as a page
    - Some restructuring of both export types for both with and without uncertainties
    - Data saving restructured
    - Analysis Information Page to give user more control over how they want to view and use their analysis
    - Additional Uncertainty Pages:
        - Benefits Uncertainties
        - Cost Uncertainties
        - Externalities Uncertainties
        - Non-Disaster Benefits Uncertainties
    - Externalities does calculations

The approach is as follows:
    - For each page:
        - Add page
        - File save
        - Calculations
        - Change Analysis page
        - Export
