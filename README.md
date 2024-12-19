## How to set up

1. Clone the repository:
   ```bash
   git clone https://github.com/codemdvd/ra_assignment_2.git
   cd ra_assignment_2

```
python -m venv .venv
```
### using venv
Windows
```
.venv/Scripts/Activate
```
Linux
```
source .venv/bin/activate
```
### installing requirments
```
pip install -r requirments.txt
```
## How to run algorithms

to run each algorithm: python run {name_of_the_agoritm}.py

For example, how to run HLL:
```
python HLL.py
```
inside each alorithm code you can chose the dataset changing this lines of code:
```
    crusoe_text_file = "datasets/war-peace.txt"
    crusoe_data_file = "datasets/war-peace.dat"
```
## How to generate datasets
In the directory you can find data_generator.py. To run it just chose parametrs n, N and alpha and run it using:
```
python data_generator.py
```
