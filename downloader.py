import zipfile
import os

def zip_folder(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

if __name__ == '__main__':
    # 指定要壓縮的資料夾路徑和輸出的 zip 檔案名稱
    folder_to_zip = './img'
    output_zip_file = 'img.zip'

    # 執行壓縮
    zip_folder(folder_to_zip, output_zip_file)
