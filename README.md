# applicator_yield
Flex Applicator Line Yield Monitor


yield_application.py is the main python file and will run the program for graphing (reading from data file) graphing.py, and the screenshot program (writing to data file) yield_calculator.py. Together these scripts allow the technicians to track manufaturing yield as a perentage of good parts made out of the total parts (including defects). This helps the technicians be able to track performance of the machines based on changes and alterations and determine if improvements need to be made or if the work done was sufficient. 

How it works:
The yield_calculatior.py script is taking a screenshot of the factory KPI every minute to grab the live production numbers. This KPI looks like what is shown in APP_KPI_example.png and APP_KPI2_example.png. The script then crops the image down to only view the number of good parts made and the number of defects which can be viewed in APP_Parts_example.png. Pytesseract (Python wrapper for Google's Tesseract-OCR enginen) is then used to convert the image containing the text into string formats that can be process further. One parsed into a usable format some math is done that compares the numbers to the previous minute and hour and then finally calculate the yield, which is then stored into a data file. This file looks like the data_example.txt. As mentioned previously, the graphing.py script is constantly reading through this file waiting for updates and once updated will graph the appended data to the line graph allowing for easy visuals and quick data analysis for the technicians. 

When running the program the user's view looks like running_example.png. 


