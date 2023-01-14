# Label Chopper

![Label Chopper](https://mrdavidoneill.com/images/labelchopper001.png)
![Label Chopper](https://mrdavidoneill.com/images/labelchopper002.png)

Convert Amazon & FBA labels to a format suitable for thermal labels printers

## Instructions how to run

Note: This was built for Python 2.7, as upgrading to Python 3 on the client's shared server used for the prototype was not possible. However, for production, upgrading to the latest Python version is recommended.

### Install miniconda

```powershell
conda install
```

### Create virtual environment

```powershell
conda create --name labelchopper python=2.7
```

### Activate virtual environment

```powershell
conda activate labelchopper
```

### Install from requirements.tx

```powershell
pip install -r requirements.txt
```

### Run program

```powershell
python labelizer.py
```
