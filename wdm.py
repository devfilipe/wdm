import argparse
import csv

# Channel table (H and C)
channel_table = {
    "H11": 191.150,
    "C12": 191.200,
    "H12": 191.250,
    "C13": 191.300,
    "H13": 191.350,
    "C14": 191.400,
    "H14": 191.450,
    "C15": 191.500,
    "H15": 191.550,
    "C16": 191.600,
    "H16": 191.650,
    "C17": 191.700,
    "H17": 191.750,
    "C18": 191.800,
    "H18": 191.850,
    "C19": 191.900,
    "H19": 191.950,
    "C20": 192.000,
    "H20": 192.050,
    "C21": 192.100,
    "H21": 192.150,
    "C22": 192.200,
    "H22": 192.250,
    "C23": 192.300,
    "H23": 192.350,
    "C24": 192.400,
    "H24": 192.450,
    "C25": 192.500,
    "H25": 192.550,
    "C26": 192.600,
    "H26": 192.650,
    "C27": 192.700,
    "H27": 192.750,
    "C28": 192.800,
    "H28": 192.850,
    "C29": 192.900,
    "H29": 192.950,
    "C30": 193.000,
    "H30": 193.050,
    "C31": 193.100,
    "H31": 193.150,
    "C32": 193.200,
    "H32": 193.250,
    "C33": 193.300,
    "H33": 193.350,
    "C34": 193.400,
    "H34": 193.450,
    "C35": 193.500,
    "H35": 193.550,
    "C36": 193.600,
    "H36": 193.650,
    "C37": 193.700,
    "H37": 193.750,
    "C38": 193.800,
    "H38": 193.850,
    "C39": 193.900,
    "H39": 193.950,
    "C40": 194.000,
    "H40": 194.050,
    "C41": 194.100,
    "H41": 194.150,
    "C42": 194.200,
    "H42": 194.250,
    "C43": 194.300,
    "H43": 194.350,
    "C44": 194.400,
    "H44": 194.450,
    "C45": 194.500,
    "H45": 194.550,
    "C46": 194.600,
    "H46": 194.650,
    "C47": 194.700,
    "H47": 194.750,
    "C48": 194.800,
    "H48": 194.850,
    "C49": 194.900,
    "H49": 194.950,
    "C50": 195.000,
    "H50": 195.050,
    "C51": 195.100,
    "H51": 195.150,
    "C52": 195.200,
    "H52": 195.250,
    "C53": 195.300,
    "H53": 195.350,
    "C54": 195.400,
    "H54": 195.450,
    "C55": 195.500,
    "H55": 195.550,
    "C56": 195.600,
    "H56": 195.650,
    "C57": 195.700,
    "H57": 195.750,
    "C58": 195.800,
    "H58": 195.850,
    "C59": 195.900,
    "H59": 195.950,
    "C60": 196.000,
    "H60": 196.050,
    "C61": 196.100,
    "H61": 196.150,
    "C62": 196.200,
    "H62": 196.250,
    "C63": 196.300,
}


def generate_frequencies(center_freq=193.1, min_freq=191.150, max_freq=196.300, granularity=12.5):
    frequencies = []

    # Generate frequencies for n < 0 (below center_freq)
    slice_width = granularity / 1000 / 2
    n = -1
    f = center_freq + (n * slice_width)
    while f >= min_freq:
        frequency = round(f, 8)
        frequencies.append((n, frequency))
        n -= 1
        f = center_freq + (n * slice_width)

    # Reverse negative n
    frequencies.reverse()

    # Add the central frequency (n=0)
    frequencies.append((0, center_freq))

    # Generate frequencies for n > 0 (above center_freq)
    n = 1
    f = center_freq + (n * slice_width)
    while f <= max_freq:
        frequency = round(f, 8)
        frequencies.append((n, frequency))
        n += 1
        f = center_freq + (n * slice_width)
    return frequencies


# Mark frequencies with ITU channels
def mark_channels(frequencies):
    marked_frequencies = []
    for n, freq in frequencies:  # Frequencies is now a list of (n, frequency) pairs
        closest_channel = None
        for channel, channel_freq in channel_table.items():
            # if abs(freq - channel_freq) < 0.025:  # Tolerance of 25 MHz
            if freq == channel_freq:  # exact match
                closest_channel = channel
                break
        marked_frequencies.append((n, freq, closest_channel if closest_channel else "N/A"))
    return marked_frequencies


# Convert frequency in THz to wavelength in nanometers
def frequency_to_wavelength(frequency):
    c = 299_792_458  # speed of light in m/s
    return (c / (frequency * 1e12)) * 1e9  # nm


# Generate the DWDM table with n, frequency, wavelength, and m columns
def generate_dwdm_table(center_freq, min_freq, max_freq, granularity, output_file):
    frequencies = generate_frequencies(center_freq, min_freq, max_freq, granularity)
    marked_frequencies = mark_channels(frequencies)

    # Open output CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "n",
                "Frequency (GHz)",
                "Wavelength (nm)",
                "m=1 (12.5GHz)",
                "m=2 (25GHz)",
                "m=3 (37.5GHz)",
                "m=4 (50GHz)",
                "m=8 (100GHz)",
                "m=12 (150GHz)",
                "ITU Channel",
            ]
        )

        # Write rows for each frequency
        for n, freq, channel in marked_frequencies:
            wavelength = frequency_to_wavelength(freq)

            # Add m columns based on frequency step sizes
            m_columns = []
            for m in range(1, 13):  # m=1 to m=12
                width = granularity / 1000 * m  # Width for current m
                minf = freq - (width / 2)  # Frequency range start
                maxf = freq + (width / 2)  # Frequency range end
                m_columns.append(f"{minf:.5f} - {maxf:.5f}")  # Format m values to 3 decimal places

            writer.writerow([n, f"{freq:.5f}", f"{wavelength:.3f}", *m_columns, channel])

    print(f"DWDM table generated and saved to {output_file}")


def convert_n_to_freq(n, granularity=12.5, center_freq=193.1):
    """Converts n to frequency (in THz)."""
    return center_freq + (granularity / 2 / 1000) * n


def convert_m_to_width(m, granularity=12.5):
    """Converts m to width (in GHz)."""
    return granularity * m


def convert_freq_to_n(freq, granularity=12.5, center_freq=193.1):
    """Converts frequency (in THz) to n."""
    return int((freq - center_freq) / (granularity / 2 / 1000))


def convert_width_to_m(width, granularity=12.5):
    """Converts width (in GHz) to m."""
    return int(width / granularity)


# Main function to parse arguments and run the program
def main():
    parser = argparse.ArgumentParser(
        description="Generate a DWDM table with n, frequency, wavelength, and ITU channels."
    )
    parser.add_argument(
        "--generate-table", action="store_true", help="Generate the DWDM table and save it to a CSV file."
    )
    parser.add_argument("--center-freq", type=float, default=193.1, help="Center frequency in THz (default: 193.1).")
    parser.add_argument("--min-freq", type=float, default=191.150, help="Minimum frequency in THz (default: 191.150).")
    parser.add_argument("--max-freq", type=float, default=196.300, help="Maximum frequency in THz (default: 196.300).")
    parser.add_argument("--slice-width", type=float, default=6.25, help="Slice width in GHz (default: 6.25GHz).")
    parser.add_argument("--granularity", type=float, default=12.5, help="Slice width in GHz (default: 12.5GHz).")
    parser.add_argument(
        "--to-freq-width", nargs=2, metavar=("n", "m"), type=int, help="Convert n to frequency and m to width."
    )
    parser.add_argument(
        "--to-n-m", nargs=2, metavar=("f", "w"), type=float, help="Convert frequency to n and width to m."
    )
    parser.add_argument("--output-file", type=str, default="output.csv", help="Output file name (default: output.csv).")

    args = parser.parse_args()

    if args.generate_table:
        generate_dwdm_table(args.center_freq, args.min_freq, args.max_freq, args.granularity, args.output_file)

    # Process --to-freq-width argument
    if args.to_freq_width:
        n, m = args.to_freq_width
        freq = convert_n_to_freq(n, granularity=args.granularity, center_freq=args.center_freq)
        width = convert_m_to_width(m, granularity=args.granularity)

        delta = width / 1000 / 2
        minfreq = freq - delta
        maxfreq = freq + delta

        print(f"Converted n={n} to frequency: {freq:.6f} THz")
        print(f"Converted m={m} to width: {width:.6f} GHz")
        print(f"Min frequency: {minfreq:.6f} THz")
        print(f"Max frequency: {maxfreq:.6f} THz")

    # Process --to-n-m argument
    if args.to_n_m:
        f, w = args.to_n_m
        n = convert_freq_to_n(f, granularity=args.granularity, center_freq=args.center_freq)
        m = convert_width_to_m(w, granularity=args.granularity)
        print(f"Converted frequency {f} THz to n: {n}")
        print(f"Converted width {w} GHz to m: {m}")


if __name__ == "__main__":
    main()
