# About My Project

Student Name:  Philip Cheuk 
Student Email:  pcheuk@syr.edu

### What it does
This project analyzes Washington State's electric vehicle population data through an interactive dashboard. It features:

Data pipeline that cleans and processes raw EV registration data

Geographic visualization of vehicle locations

Market share analysis of different manufacturers

Historical trends in EV adoption and battery range improvements

Interactive filters for state, year range, and manufacturers

Automated tests for data transformation logic

Built with Python using Streamlit for the UI, Pandas for data processing, and Plotly for visualizations.

### How you run my project
1. Install dependencies: pip install -r requirements.txt
2. Process data: data_processing.py
3. Launch dashboard: streamlit run code_app.py
4. (Optional) Run tests: pytest tests

### Other things you need to know
1. First run will create a cache/ folder with processed data
2. Test coverage focuses on data cleaning transformations