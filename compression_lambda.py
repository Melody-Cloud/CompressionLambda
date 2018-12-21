import boto3
import subprocess
import os


def strip_extension(path):
    return os.path.splitext(path)[0]


def lambda_handler(event, context):
    first_record = event["Records"][0]
    name_of_audio_file_on_s3bucket = str(first_record['s3']['object']['key'])

    name_of_bucket_with_songs = os.environ['name_of_bucket_with_songs']
    name_of_bucket_with_output = os.environ['name_of_bucket_with_output']

    s3 = boto3.resource('s3')
    s3.Bucket(name_of_bucket_with_songs).download_file(
        name_of_audio_file_on_s3bucket, '/tmp/{0}'.format(name_of_audio_file_on_s3bucket))

    subprocess.call(['cp /var/task/ffmpeg /tmp/ffmpeg'], shell=True)
    subprocess.call(['chmod 755 /tmp/ffmpeg'], shell=True)

    mp3_relative_path = strip_extension(name_of_audio_file_on_s3bucket) + '.mp3'
    mp3_output_path = '/tmp/{0}'.format(mp3_relative_path)

    subprocess.call(['/tmp/ffmpeg -y -i /tmp/{0} -ab 320k {1} </dev/null'
                    .format(name_of_audio_file_on_s3bucket, mp3_output_path)], shell=True)

    s3.Bucket(name_of_bucket_with_output).upload_file(mp3_output_path, mp3_relative_path)
