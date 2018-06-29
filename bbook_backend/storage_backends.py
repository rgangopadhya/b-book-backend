from storages.backends.s3boto3 import S3Boto3Storage


class StoryTitleStorage(S3Boto3Storage):
    location = 'story_titles'
    file_overwrite = False


class SceneStorage(S3Boto3Storage):
    location = 'scenes'
    file_overwrite = True


class SceneRecordingStorage(S3Boto3Storage):
    location = 'scene_recordings'
    file_overwrite = False


class StoryStorage(S3Boto3Storage):
    location = 'story'
    file_overwrite = False
