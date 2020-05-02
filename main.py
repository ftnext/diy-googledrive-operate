import argparse

from operate_drive import create_diy_gdrive


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_id")
    args = parser.parse_args()

    dest_title_prefix = "copied"
    dest_file_url = cp_in_drive(args.source_id, dest_title_prefix)
    print(f"コピーされました: {dest_file_url}")


def cp_in_drive(source_id, dest_title_prefix):
    """Copy a file in Google Drive and return the URL.

    prefix `dest_title_prefix` to a title of source file
    """
    drive = create_diy_gdrive()
    source_file = drive.fetch_file_by_id(source_id)
    dest_title = f"{dest_title_prefix}_{source_file.fetch_title()}"
    dest_file = drive.copy_file(source_file, dest_title)
    return dest_file.fetch_url()


if __name__ == "__main__":
    main()
