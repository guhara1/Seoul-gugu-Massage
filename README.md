# 서울 출장마사지 · 홈타이 지역 안내 (GUGU 마사지)

서울 25개 자치구 기준으로 출장마사지·홈타이 **예약 전 확인 정보**(생활권 · 대표 행정동 · 핵심 역세권 · 이용 주의사항)를 안내하는 정적 사이트입니다.
정적 HTML + Python 빌드 스크립트로 생성하며, GitHub Pages 등 정적 호스팅에 바로 배포할 수 있습니다.

- 상호: **GUGU 마사지**
- 전화예약: **0508-202-4719**
- 디자인 테마: **미드나잇 글래스** (미드나잇 블루 그라데이션 + 글래스모피즘 + 골드 글로우 / Pretendard)

## 1차 구축 범위 (현재)

| 구분 | 개수 | 비고 |
|---|---|---|
| 메인 | 1 | `/seoul-chuljangmassage/` |
| 자치구 | 25 | `/seoul/<slug>-gu-chuljangmassage/` · 각 2000~2500자 고유 본문 |
| 이용 안내 | 5 | 예약 안내 · 이용 전 확인사항 · 홈타이 가이드 · 고객센터 · 개인정보 처리방침 |

> 대표 행정동(약 180~220개)·역세권 페이지는 GSC 색인·유입 데이터 확인 후 2차로 확장합니다.

## 구조

```
build.py                # 빌더 (실행 진입점)
src/
  data_site.py          # 사이트 설정 · 25개 구 메타 · 행정동 버튼
  data_districts.py     # 구별 고유 본문 콘텐츠 (도어웨이 방지: 구마다 내용 상이)
assets/
  css/style.css         # 디자인 토큰 + 글래스 컴포넌트
  img/                  # favicon · OG 커버
# --- 빌드 산출물 (커밋됨) ---
index.html              # 메인으로 리다이렉트
seoul-chuljangmassage/  # 메인
seoul/.../              # 25개 자치구
guide/ support/ privacy/
sitemap.xml  robots.txt
```

## 빌드

```bash
python3 build.py
```

배포 도메인이 정해지면 `src/data_site.py`의 `SITE["base_url"]`을 실제 도메인으로 수정한 뒤 다시 빌드하세요. (canonical · og:url · sitemap · JSON-LD에 반영됩니다.)

## SEO 설계 요점

- **개별 메타데이터**: 25개 구 모두 SEO Title·Description(80자 이내) 개별 작성.
- **구조화 데이터**: WebPage · BreadcrumbList · Organization · ImageObject(primaryImageOfPage) · FAQPage(JSON-LD).
- **선호 이미지**: schema.org `ImageObject` + `og:image` 동시 지정.
- **도어웨이 방지**: 구마다 실제 생활권·상권·업무·역세권·예약 기준을 다르게 작성, 지역명만 바꾼 복제 금지.
- **E-E-A-T**: 전 페이지 하단에 작성·검수·최종 수정일·작성 방식·목적 명시. 가짜 경험 표현 미사용(정보형 서술).
- **성능/페이지 경험**: JS 렌더 의존 없는 정적 HTML, 시스템 폰트 폴백, `prefers-reduced-motion` 대응.
- **LocalBusiness 미사용**: 실제 오프라인 사업장 주소가 없어 Organization으로만 표기(안전).

> 합법적·건전한 방문 관리 서비스를 전제로 한 정보 안내 사이트이며, 선정적·허위 표현을 사용하지 않습니다.
