import zipfile
import hashlib
import os
import requests
import uuid
import json
import time

url = 'https://t-openapi.vistel.cn/api/hub/json'
# url = 'http://localhost:8080/api/hub/json'
# url = 'http://localhost/api/hub/json'
# url = 'http://t-eye.vistel.cn/api/hub/json'
# pic_path = './正常 (2).jpeg'
zip_path = 'C:\\work\\test_hub.zip'
json_path = 'dcm.json'
mac = 'b0416f0347ce'
# mac = 'zxm-test'
_patient_no = '15801662127'
_patient_sex = 'F'
_patient_name = '飞鱼'
# _image_dir = 'C:\\Users\\gao\\Desktop\\Visumall 20190220 上海眼镜展数据\\多病种\\'
# _image_dir = 'C:\\Users\\gao\\Desktop\\Visumall 20190220 上海眼镜展数据\\DR\\'
# _image_dir = 'C:\\Users\\gao\\Desktop\\Visumall 20190220 上海眼镜展数据\\各种病\\视乳头视神经星状体\\'
# _image_dir = 'C:\\Users\\gao\\Desktop\\Visumall 20190220 上海眼镜展数据\\多病种20190604\\豹纹\\可见\\'
_image_dir = 'C:\\Users\\gao\\Desktop\\Visumall 20190220 上海眼镜展数据\\20190627\\'

def generate_json_file(study_date, batch=str(uuid.uuid4())):
    data = {
        "SpecificCharacterSet": "GB18030",
        "ProtocolName": "Color",
        "InstanceNumber": "3",
        "DeviceUID": mac,
        "PerformingPhysicianName": "Administrator",
        "SeriesInstanceUID": "1.2.392.200046.100.3.8.0.10.20171012143712.1",
        "ImageType": "ORIGINAL",
        "SeriesDescription": "Color/R",
        "InstitutionalDepartmentName": "测试",
        "BitsAllocated": "8",
        "ContentDate": "20171012",
        "Manufacturer": "Canon Inc.",
        "Laterality": "R",
        "SOPInstanceUID": "1.2.392.200046.100.3.8.0.10.20171012143712.1.1.3.1",
        "SOPClassUID": "1.2.840.10008.5.1.4.1.1.77.1.4",
        "SoftwareVersions": "4.0.0.12",
        "HighBit": "7",
        "StudyDate": study_date,
        "AcquisitionNumber": "1",
        "PatientName": _patient_name,
        "PatientAge": "037Y",
        "StudyID": "10",
        "PatientSex": _patient_sex,
        "PatientID": _patient_no,
        "OperatorsName": "Administrator",
        "AccessionNumber": "88888888",
        "Modality": "OP",
        "AcquisitionContextSequence": None,
        "PatientBirthDate": "19410101",
        "SamplesPerPixel": "3",
        "BitsStored": "8",
        "StudyInstanceUID": batch,
        "PixelRepresentation": "0",
        "DeviceSerialNumber": "000000",
        "LossyImageCompression": None,
        "PlanarConfiguration": "0",
        "PhotometricInterpretation": "RGB",
        "PatientOrientation": "L",
        "SeriesNumber": "1",
        "SeriesTime": "143711",
        "Rows": "3168",
        "InstitutionName": "测试",
        "ManufacturerModelName": "CR-2",
        "ImageComments": "Timer:0.0/Field Angle:45/Ref-ERR Comp. Lens:U/Flash Intensity:/Flash Intensity Compensation:/Flash Observation:/SP:OTHER/Image Comment:",
        "Columns": "4752",
        "StudyTime": "143706",
        "ContentTime": "143714",
        "ReferringPhysicianName": None
    }
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def get_file_md5_str(path):
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def generate_request_json(pic_name, json, md5_str):
    return [{
        "macAddress": mac,
        "fileName": pic_name,
        "jsonName": os.path.basename(json),
        "fileType": "0",
        "md5": md5_str
    }]


if __name__ == '__main__':
    generate_json_file(time.strftime("%Y-%m-%d"))
    for f in os.listdir(_image_dir):
        if (f.endswith('.jpg') or f.endswith('.jpeg')):
            pic_path = _image_dir + f
            if os.path.exists(zip_path):
                os.remove(zip_path)
            name, extension = os.path.splitext(pic_path)
            new_pic_name = str(uuid.uuid4()) + extension
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(pic_path, new_pic_name)
                zipf.write(json_path)
            request_json = generate_request_json(new_pic_name, json_path, get_file_md5_str(zip_path))
            result = requests.post(url, data={'json': str(request_json)}, files={'pic': open(zip_path, 'rb')})
            print(result)
