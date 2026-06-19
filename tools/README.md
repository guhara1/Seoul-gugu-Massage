# 색인(인덱싱) 자동화 도구

빌드 시 자동 생성되는 것 (`python build.py`):

| 파일 | 용도 |
|---|---|
| `sitemap.xml` | 색인 대상 URL 목록 (noindex 페이지 제외) |
| `rss.xml` | RSS 2.0 피드 (페이지 발견용, `<head>`에 alternate 링크 연결) |
| `robots.txt` | 전체 허용 + 구글/네이버(Yeti)/빙/다음 봇 + 사이트맵 선언 |
| `{indexnow_key}.txt` | IndexNow 키 검증 파일 (루트) |

## 가장 빠른 색인 워크플로

### 1. 최초 1회 등록
- **Google Search Console**: 속성 추가 → `sitemap.xml` 제출
- **네이버 서치어드바이저**: 사이트 등록(소유확인) → `sitemap.xml`, `rss.xml` 제출
- **Bing Webmaster Tools**: 사이트 추가 → `sitemap.xml` 제출

### 2. 글/페이지를 올리거나 수정할 때마다 (즉시 통보)
```bash
python build.py                 # 사이트 재생성
# (배포 후)
python tools/indexnow.py        # 빙·네이버·얀덱스에 즉시 통보 (sitemap 전체)
python tools/indexnow.py /guide/booking/ /seoul/gangnam-gu-chuljangmassage/   # 특정 URL만
```

> IndexNow는 **Bing·Naver·Yandex·Seznam**이 참여합니다. 한 곳에 제출하면 공유되지만,
> 반영을 빠르게 하려고 대표 엔드포인트 여러 곳에 함께 제출합니다.

### 3. (선택) 구글 즉시 통보 — Indexing API
구글은 IndexNow에 참여하지 않습니다. 일반 색인은 **Search Console 사이트맵**이 기본이며,
즉시 통보가 필요하면 Indexing API를 쓸 수 있습니다(설정은 `google_index.py` 상단 주석 참고).
```bash
export GOOGLE_APPLICATION_CREDENTIALS=service_account.json
python tools/google_index.py
```
⚠️ Indexing API는 공식적으로 JobPosting/BroadcastEvent용이며 일반 페이지는 보장되지 않습니다.
기본 한도 200 URL/일.

## IndexNow 키
- 키는 `src/data_site.py`의 `SITE["indexnow_key"]`에 저장되어 있고, 빌드 시 `{key}.txt`로 출력됩니다.
- 배포 후 `https://<도메인>/{key}.txt` 가 **200**으로 열려야 통보가 검증됩니다.

## 참고: 사이트맵 핑은 폐지됨
구글(2023년)과 빙은 익명 `GET /ping?sitemap=` 엔드포인트를 **폐지**했습니다.
따라서 사이트맵 핑 대신 **Search Console/서치어드바이저 사이트맵 제출 + IndexNow**를 사용합니다.

## 네트워크 주의
이 도구들은 외부로 HTTP 요청을 보냅니다. 외부 네트워크가 열린 **로컬 PC에서 실행**하세요.
(샌드박스/CI 환경에서는 egress 정책으로 차단될 수 있습니다.)
