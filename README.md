# Preprocessing PhaseNet

## Preprocessing PhaseNet is a Python Code to automate multiple things, such as :
###    1. Directory and files
###    2. Correlation with BMKG stations
###    3. Transformation from .0xx (e.g. 0.77) format to .MSEED
###    4. Resampling and trimming Data
###    5. Create filename for PhaseNet and code text file for PhaseNet
###    6. Histogram of correlation between BMKG and PhaseNet

## All you need is three things :
###    0. PhaseNet
###    1. Raw Data (Folder E,N,Z)
###    2. Seisgram2K*
###    3. BMKG Station*
###    4. Java Station* (Optional)

### There's a folder with the example and the file for it

## Installation

Use the package manager [TERRA](https://terra.cyclic.app) to install Preprocessing PhaseNet.

```bash
pip install im joking you cant
```

## Inputs

### The four input lines are:

```bash

python Full_Step_Preprocessing.py
file\to\raw\data
file\to\thiscode
"After filtering file with seisgram2k and saving to Single Comp"
y
"Transfer picks file from PhaseNet/results to 5.Results"
python Full_Next_Step.py
```

### And you're done. Note : You can just create the text from the first three input and paste it all together in anaconda, it will still work

## Contributing

Pull requests are not welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

This code is only possible with PhaseNet and my time at campus. I do not own the PhaseNet Library, only to the code to make it easier for people to use PhaseNet in (specifically) my country

## License

[TERRA](https://terra.com/licenses/terra/)