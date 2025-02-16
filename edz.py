import csv

def calculate_antenna_lengths(band_mhz, frequency_step=0.01, reflector_adjustment=0.05, velocity_factor=0.98):
    """
    Calculate element, matching stub, and ground reflector lengths for an extended double zepp antenna,
    adjusted for real-world conditions with 600-ohm open-wire feedline and 14 AWG wire.

    Parameters:
        band_mhz (tuple): The start and end frequencies of the band in MHz.
        frequency_step (float): The step size to iterate through frequencies in MHz.
        reflector_adjustment (float): The percentage increase for the ground reflector length.
        velocity_factor (float): The velocity factor for the 600-ohm open-wire feedline.

    Returns:
        list of dict: A list of dictionaries with the calculated antenna dimensions.
    """
    start_freq, end_freq = band_mhz
    results = []

    for freq in range(int(start_freq * 1000), int(end_freq * 1000), int(frequency_step * 1000)):
        freq_mhz = freq / 1000.0
        wavelength = 11811 / freq_mhz  # Full wavelength in inches (speed of light in air)

        # Apply velocity factor correction
        effective_wavelength = wavelength * velocity_factor

        # Calculate lengths using corrected wavelength
        element_length = (effective_wavelength * 5 / 8) / 12  # Convert inches to feet
        stub_length = (effective_wavelength * 1 / 8) / 12
        reflector_length = element_length * (1 + reflector_adjustment)

        # Calculate total lengths
        total_antenna_length = element_length * 2
        total_reflector_length = reflector_length * 2

        # Round to whole inches
        def to_feet_and_inches(total_inches):
            feet = total_inches // 12
            inches = total_inches % 12
            return feet, inches

        element_ft, element_in = to_feet_and_inches(round(element_length * 12))
        stub_ft, stub_in = to_feet_and_inches(round(stub_length * 12))
        reflector_ft, reflector_in = to_feet_and_inches(round(reflector_length * 12))
        total_antenna_ft, total_antenna_in = to_feet_and_inches(round(total_antenna_length * 12))
        total_reflector_ft, total_reflector_in = to_feet_and_inches(round(total_reflector_length * 12))

        results.append({
            "Band": f"{band_mhz[0]}-{band_mhz[1]} MHz",
            "Frequency_MHz": freq_mhz,
            "Element_Length_Ft": element_ft,
            "Element_Length_In": element_in,
            "Stub_Length_Ft": stub_ft,
            "Stub_Length_In": stub_in,
            "Reflector_Length_Ft": reflector_ft,
            "Reflector_Length_In": reflector_in,
            "Total_Antenna_Length_Ft": total_antenna_ft,
            "Total_Antenna_Length_In": total_antenna_in,
            "Total_Reflector_Length_Ft": total_reflector_ft,
            "Total_Reflector_Length_In": total_reflector_in,
        })

    return results

# Define band ranges (in MHz)
bands = {
    "160m": (1.8, 2.0),
    "80m": (3.5, 4.0),
    "40m": (7.074, 7.285),
    "20m": (14.0, 14.35),
    "15m": (21.0, 21.45),
    "10m": (28.0, 29.7),
}

# Frequency step (in MHz)
frequency_step = 0.01

# Collect results for all bands
all_results = []
for band_name, band_range in bands.items():
    band_results = calculate_antenna_lengths(band_range, frequency_step=frequency_step)
    all_results.extend(band_results)

# Save results to CSV
csv_filename = "extended_double_zepp_antenna.csv"
csv_fields = [
    "Band", "Frequency_MHz", "Element_Length_Ft", "Element_Length_In",
    "Stub_Length_Ft", "Stub_Length_In", "Reflector_Length_Ft", "Reflector_Length_In",
    "Total_Antenna_Length_Ft", "Total_Antenna_Length_In", "Total_Reflector_Length_Ft",
    "Total_Reflector_Length_In"
]

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=csv_fields)
    writer.writeheader()
    writer.writerows(all_results)

print(f"Antenna dimensions saved to {csv_filename}")
