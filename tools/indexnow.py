#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IndexNow 즉시 색인 통보 (Bing · Naver · Yandex 등 참여 엔진).

사용법(로컬에서 실행 — 외부 네트워크 필요):
  python tools/indexnow.py                # sitemap.xml의 모든 URL 통보
  python tools/indexnow.py /  /guide/booking/   # 특정 URL만 통보(경로 또는 전체 URL)

준비:
  1) python build.py 로 빌드하면 루트에 {key}.txt 키 파일과 sitemap.xml 이 생성됩니다.
  2) 사이트를 배포해 https://<도메인>/{key}.txt 가 200으로 열려야 합니다(키 검증).
  3) 글/페이지를 올리거나 수정할 때마다 이 스크립트를 실행하면 즉시 통보됩니다.

IndexNow는 한 곳에 제출하면 참여 엔진끼리 공유하지만, 반영을 빠르게 하려고
대표 엔드포인트 여러 곳에 함께 제출합니다. (Google은 IndexNow 미참여 → google_index.py 사용)
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from data_site import SITE  # noqa: E402

BASE = SITE["base_url"].rstrip("/")
HOST = BASE.split("://", 1)[-1]
KEY = SITE["indexnow_key"]
KEY_LOCATION = f"{BASE}/{KEY}.txt"

ENDPOINTS = [
    "https://api.indexnow.org/indexnow",        # 통합(빙·얀덱스 등으로 분배)
    "https://www.bing.com/indexnow",            # 빙 직접
    "https://searchadvisor.naver.com/indexnow",  # 네이버 직접
    "https://yandex.com/indexnow",              # 얀덱스 직접
]


def sitemap_urls():
    path = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(path):
        sys.exit("sitemap.xml 이 없습니다. 먼저 `python build.py` 를 실행하세요.")
    xml = open(path, encoding="utf-8").read()
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def normalize(args):
    urls = []
    for a in args:
        a = a.strip()
        if a.startswith("http"):
            urls.append(a)
        else:
            urls.append(BASE + (a if a.startswith("/") else "/" + a))
    return urls


def chunked(seq, n=10000):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def submit(endpoint, url_list):
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": url_list,
    }).encode("utf-8")
    req = urllib.request.Request(
        endpoint, data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read(200).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read(200).decode("utf-8", "ignore")
    except Exception as e:  # noqa: BLE001
        return None, str(e)


def main():
    args = sys.argv[1:]
    urls = normalize(args) if args else sitemap_urls()
    if not urls:
        sys.exit("통보할 URL이 없습니다.")
    print(f"호스트: {HOST}")
    print(f"키 위치: {KEY_LOCATION}")
    print(f"통보 URL 수: {len(urls)}\n")
    for batch in chunked(urls):
        for ep in ENDPOINTS:
            code, body = submit(ep, batch)
            ok = "OK" if code in (200, 202) else "확인필요"
            print(f"[{ok}] {ep} → HTTP {code} {('· ' + body.strip()) if body else ''}")
    print("\n완료. (200/202 = 접수 성공. 키 검증 실패 시 422/403 — 배포된 키 파일 URL을 확인하세요.)")


if __name__ == "__main__":
    main()
