# DWDM Table Generator

This Python script generates a Dense Wavelength Division Multiplexing (DWDM) table and provides utilities for frequency and wavelength conversions based on the ITU grid. It supports custom configurations, including center frequency, slice width, and granularity.

## Features

- Generate a DWDM table with `n`, frequency, wavelength, and ITU channel mappings.
- Convert `n` to frequency and `m` to bandwidth.
- Convert frequency to `n` and width to `m`.
- Mark frequencies with their corresponding ITU channel (if available).
- Save results to a CSV file.

## Requirements

- Python 3.6 or later

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/devfilipe/wdm.git
   ```
2. Navigate to the project directory:
   ```bash
   cd wdm
   ```

## Usage

### Command-line Arguments

The script provides several command-line options:

| Argument                  | Description                                                                                       |
|---------------------------|---------------------------------------------------------------------------------------------------|
| `--generate-table`        | Generate the DWDM table and save it to a CSV file.                                               |
| `--center-freq`           | Center frequency in THz (default: 193.1).                                                        |
| `--min-freq`              | Minimum frequency in THz (default: 191.150).                                                     |
| `--max-freq`              | Maximum frequency in THz (default: 196.300).                                                     |
| `--slice-width`           | Slice width in GHz (default: 6.25 GHz).                                                          |
| `--granularity`           | Granularity in GHz (default: 12.5 GHz).                                                          |
| `--to-freq-width`         | Convert `n` to frequency and `m` to width.                                                       |
| `--to-n-m`                | Convert frequency to `n` and width to `m`.                                                       |
| `--output-file`           | Output file name (default: `output.csv`).                                                        |

### Examples

#### Generate a DWDM Table
To generate a DWDM table and save it as `output.csv`:
```bash
python wdm.py --generate-table --output-file output.csv
```

#### Convert `n` to Frequency and `m` to Width
To calculate frequency and bandwidth for a given `n` and `m`:
```bash
python wdm.py --to-freq-width 10 4
```

#### Convert Frequency to `n` and Width to `m`
To calculate `n` and `m` from a frequency and width:
```bash
python wdm.py --to-n-m 193.1 50
```

## Output Format

The generated CSV file contains the following columns:
- **n**: Index relative to the center frequency.
- **Frequency (GHz)**: Frequency in GHz.
- **Wavelength (nm)**: Wavelength in nanometers.
- **m=1 to m=12**: Frequency ranges based on `m` values.
- **ITU Channel**: ITU channel name or `N/A` if no match is found.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

