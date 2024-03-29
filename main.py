import argparse
from typing import Optional

from operate_drive import create_diy_gdrive
from operate_drive.drive import DiyGoogleDrive
from operate_drive.file import DiyGDriveFile


def main():
    args = parse_args()

    dest_file = cp_in_drive(
        args.source_id, args.dest_title, args.parent_dir_id
    )

    info = display_information(dest_file)
    print(info)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_id")
    parser.add_argument("--dest_title")
    parser.add_argument("--parent_dir_id")
    return parser.parse_args()


def cp_in_drive(
    source_id: str,
    dest_title: Optional[str] = None,
    parent_dir_id: Optional[str] = None,
) -> DiyGDriveFile:
    """Copy a specified file in Google Drive and return the created file."""
    drive = create_diy_gdrive()
    if dest_title is None:
        dest_title = build_dest_title(drive, source_id)
    return drive.copy_file(source_id, dest_title, parent_dir_id)


def build_dest_title(drive: DiyGoogleDrive, source_id: str) -> str:
    source = drive.fetch_file_by_id(source_id)
    source_title = source.fetch_title()
    return title_of_copy_dest(source_title)


def title_of_copy_dest(source_title: str) -> str:
    # 暫定的に、元のファイル名にcopied_をつけるものとする
    return f"copied_{source_title}"


def display_information(gdrive_file: DiyGDriveFile) -> str:
    """Create information to show in command line."""
    url = gdrive_file.fetch_url()
    return f"コピーされました: {url}"


if __name__ == "__main__":
    main()
