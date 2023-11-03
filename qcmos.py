pixel_size = 4.6
conversion_factor = 0.107

quantum_efficiency = 0.56
offset = 200

def grayscale_value_to_photon_number(grayscale_value):
    return (grayscale_value - offset) * conversion_factor / quantum_efficiency

