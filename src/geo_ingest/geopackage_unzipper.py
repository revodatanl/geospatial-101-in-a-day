import os
import zipfile
from typing import List


class GeoPackageUnzipper:
    """
    Unzips selected .zip files from an Azure Blob Storage container,
    extracts .gpkg files, and uploads them to another directory in the container.
    Skips files if the corresponding .gpkg already exists in the output directory.
    """

    def __init__(
        self,
        dbutils,
        storage_account_name: str,
        container_name: str,
        input_dir: str,
        output_dir: str,
        local_tmp_dir: str = "/tmp/unzip_cache",
    ):
        self.dbutils = dbutils
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.input_dir = input_dir.strip('/')
        self.output_dir = output_dir.strip('/')
        self.local_tmp_dir = local_tmp_dir

        os.makedirs(self.local_tmp_dir, exist_ok=True)

    def _get_abfss_path(self, dir_name: str, file_name: str = "") -> str:
        return f"abfss://{self.container_name}@{self.storage_account_name}.dfs.core.windows.net/{dir_name}/{file_name}".rstrip('/')

    def unzip_selected_and_upload(self, zip_filenames: List[str]) -> None:
        input_path = self._get_abfss_path(self.input_dir)
        output_path = self._get_abfss_path(self.output_dir)

        for zip_filename in zip_filenames:
            expected_gpkg_name = zip_filename.replace(".zip", ".gpkg")
            remote_gpkg_path = f"{output_path}/{expected_gpkg_name}"

            # Check if the .gpkg file already exists
            try:
                existing_files = self.dbutils.fs.ls(output_path)
                existing_gpkg_files = [f.name for f in existing_files if f.name.endswith(".gpkg")]
                if expected_gpkg_name in existing_gpkg_files:
                    print(f"[INFO] Skipping {zip_filename}, GPKG already exists.")
                    continue
            except Exception as e:
                print(f"[WARNING] Could not check for existing files in {output_path}: {e}")

            full_zip_path = f"{input_path}/{zip_filename}"
            local_zip_path = os.path.join(self.local_tmp_dir, zip_filename)

            print(f"[INFO] Downloading: {full_zip_path}")
            try:
                self.dbutils.fs.cp(full_zip_path, f"file:{local_zip_path}")
            except Exception as e:
                print(f"[ERROR] Failed to download {zip_filename}: {e}")
                continue

            # Extract locally
            try:
                with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(self.local_tmp_dir)
                print(f"[INFO] Unzipped: {zip_filename}")
            except Exception as e:
                print(f"[ERROR] Failed to unzip {zip_filename}: {e}")
                continue

            # Upload all .gpkg files found
            try:
                for root, _, files in os.walk(self.local_tmp_dir):
                    for extracted_file in files:
                        if extracted_file.endswith(".gpkg"):
                            local_file_path = os.path.join(root, extracted_file)
                            remote_file_path = f"{output_path}/{extracted_file}"
                            print(f"[INFO] Uploading GPKG: {remote_file_path}")
                            try:
                                self.dbutils.fs.cp(f"file:{local_file_path}", remote_file_path)
                            except Exception as e:
                                print(f"[ERROR] Failed to upload {extracted_file}: {e}")
            except Exception as e:
                print(f"[ERROR] Problem during file scanning/upload: {e}")

            # Clean up the temp directory
            try:
                print(f"[INFO] Cleaning up temp directory: {self.local_tmp_dir}")
                self.dbutils.fs.rm(f"file:{self.local_tmp_dir}", recurse=True)
                os.makedirs(self.local_tmp_dir, exist_ok=True)
            except Exception as e:
                print(f"[ERROR] Failed to clean temp dir: {e}")