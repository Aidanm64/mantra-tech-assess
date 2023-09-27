from urllib.parse import urljoin
import pytest


def test_get_status(wait_for_api):

    request_session, api_url, headers = wait_for_api

    response = request_session.get(urljoin(api_url, "/"))

    assert response.status_code == 200


def test_create_recording(wait_for_api):

    request_session, api_url, headers = wait_for_api

    audio_video_file = open("backend/test/data/audio_video_file.mp4", 'rb')
    audio_only_file = open("backend/test/data/audio_only_file.aac", 'rb')
    video_only_file = open("backend/test/data/video_only_file.mp4", 'rb')
    response = request_session.post(api_url + "recordings",
                                    files={
                                        'audio_video_file': audio_video_file,
                                        'audio_only_file': audio_only_file,
                                        'video_only_file': video_only_file
                                    })
    audio_video_file.close()
    audio_only_file.close()
    video_only_file.close()
    assert response.status_code == 201

    pytest.recording_uuid = response.json()['uuid']


def test_get_recording(wait_for_api):
    request_session, api_url, headers = wait_for_api

    response = request_session.get(f'{api_url}recordings/{pytest.recording_uuid}')

    print(response.json())
    assert response.status_code == 200
    assert 0
