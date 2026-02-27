import exifread
import os

def read_exif(image_path: str) -> dict:
    """
    Takes a local image file path.
    Reads all EXIF metadata hidden inside the image.
    Returns a clean dict with the most important fields.
    Returns empty dict if no metadata found.
    """
    try:
        if not os.path.exists(image_path):
            print("Image file not found")
            return {}

        with open(image_path, "rb") as f:
            tags = exifread.process_file(f, stop_tag="UNDEF", details=False)

        if not tags:
            print("No EXIF data found in image")
            return {}

        # Extract the most useful fields
        result = {}

        # Date the photo was originally taken
        date_taken = tags.get("EXIF DateTimeOriginal") or tags.get("Image DateTime")
        if date_taken:
            result["date_taken"] = str(date_taken)

        # Camera or device used
        camera_make  = tags.get("Image Make")
        camera_model = tags.get("Image Model")
        if camera_make:
            result["camera_make"] = str(camera_make)
        if camera_model:
            result["camera_model"] = str(camera_model)

        # Software used to edit
        software = tags.get("Image Software")
        if software:
            result["software"] = str(software)

        # GPS location
        gps_lat  = tags.get("GPS GPSLatitude")
        gps_long = tags.get("GPS GPSLongitude")
        if gps_lat:
            result["gps_latitude"]  = str(gps_lat)
        if gps_long:
            result["gps_longitude"] = str(gps_long)

        # Image dimensions
        width  = tags.get("EXIF ExifImageWidth")  or tags.get("Image ImageWidth")
        height = tags.get("EXIF ExifImageLength") or tags.get("Image ImageLength")
        if width:
            result["width"]  = str(width)
        if height:
            result["height"] = str(height)

        print(f"EXIF data extracted: {list(result.keys())}")
        return result

    except Exception as e:
        print(f"EXIF reading error: {e}")
        return {}