#!/usr/bin/env python3
"""Upload a reviewed MP4 to YouTube; default private and explicit opt-in."""
import argparse
import json
import os
from pathlib import Path


def get_credentials(scopes):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow

    env_token = os.environ.get("YOUTUBE_OAUTH_TOKEN_JSON")
    token_path = Path("token.json")
    if env_token:
        creds = Credentials.from_authorized_user_info(json.loads(env_token), scopes)
    elif token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), scopes)
    else:
        creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif not os.environ.get("CI") and Path("client_secret.json").is_file():
            creds = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", scopes
            ).run_local_server(port=0, access_type="offline", prompt="consent")
            token_path.write_text(creds.to_json(), encoding="utf-8")
        else:
            raise SystemExit(
                "YouTube OAuth yetkisi eksik. Kimlik bilgilerini GitHub deposuna "
                "koymayın; Actions Secret: YOUTUBE_OAUTH_TOKEN_JSON."
            )
    return creds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="Lion Cartoons | Özgün çocuk içerikleri")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--made-for-kids", action="store_true")
    parser.add_argument("--expected-channel-id", default="")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    mp4 = Path(args.file)
    if not mp4.is_file() or mp4.suffix.lower() != ".mp4":
        parser.error("Geçerli MP4 dosyası bulunamadı.")
    if not args.publish:
        print(f"DRY RUN: {mp4} / {args.title} / {args.privacy} / kids={args.made_for_kids}")
        return

    # The YouTube API upload scope is not interchangeable with Windsor.ai authorization.
    scopes = [
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.readonly",
    ]
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    api = build("youtube", "v3", credentials=get_credentials(scopes))
    channel_response = api.channels().list(part="id,snippet", mine=True).execute()
    channels = channel_response.get("items", [])
    if len(channels) != 1:
        raise SystemExit("Hesabın eriştiği kanal tekil doğrulanamadı. Yükleme iptal.")
    channel = channels[0]
    channel_id = channel["id"]
    if not args.expected_channel_id:
        raise SystemExit(
            f"Kanal kimliği doğrulaması gerekiyor: {channel_id}. "
            "EXPECTED_YOUTUBE_CHANNEL_ID ayarlanmadan yükleme yapılmaz."
        )
    if args.expected_channel_id != channel_id:
        raise SystemExit("Kanal kimliği eşleşmedi; yanlış kanala yükleme engellendi.")

    request = api.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": args.title,
                "description": args.description,
                "categoryId": "1",
            },
            "status": {
                "privacyStatus": args.privacy,
                "selfDeclaredMadeForKids": args.made_for_kids,
            },
        },
        media_body=MediaFileUpload(str(mp4), mimetype="video/mp4", resumable=True),
    )
    response = None
    while response is None:
        progress, response = request.next_chunk()
        if progress:
            print(f"Upload: %{int(progress.progress() * 100)}")
    print("Uploaded video ID:", response["id"])


if __name__ == "__main__":
    main()
