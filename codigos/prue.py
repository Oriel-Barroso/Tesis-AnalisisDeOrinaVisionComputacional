import cv2
import numpy as np
import colour

def calculate_delta_eitp(image1, image2):
    size = (min(image1.shape[1], image2.shape[1]), min(image1.shape[0], image2.shape[0]))
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)

    xyz1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    xyz2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

    # xyz1 = cv2.cvtColor(image1, cv2.COLOR_BGR2XYZ)
    # xyz2 = cv2.cvtColor(image2, cv2.COLOR_BGR2XYZ)

    # Convert CIE XYZ to ICTCP
    ictcp1 = colour.models.rgb.RGB_to_ICtCp(xyz1/100)
    ictcp2 = colour.models.rgb.RGB_to_ICtCp(xyz2/100)
    
    # ictcp1 = colour.models.rgb.XYZ_to_ICtCp(xyz1/100)
    # ictcp2 = colour.models.rgb.XYZ_to_ICtCp(xyz2/100)

    # Calculate color difference using Delta E ITP formula
    #delta_eitp = 720 * np.sqrt((ictcp1. - ictcp2.J)**2 + 0.25*(ictcp1.T - ictcp2.T)**2 + (ictcp1.P - ictcp2.P)**2)
    s = colour.difference.delta_E_ITP(ictcp1, ictcp2)
    d = colour.difference.power_function_Huang2015(s)
    avg_delta_eitp1 = np.mean(d)
    avg_delta_eitp2 = np.mean(s)

    return avg_delta_eitp1, avg_delta_eitp2 


# Load two images to compare
image1 = cv2.imread("./crop/1.jpg")
image2 = cv2.imread("./colores/1/bil3.jpeg")
print('bil3')
# Calculate Delta E ITP between the two images
delta_eitp = calculate_delta_eitp(image1, image2)



# Print the result
print(f"Delta E ITP: {delta_eitp}")
