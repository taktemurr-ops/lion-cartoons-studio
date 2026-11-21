#!/usr/bin/env python3
"""YouTube OAuth upload (explicit --publish required; private by default)."""
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="Lion Cartoons | Özgün çocuk içerikleri")
    parser.add_argument("--privacy", choices=["private", "unlisted", "public"], default="private")
    parser.add_argument("--made-for-kids", action="store_true")
    parser.add_argument("--publish", action="store_true", help="Upload after separate OAuth authorization")
    args = parser.parse_args()
    target = Path(args.file)
    if not target.is_file():
        parser.error(f"Video dosyası bulunamadı: {target}")
    if not args.publish:
        print(f"DRY RUN | {target} | {args.title} | {args.privacy} | made_for_kids={args.made_for_kids}")
        print("Upload için --publish ve yerel Google OAuth gerekiyor.")
        return
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    secret = Path("client_secret.json")
    if not secret.exists():
        parser.error("OAuth client_secret.json yerel dosyası eksik; bunu GitHub'a göndermeyin.")
    token = Path("token.json")
    creds = Credentials.from_authorized_user_file(str(token), scopes) if token.exists() else None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = InstalledAppFlow.from_client_secrets_file(str(secret), scopes).run_local_server(port=0)
        token.write_text(creds.to_json(), encoding="utf-8")
    api = build("youtube", "v3", credentials=creds)
    payload = {
        "snippet": {"title": args.title, "description": args.description, "categoryId": "1"},
        "status": {"privacyStatus": args.privacy, "selfDeclaredMadeForKids": args.made_for_kids},
    }
    req = api.videos().insert(
        part="snippet,status", body=payload,
        media_body=MediaFileUpload(str(target), mimetype="video/mp4", resumable=True))
    result = None
    while result is None:
        status, result = req.next_chunk()
        if status: print(f"Yükleniyor: %{int(status.progress()*100)}")
    print("Video ID:", result.get("id"))

if __name__ == "__main__":
    main()
