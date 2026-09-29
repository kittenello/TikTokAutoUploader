"""Small Windows-friendly CLI for TikTok photo carousels.

Examples:
    python photo_uploader.py login main backup
    python photo_uploader.py photos ./photos --accounts main backup --caption "hello"
"""

import argparse
import re
from pathlib import Path

from tiktokautouploader import (
    login_tiktok_account,
    upload_tiktok_photos_multi,
)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}


def natural_key(path: Path):
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def collect_photos(folder: str):
    root = Path(folder).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Photo folder not found: {root}")

    photos = sorted(
        (p for p in root.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS),
        key=natural_key,
    )
    if not photos:
        raise SystemExit(f"No supported photos found in: {root}")

    return [str(photo) for photo in photos]


def cmd_login(args):
    for account in args.accounts:
        print(f"\n=== Login: {account} ===")
        login_tiktok_account(account)


def cmd_photos(args):
    photos = collect_photos(args.folder)
    print(f"Found {len(photos)} photo(s):")
    for index, photo in enumerate(photos, 1):
        print(f"  {index:02d}. {Path(photo).name}")

    hashtags = args.hashtags or None
    results = upload_tiktok_photos_multi(
        photos=photos,
        description=args.caption,
        accountnames=args.accounts,
        hashtags=hashtags,
        headless=not args.visible_browser,
        stealth=args.stealth,
        visibility=args.visibility,
        continue_on_error=True,
    )

    print("\n=== Results ===")
    for account, result in results.items():
        print(f"{account}: {result}")


def build_parser():
    parser = argparse.ArgumentParser(
        description="Login TikTok accounts and upload the same photo carousel to multiple accounts."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    login = sub.add_parser("login", help="Log in and save cookies for one or more account labels.")
    login.add_argument("accounts", nargs="+", help="Local account labels, e.g. main backup")
    login.set_defaults(func=cmd_login)

    photos = sub.add_parser("photos", help="Upload all supported images from a folder as one carousel.")
    photos.add_argument("folder", help="Folder containing the carousel photos.")
    photos.add_argument("--accounts", nargs="+", required=True, help="Saved account labels.")
    photos.add_argument("--caption", default="", help="Post caption.")
    photos.add_argument(
        "--hashtags",
        nargs="*",
        default=None,
        help="Hashtags with or without #, e.g. --hashtags fyp memes",
    )
    photos.add_argument(
        "--visibility",
        choices=["everyone", "friends", "private"],
        default="everyone",
    )
    photos.add_argument(
        "--visible-browser",
        action="store_true",
        help="Show Chromium while uploading. Recommended for the first test.",
    )
    photos.add_argument(
        "--stealth",
        action="store_true",
        help="Use extra human-like delays provided by the library.",
    )
    photos.set_defaults(func=cmd_photos)
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
