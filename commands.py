from database_utils import add_photos, add_audio, check_status, clear_photos, change_name, ignor

commands = {
    "!photo": add_photos,
    "!audio": add_audio,
    "!status": check_status,
    "!clear": clear_photos,
    "!name": change_name,
    "!ignor": ignor,

    "!фото": add_photos,
    "!аудио": add_audio,
    "!статус": check_status,
    "!оч": clear_photos,
    "!имя": change_name,
    "!игнор": ignor
}
