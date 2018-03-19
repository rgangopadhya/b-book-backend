from storages.backends.s3boto3 import S3Boto3Storage


class SceneStorage(S3Boto3Storage):
    location = 'scenes'
    file_overwrite = True


class SceneRecordingStorage(S3Boto3Storage):
    location = 'scene_recordings'
    file_overwrite = False
