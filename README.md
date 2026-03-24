# 2024114001

## GitHub Repository
GitHub repo link: (https://github.com/shaurya-kochar/2024114001.git)

## OneDrive Submission
OneDrive link: https://drive.google.com/file/d/10qxWZsbBYeOC9Ew_MsgO8VKxg9c3Uq9Z/view?usp=sharing

---

# How To Run Code

## Integration (Street Race Manager)
cd integration/code  
python3 main.py  

## Whitebox (MoneyPoly)
cd whitebox/code/moneypoly  
python3 main.py  

---

# How To Run Tests

## Integration Tests
cd integration  
python3 -m pytest tests -q  

## Whitebox Tests
cd whitebox/tests  
python3 -m pytest whitebox_tests.py -q  

## Blackbox API Tests
cd blackbox  
python3 -m pytest tests -q  

---

# Notes

- Ensure Python 3 is installed  
- Install dependencies if needed:
  pip install pytest requests  

- All tests are designed to run independently  
- Integration tests use GameManager as central controller  
- Blackbox tests require API connectivity  

---