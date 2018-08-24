import pydicom
import numpy

from ctvector3 import CTVector3

class CTSlice:
    def __init__(self, dicom_data : pydicom.dataset.FileDataset):

        image_position : pydicom.multival.MultiValue = dicom_data.ImagePositionPatient

        self.position = CTVector3(image_position[0], image_position[1], image_position[2])
        
        self.pixel_array = dicom_data.pixel_array # The value of each pixel is using bone color map

        return