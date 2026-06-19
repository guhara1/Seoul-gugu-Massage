#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Google Indexing API 즉시 색인 통보.

⚠️ 공식적으로 Indexing API는 JobPosting/BroadcastEvent 구조화 데이터 페이지를 위한 것입니다.
   일반 페이지에도 동작하는 경우가 많지만 보장되지 않으며, 일반 색인은 Search Console
   사이트맵 제출이 기본입니다. (Google은 IndexNow 미참여)

준비:
  1) Google Cloud 프로젝트 생성 → "Indexing API" 사용 설정
  2) 서비스 계정 생성 → JSON 키 다운로드 (예: service_account.json)
  3) Search Console에서 해당 사이트 속성에 서비스 계정 이메일을 '소유자'로 추가
  4) 의존성 설치:  pip install google-auth requests
  5) 실행:
        export GOOGLE_APPLICATION_CREDENTIALS=service_account.json
        python tools/google_index.py            # sitemap.xml 전체(기본 200/일 한도 주의)
        python tools/google_index.py /guide/booking/   # 특정 URL만
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from data_site import SITE  # noqa: E402

BASE = SITE["base_url"].rstrip("/")
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python build.py` 를 실행하세요.")
    return re.findall(r"<loc>([^<]+)</loc>", open(path, encoding="utf-8").read())


def normalize(args):
    out = []
    for a in args:
        a = a.strip()
        out.append(a if a.startswith("http") else BASE + (a if a.startswith("/") else "/" + a))
    return out


def main():
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        sys.exit("의존성 필요:  pip install google-auth requests")

    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "service_account.json")
    if not os.path.exists(cred_path):
        sys.exit(f"서비스 계정 키를 찾을 수 없습니다: {cred_path}\n"
                 "GOOGLE_APPLICATION_CREDENTIALS 환경변수로 경로를 지정하세요.")

    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    session = AuthorizedSession(creds)

    args = sys.argv[1:]
    urls = normalize(args) if args else sitemap_urls()
    print(f"통보 URL 수: {len(urls)} (Indexing API 기본 한도 200/일)\n")
    ok = 0
    for u in urls:
        r = session.post(ENDPOINT, json={"url": u, "type": "URL_UPDATED"})
        if r.status_code == 200:
            ok += 1
            print(f"[OK] {u}")
        else:
            print(f"[ERR {r.status_code}] {u} → {r.text[:160]}")
    print(f"\n완료: {ok}/{len(urls)} 성공")


if __name__ == "__main__":
    main()
