# Trust Listing Processing Tools

This repository provides open-source tools for processing and analyzing Clio trust listing reports. It includes:
- A **Command Line Trust Ranking Tool** for processing CSV reports.
- A **Streamlit Trust Account Activity Analyzer** for interactive data exploration.

## Features
- Data cleaning and balance formatting.
- Calculation of days since last activity.
- Generation of sorted and grouped reports.
- Interactive CSV upload and download via Streamlit.

## Installation
1. Install [Python 3](https://www.python.org/downloads/).
2. Clone the repository:
   ```
   git clone https://github.com/yourusername/repository-name.git
   ```
3. Install dependencies:
   ```
   pip install pandas streamlit
   ```
  

## Usage

### Command Line Trust Ranking Tool
Run the script from the repository root:
```
python "Clio/Aged Trust/Working Code/Rank trust listing by age.py"
```

### Streamlit Trust Account Activity Analyzer
Launch the interactive dashboard with:
```
streamlit run "Clio/Aged Trust/Streamlit/2025-03-21 Aged_trust.py"
```

## Repository Structure
- `Clio/Aged Trust/Working Code/`: Contains the command line processing script.
- `Clio/Aged Trust/Streamlit/`: Contains the Streamlit application.
- `README.md`: This documentation file.

## License
This project is open-source under the MIT License. See the [LICENSE](LICENSE) file for details.