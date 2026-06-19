#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""정적 사이트 빌더 — 서울 출장마사지·홈타이 지역 안내.

출력: 저장소 루트에 디렉터리형 정적 HTML + sitemap.xml + robots.txt
실행: python3 build.py
"""

import html
import json
import os
import shutil

from src.data_site import (
    SITE, KEYWORDS_MAIN, KEYWORDS_SUB, GUIDE_PAGES, DISTRICTS, DONGS,
)
from src.data_districts import CONTENT

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = SITE["base_url"].rstrip("/")


# --------------------------------------------------------------------- #
# 유틸                                                                   #
# --------------------------------------------------------------------- #
def esc(s):
    return html.escape(str(s), quote=True)


def write(path_parts, content):
    """path_parts: URL 경로 조각. index.html 로 저장."""
    out_dir = os.path.join(ROOT, *path_parts)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)


def district_url(slug):
    return f"/seoul/{slug}-chuljangmassage/"


# --------------------------------------------------------------------- #
# 공통 레이아웃                                                          #
# --------------------------------------------------------------------- #
def head(title, desc, canonical, schema_blocks, extra_keywords=""):
    kw = ", ".join([KEYWORDS_MAIN] + KEYWORDS_SUB + ([extra_keywords] if extra_keywords else []))
    og_img = BASE + SITE["og_image"]
    schema_json = "\n".join(
        f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>'
        for b in schema_blocks
    )
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="keywords" content="{esc(kw)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="{esc(SITE['author'])}">
<link rel="canonical" href="{esc(BASE + canonical)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITE['brand'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(BASE + canonical)}">
<meta property="og:image" content="{esc(og_img)}">
<meta property="og:image:alt" content="{esc(SITE['brand'])} — 서울 출장마사지·홈타이 지역 안내">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_img)}">
<meta name="theme-color" content="#070b1d">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/style.css">
{schema_json}
</head>"""


def header():
    nav_links = "".join(
        f'<a href="{esc(g["url"])}">{esc(g["label"])}</a>' for g in GUIDE_PAGES[:3]
    )
    return f"""<a class="skip-link" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="/seoul-chuljangmassage/">
      <span class="mark"><span>G</span></span>
      <span>{esc(SITE['brand'])} <small class="muted">서울 출장마사지</small></span>
    </a>
    <nav aria-label="주요 메뉴" style="display:flex;align-items:center;gap:18px">
      <span class="muted" style="display:none">{nav_links}</span>
      <a class="nav-cta" href="tel:{esc(SITE['phone_tel'])}">📞 전화예약 {esc(SITE['phone'])}</a>
    </nav>
  </div>
</header>"""


def book_bar():
    return f"""<div class="book-bar" role="complementary" aria-label="예약 바">
  <a class="call" href="tel:{esc(SITE['phone_tel'])}">전화예약 {esc(SITE['phone'])}</a>
  <a class="info" href="/guide/booking/">예약 안내</a>
</div>"""


def footer():
    guide_links = "".join(f'<a href="{esc(g["url"])}">{esc(g["label"])}</a>' for g in GUIDE_PAGES)
    district_links = "".join(
        f'<a href="{esc(district_url(d["slug"]))}">{esc(d["name"])}</a>'
        for d in DISTRICTS[:12]
    )
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <h4>{esc(SITE['brand'])}</h4>
        <p class="footer-note">서울 25개 자치구·행정동·역세권 기준으로 출장마사지와 홈타이 예약 전 확인 정보를 안내하는 지역 정보 사이트입니다. 예약 전 방문 가능 지역, 이동 기준, 이용 주의사항을 확인하세요.</p>
        <p style="margin-top:14px"><a class="nav-cta" href="tel:{esc(SITE['phone_tel'])}">📞 {esc(SITE['phone'])}</a></p>
      </div>
      <div>
        <h4>이용 안내</h4>
        <div class="footer-links">{guide_links}</div>
      </div>
      <div>
        <h4>자치구 바로가기</h4>
        <div class="footer-links">{district_links}<a href="/seoul-chuljangmassage/#districts">전체 25개 구 →</a></div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 {esc(SITE['brand'])}. 서울 출장마사지·홈타이 지역 안내.</span>
      <span>전화예약 {esc(SITE['phone'])} · 최종 수정일 {esc(SITE['updated_label'])}</span>
    </div>
  </div>
</footer>"""


def page(title, desc, canonical, body, schema_blocks, extra_keywords=""):
    return f"""{head(title, desc, canonical, schema_blocks, extra_keywords)}
<body>
{header()}
<main id="main">
{body}
</main>
{footer()}
{book_bar()}
</body>
</html>"""


# --------------------------------------------------------------------- #
# 스키마(JSON-LD) 빌더                                                   #
# --------------------------------------------------------------------- #
def org_schema():
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE["brand"],
        "url": BASE + "/seoul-chuljangmassage/",
        "telephone": SITE["phone"],
        "areaServed": {"@type": "City", "name": "서울특별시"},
        "logo": BASE + SITE["og_image"],
        "image": BASE + SITE["og_image"],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": SITE["phone"],
            "contactType": "reservations",
            "areaServed": "KR",
            "availableLanguage": "Korean",
        },
    }


def image_object(name):
    return {
        "@context": "https://schema.org",
        "@type": "ImageObject",
        "contentUrl": BASE + SITE["og_image"],
        "url": BASE + SITE["og_image"],
        "caption": name,
        "creditText": SITE["brand"],
    }


def webpage_schema(name, desc, url):
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "description": desc,
        "url": BASE + url,
        "inLanguage": "ko-KR",
        "isPartOf": {"@type": "WebSite", "name": SITE["brand"], "url": BASE + "/seoul-chuljangmassage/"},
        "primaryImageOfPage": {
            "@type": "ImageObject",
            "contentUrl": BASE + SITE["og_image"],
            "url": BASE + SITE["og_image"],
        },
        "dateModified": SITE["updated"],
    }


def breadcrumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": BASE + url}
            for i, (name, url) in enumerate(items)
        ],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


# --------------------------------------------------------------------- #
# 공통 컴포넌트                                                          #
# --------------------------------------------------------------------- #
def breadcrumb_html(items):
    parts = []
    for i, (name, url) in enumerate(items):
        if i:
            parts.append('<span class="sep">›</span>')
        if i == len(items) - 1:
            parts.append(f"<span>{esc(name)}</span>")
        else:
            parts.append(f'<a href="{esc(url)}">{esc(name)}</a>')
    return f'<nav class="breadcrumb" aria-label="현재 위치">{"".join(parts)}</nav>'


def author_box(district_name=None):
    method = ("서울시 자치구·행정동 구조, 역세권, 실제 예약 전 확인사항을 기준으로 작성"
              if not district_name else
              f"{district_name}의 생활권·대표 행정동·역세권과 예약 전 확인 기준을 토대로 작성")
    return f"""<section class="section">
  <div class="glass card author-box">
    <div class="eyebrow">콘텐츠 정보</div>
    <div class="row"><span class="k">작성</span><span class="v">{esc(SITE['author'])}</span></div>
    <div class="row"><span class="k">검수</span><span class="v">{esc(SITE['reviewer'])}</span></div>
    <div class="row"><span class="k">최종 수정일</span><span class="v">{esc(SITE['updated_label'])}</span></div>
    <div class="row"><span class="k">작성 방식</span><span class="v">{esc(method)}</span></div>
    <div class="row"><span class="k">콘텐츠 목적</span><span class="v">사용자가 예약 전 지역, 이동 기준, 추가비, 이용 주의사항을 확인하도록 돕기 위함</span></div>
  </div>
</section>"""


def cta_panel(heading="지금 전화로 바로 예약하세요"):
    return f"""<section class="section">
  <div class="glass card cta-panel">
    <div class="eyebrow center" style="justify-content:center">GUGU 마사지 · 전화예약</div>
    <h2>{esc(heading)}</h2>
    <a class="phone text-gold" href="tel:{esc(SITE['phone_tel'])}">{esc(SITE['phone'])}</a>
    <p class="muted">예약 전 방문 가능 지역·시간, 추가 이동비, 취소 기준을 함께 안내해 드립니다.</p>
    <div class="cta-row" style="justify-content:center">
      <a class="btn btn-gold" href="tel:{esc(SITE['phone_tel'])}">📞 전화예약</a>
      <a class="btn btn-ghost" href="/guide/booking/">예약 절차 보기</a>
    </div>
  </div>
</section>"""


# --------------------------------------------------------------------- #
# 메인 페이지                                                            #
# --------------------------------------------------------------------- #
def render_main():
    url = "/seoul-chuljangmassage/"
    title = "서울 출장마사지｜25개 자치구 홈타이 지역별 예약 안내"
    desc = "서울 출장마사지·홈타이 예약 전 자치구, 행정동, 역세권 정보를 확인하세요."

    # 자치구 버튼 그리드
    btns = []
    for d in DISTRICTS:
        rep = "·".join(s.replace("역", "") for s in d["stations"][:3])
        btns.append(f"""<a class="area-btn" href="{esc(district_url(d['slug']))}">
  <span>{esc(d['name'])} 출장마사지<span class="sub">{esc(rep)} 생활권</span></span>
  <span class="arw">→</span>
</a>""")
    grid = '<div class="area-grid">' + "".join(btns) + "</div>"

    body = f"""
<section class="hero">
  <div class="wrap">
    <div class="eyebrow">SEOUL · 출장마사지 &amp; 홈타이</div>
    <h1>서울 출장마사지 · 서울특별시 홈타이<br><span class="text-gold">지역별 예약 안내</span></h1>
    <p class="lead">서울은 25개 자치구마다 생활권과 이동 기준이 다릅니다. 예약 전 본인 지역의 자치구·대표 행정동·핵심 역세권 정보를 먼저 확인하세요.</p>
    <div class="hero-badges">
      <span class="badge"><span class="dot"></span>25개 자치구 전지역 안내</span>
      <span class="badge"><span class="dot"></span>대표 행정동·역세권 기준</span>
      <span class="badge"><span class="dot"></span>예약 전 확인사항 제공</span>
    </div>
    <div class="cta-row">
      <a class="btn btn-gold" href="tel:{esc(SITE['phone_tel'])}">📞 전화예약 {esc(SITE['phone'])}</a>
      <a class="btn btn-ghost" href="#districts">25개 자치구 보기</a>
    </div>
  </div>
</section>

<section class="section" id="districts">
  <div class="wrap">
    <div class="eyebrow">자치구 선택</div>
    <h2>서울 25개 자치구 출장마사지·홈타이</h2>
    <p class="muted" style="max-width:64ch">원하는 자치구를 선택하면 해당 구의 생활권 설명과 대표 행정동 버튼, 핵심 역세권, 예약 전 확인사항을 확인할 수 있습니다.</p>
    <div style="margin-top:22px">{grid}</div>
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    <h2>서울 출장마사지 사이트 이용 방법</h2>
    <p>서울 출장마사지를 찾는 분들은 대부분 현재 위치에서 가까운 방문 가능 지역을 먼저 확인합니다. 서울은 25개 자치구로 나뉘고, 각 구마다 생활권과 이동 기준이 다릅니다. 강남구와 서초구는 강남역·역삼역·교대역·고속터미널역을 중심으로 업무지구와 주거지가 함께 있고, 송파구는 잠실역·문정역·가락시장역·석촌역 생활권이 중요합니다. 마포구는 홍대입구역·합정역·공덕역을 중심으로 상권과 주거지가 연결되고, 영등포구는 여의도와 영등포역·당산역 생활권을 함께 고려해야 합니다.</p>
    <p>메인페이지에서는 25개 자치구를 버튼으로 보여주고, 사용자가 구를 선택하면 해당 구 페이지 안에서 대표 행정동 버튼을 다시 고를 수 있도록 구성했습니다. 번호로 나뉜 행정동(예: 논현1·2동, 역삼1·2동, 잠실본동~잠실7동)은 대표동 한 곳으로 통합해, 사용자가 본인 생활권을 빠르게 찾고 검색엔진도 구조를 이해하기 쉽게 했습니다.</p>
    <p>각 구 페이지는 지역명만 바꾼 반복 콘텐츠가 아니라, 그 구의 실제 생활권·상권·업무지구·역세권 차이와 예약 전 확인사항을 담고 있습니다. 강남구 페이지는 테헤란로 업무지구와 압구정·청담 상권, 대치동 학원가, 수서역 생활권을 다루고, 마포구 페이지는 홍대입구·합정·공덕·상암DMC 생활권을 다루는 식으로 본문 내용이 서로 다릅니다.</p>
    <h2>서울 홈타이 예약 전 확인할 점</h2>
    <p>서울 홈타이는 자택·숙소·사무실 인근에서 예약 가능 여부를 먼저 확인한 뒤 이용하는 방문형 관리 서비스입니다. 예약 전에는 방문 가능 지역, 예약 가능 시간, 추가 이동비, 결제 방식, 취소 기준, 개인정보 처리 기준을 확인하는 것이 좋습니다. 서울은 거리보다 시간대별 교통 상황이 더 중요할 때가 많아, 강남역·여의도·홍대입구·잠실·서울역 주변은 평일 저녁과 주말의 이동 시간이 다를 수 있습니다. 자세한 공통 기준은 <a href="/guide/booking/">예약 안내</a>와 <a href="/guide/before-use/">이용 전 확인사항</a>에서 확인하세요.</p>
  </div>
</section>

{cta_panel()}
{author_box()}
"""
    schema = [
        org_schema(),
        webpage_schema(title, desc, url),
        breadcrumb_schema([("서울 출장마사지", url)]),
        image_object("서울 출장마사지·홈타이 지역 안내"),
    ]
    write(["seoul-chuljangmassage"], page(title, desc, url, body, schema))


# --------------------------------------------------------------------- #
# 자치구 페이지                                                          #
# --------------------------------------------------------------------- #
def render_district(d):
    slug = d["slug"]
    url = district_url(slug)
    name = d["name"]
    c = CONTENT[slug]

    # 행정동 칩 (본문 내 섹션 앵커로 연결)
    dong_chips = "".join(
        f'<a class="chip" href="#dong-area" aria-disabled="false">{esc(dong)}</a>'
        for dong in DONGS[slug]
    )
    # 역세권 정보 카드
    station_cards = "".join(
        f'<div class="glass card info-card"><h3>{esc(st)}</h3><p>{esc(name)} 생활권의 핵심 역세권으로, 출구·건물명을 함께 알려주면 이동 안내가 빠릅니다.</p></div>'
        for st in d["stations"]
    )
    # 관련 내부링크 (다른 구 6개 + 가이드)
    others = [x for x in DISTRICTS if x["slug"] != slug][:6]
    related = "".join(f'<a class="chip" href="{esc(district_url(o["slug"]))}">{esc(o["name"])} 출장마사지</a>' for o in others)
    guide_chips = "".join(f'<a class="chip" href="{esc(g["url"])}">{esc(g["label"])}</a>' for g in GUIDE_PAGES[:3])

    # FAQ
    faq_html = "".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"
        for q, a in c["faqs"]
    )

    crumbs = [("서울 출장마사지", "/seoul-chuljangmassage/"), (f"{name} 출장마사지", url)]

    body = f"""
<section class="hero" style="padding-block:clamp(38px,7vw,72px)">
  <div class="wrap">
    {breadcrumb_html(crumbs)}
    <div class="eyebrow">{esc(name)} · 출장마사지 &amp; 홈타이</div>
    <h1>{esc(name)} 출장마사지 · 홈타이<br><span class="text-gold">지역별 예약 안내</span></h1>
    <p class="lead">{esc(c['intro'])}</p>
    <div class="cta-row">
      <a class="btn btn-gold" href="tel:{esc(SITE['phone_tel'])}">📞 전화예약 {esc(SITE['phone'])}</a>
      <a class="btn btn-ghost" href="#dong-area">대표 행정동 보기</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    <h2>{esc(name)} 생활권 안내</h2>
    <p>{esc(c['living'])}</p>

    <h2>{esc(name)}에서 출장마사지·홈타이를 찾는 이유</h2>
    <p>{esc(name)}에서 출장마사지나 홈타이를 검색하는 분들은 보통 이동 시간을 줄이고 본인 생활권에서 방문 가능한지를 먼저 확인하려 합니다. 같은 {esc(name)} 안에서도 상권·업무지구·주거지의 흐름이 달라, 예약 전 본인 위치가 어느 권역에 속하는지 파악해 두면 안내가 한결 정확해집니다.</p>
  </div>
</section>

<section class="section" id="dong-area">
  <div class="wrap">
    <div class="eyebrow">대표 행정동</div>
    <h2 style="color:var(--t-hi)">{esc(name)} 대표 행정동</h2>
    <p class="muted" style="max-width:64ch">{esc(c['dong_intro'])}</p>
    <div class="chip-grid" style="margin-top:18px">{dong_chips}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="prose" style="max-width:74ch">
      <h2>{esc(name)} 핵심 역세권</h2>
      <p>{esc(c['station'])}</p>
    </div>
    <div class="info-grid" style="margin-top:20px">{station_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    <h2>{esc(name)} 주거지·상권·업무지구 차이</h2>
    <p>{esc(c['zones'])}</p>

    <h2>{esc(name)} 예약 전 확인사항</h2>
    <p>{esc(c['booking'])}</p>
    <ul>
      <li><strong>방문 가능 지역·시간</strong>은 예약 단계에서 확인하세요.</li>
      <li><strong>추가 이동비·심야 기준</strong>은 권역·시간대에 따라 달라질 수 있습니다.</li>
      <li><strong>결제 방식·취소 기준</strong>은 예약 전에 미리 안내받는 것이 좋습니다.</li>
      <li><strong>위치 정보</strong>는 가까운 역 출구, 건물명, 단지·동을 함께 전달하면 정확합니다.</li>
    </ul>

    <h2>안전·합법·개인정보 안내</h2>
    <p>{esc(SITE['brand'])}는 {esc(name)} 지역 안내에서 과장된 표현이나 허위 후기, 선정적 문구를 사용하지 않습니다. 이 페이지는 예약 전 지역·이동 기준·이용 주의사항을 확인하도록 돕는 정보형 안내이며, 실제 운영 데이터가 없는 경험성 표현은 사용하지 않습니다. 예약 과정에서 수집되는 개인정보는 <a href="/privacy/">개인정보 처리방침</a> 기준에 따라 처리됩니다.</p>
  </div>
</section>

<section class="section faq">
  <div class="wrap" style="max-width:820px">
    <div class="eyebrow">자주 묻는 질문</div>
    <h2 style="color:var(--t-hi)">{esc(name)} 출장마사지 FAQ</h2>
    {faq_html}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="eyebrow">관련 안내</div>
    <h2 style="color:var(--t-hi)">함께 확인하면 좋은 페이지</h2>
    <p class="muted">인접 자치구와 공통 이용 안내를 함께 확인하면 예약이 더 수월합니다.</p>
    <div class="chip-grid" style="margin-top:16px">{related}{guide_chips}</div>
  </div>
</section>

{cta_panel(f"{name} 출장마사지·홈타이, 전화로 예약하세요")}

<section class="section">
  <div class="wrap prose">
    <p>{esc(c['closing'])}</p>
  </div>
</section>

{author_box(name)}
"""
    schema = [
        org_schema(),
        webpage_schema(d["title"], d["desc"], url),
        breadcrumb_schema(crumbs),
        faq_schema(c["faqs"]),
        image_object(f"{name} 출장마사지·홈타이 지역 안내"),
    ]
    write(["seoul", f"{slug}-chuljangmassage"],
          page(d["title"], d["desc"], url, body, schema, extra_keywords=f"{name} 출장마사지, {name} 홈타이"))


# --------------------------------------------------------------------- #
# 가이드 / 안내 페이지                                                   #
# --------------------------------------------------------------------- #
def simple_page(path_parts, url, title, desc, crumbs, inner, faqs=None, extra_kw=""):
    faq_block = ""
    schema = [org_schema(), webpage_schema(title, desc, url), breadcrumb_schema(crumbs),
              image_object(title)]
    if faqs:
        faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
        faq_block = f"""<section class="section faq"><div class="wrap" style="max-width:820px">
        <div class="eyebrow">자주 묻는 질문</div><h2 style="color:var(--t-hi)">FAQ</h2>{faq_html}</div></section>"""
        schema.append(faq_schema(faqs))
    body = f"""
<section class="hero" style="padding-block:clamp(38px,7vw,64px)">
  <div class="wrap">
    {breadcrumb_html(crumbs)}
    <div class="eyebrow">이용 안내</div>
    <h1>{esc(title.split('｜')[0])}</h1>
    <p class="lead">{esc(desc)}</p>
  </div>
</section>
<section class="section"><div class="wrap prose">{inner}</div></section>
{faq_block}
{cta_panel()}
{author_box()}
"""
    write(path_parts, page(title, desc, url, body, schema, extra_keywords=extra_kw))


def render_guides():
    H = "/seoul-chuljangmassage/"

    # 1) 예약 안내
    simple_page(
        ["guide", "booking"], "/guide/booking/",
        "예약 안내｜서울 출장마사지·홈타이 예약 절차",
        "서울 출장마사지·홈타이 예약 절차, 가능 시간, 추가 이동비, 취소 기준을 안내합니다.",
        [("서울 출장마사지", H), ("예약 안내", "/guide/booking/")],
        f"""
        <h2>예약 절차</h2>
        <p>서울 출장마사지·홈타이 예약은 전화로 진행됩니다. 전화예약 번호 <a href="tel:{esc(SITE['phone_tel'])}"><strong>{esc(SITE['phone'])}</strong></a>로 연락해 방문 희망 지역(자치구·행정동 또는 가까운 역), 희망 시간, 인원, 위치 유형(아파트 단지·오피스텔·주택 등)을 알려주시면 가능 여부를 안내해 드립니다.</p>
        <ul>
          <li><strong>1단계</strong> 전화로 희망 지역·시간 문의</li>
          <li><strong>2단계</strong> 방문 가능 지역·시간 및 추가 이동비 안내</li>
          <li><strong>3단계</strong> 위치(역 출구·건물명·동) 전달 및 예약 확정</li>
          <li><strong>4단계</strong> 방문 및 이용</li>
        </ul>
        <h2>예약 가능 시간</h2>
        <p>예약 가능 시간은 지역과 시간대에 따라 달라질 수 있습니다. 서울은 거리보다 시간대별 교통 상황이 이동 시간에 더 큰 영향을 주므로, 강남·여의도·홍대·잠실·서울역 등 혼잡 권역은 희망 시간에 여유를 두고 예약하시길 권장합니다.</p>
        <h2>추가 이동비 기준</h2>
        <p>기본 안내 외에 거리·심야 시간대에 따라 추가 이동비가 발생할 수 있습니다. 정확한 금액은 위치와 시간대를 기준으로 예약 시 미리 안내해 드립니다.</p>
        <h2>결제 및 취소 기준</h2>
        <p>결제 방식과 취소·변경 기준은 예약 확정 단계에서 안내됩니다. 예약 변경이나 취소가 필요한 경우 가능한 빨리 전화로 알려주시면 원활하게 조정할 수 있습니다.</p>
        """,
        faqs=[
            ("예약은 어떻게 하나요?", f"전화예약 {SITE['phone']}로 희망 지역과 시간을 알려주시면 가능 여부를 안내해 드립니다."),
            ("당일 예약도 가능한가요?", "지역과 시간대에 따라 다릅니다. 혼잡 권역은 여유 시간을 두고 문의하시면 안내가 수월합니다."),
            ("추가 이동비는 얼마인가요?", "위치와 시간대 기준으로 예약 시 미리 안내해 드립니다."),
        ],
        extra_kw="출장마사지 예약, 홈타이 예약",
    )

    # 2) 이용 전 확인사항
    simple_page(
        ["guide", "before-use"], "/guide/before-use/",
        "이용 전 확인사항｜서울 출장마사지·홈타이",
        "서울 출장마사지·홈타이 이용 전 방문 지역, 시간, 위치 전달, 주의사항을 확인하세요.",
        [("서울 출장마사지", H), ("이용 전 확인사항", "/guide/before-use/")],
        """
        <h2>이용 전 꼭 확인하세요</h2>
        <p>원활한 방문 관리를 위해 예약 전 아래 사항을 확인해 주세요. 정확한 정보를 전달할수록 이동 시간이 줄고 안내가 빨라집니다.</p>
        <h3>방문 지역과 위치</h3>
        <ul>
          <li>방문 가능 지역(자치구·행정동) 또는 가까운 역세권을 확인하세요.</li>
          <li>아파트는 단지명·동·정문/후문, 오피스텔·빌딩은 건물명·층·호수를 준비하세요.</li>
          <li>언덕·골목이 많은 주거지는 차량 진입 경로를 미리 알려주세요.</li>
        </ul>
        <h3>시간과 이동</h3>
        <ul>
          <li>서울은 시간대별 교통 상황에 따라 이동 시간이 달라질 수 있습니다.</li>
          <li>혼잡 권역·시간대는 희망 시간에 여유를 두는 것이 좋습니다.</li>
        </ul>
        <h3>이용 환경</h3>
        <ul>
          <li>편안하게 이용할 수 있는 공간과 환경을 미리 준비해 주세요.</li>
          <li>예약 인원과 이용 시간을 정확히 전달해 주세요.</li>
        </ul>
        <h2>건전한 이용 안내</h2>
        <p>본 사이트와 안내는 합법적이고 건전한 방문 관리 서비스를 전제로 합니다. 불법·선정적 요청은 제공되지 않으며, 모든 안내는 예약 전 확인 정보를 돕기 위한 것입니다.</p>
        """,
        extra_kw="이용 전 확인사항",
    )

    # 3) 홈타이 이용 가이드
    simple_page(
        ["guide", "hometai"], "/guide/hometai/",
        "홈타이 이용 가이드｜서울 홈타이 방문 관리 안내",
        "서울 홈타이가 무엇인지, 예약부터 이용까지 과정과 준비 사항을 안내합니다.",
        [("서울 출장마사지", H), ("홈타이 이용 가이드", "/guide/hometai/")],
        """
        <h2>홈타이란?</h2>
        <p>홈타이는 자택·숙소·사무실 등 이용자가 머무는 공간 인근에서 예약 가능 여부를 확인한 뒤 이용하는 방문형 관리 서비스를 말합니다. 출장마사지와 함께 자주 쓰이는 표현으로, 이동 부담을 줄이고 익숙한 공간에서 관리받고자 할 때 찾습니다.</p>
        <h2>이용 과정</h2>
        <ul>
          <li><strong>예약 확인</strong> 방문 가능 지역·시간을 전화로 확인합니다.</li>
          <li><strong>위치 전달</strong> 가까운 역·건물명·동을 정확히 전달합니다.</li>
          <li><strong>방문 준비</strong> 편안한 이용 공간과 환경을 준비합니다.</li>
          <li><strong>이용</strong> 예약한 시간에 방문 관리를 받습니다.</li>
        </ul>
        <h2>준비하면 좋은 점</h2>
        <p>방문 전 공간을 정리하고, 단지·건물 출입 절차나 주차 가능 여부를 미리 확인하면 이용이 한결 매끄럽습니다. 지역별 이동 기준은 각 자치구 페이지에서 확인할 수 있습니다.</p>
        <h2>지역별 안내 보기</h2>
        <p>서울 25개 자치구의 생활권·역세권·예약 전 확인사항은 <a href="/seoul-chuljangmassage/#districts">자치구별 안내</a>에서 확인하세요.</p>
        """,
        faqs=[
            ("홈타이와 출장마사지는 다른가요?", "둘 다 방문형 관리 서비스를 가리키는 표현으로, 자택·숙소 등 이용자 공간 인근에서 예약 가능 여부를 확인한 뒤 이용한다는 점이 같습니다."),
            ("어떤 공간에서 이용하나요?", "자택·숙소·사무실 등 예약 시 확인된 방문 가능 공간에서 이용합니다. 정확한 위치를 전달하면 안내가 빠릅니다."),
        ],
        extra_kw="서울 홈타이, 홈타이 가이드",
    )

    # 4) 고객센터
    simple_page(
        ["support"], "/support/",
        "고객센터｜서울 출장마사지·홈타이 문의",
        "서울 출장마사지·홈타이 예약 문의와 안내는 전화 고객센터로 연락하세요.",
        [("서울 출장마사지", H), ("고객센터", "/support/")],
        f"""
        <h2>전화 문의</h2>
        <p>예약·변경·취소, 방문 가능 지역 문의는 전화로 안내해 드립니다.</p>
        <p style="font-size:1.6rem;font-weight:800"><a class="text-gold" href="tel:{esc(SITE['phone_tel'])}">{esc(SITE['phone'])}</a></p>
        <h2>문의 시 알려주시면 좋은 정보</h2>
        <ul>
          <li>방문 희망 지역(자치구·행정동) 또는 가까운 역</li>
          <li>희망 날짜와 시간</li>
          <li>위치 유형(아파트 단지·오피스텔·주택 등)</li>
        </ul>
        <h2>운영 안내</h2>
        <p>전화 연결이 어려운 시간에는 잠시 후 다시 시도해 주시면 순차적으로 안내해 드립니다. 예약 변경·취소는 가능한 빨리 알려주시면 원활하게 조정됩니다.</p>
        """,
        extra_kw="고객센터, 출장마사지 문의",
    )

    # 5) 개인정보 처리방침
    simple_page(
        ["privacy"], "/privacy/",
        "개인정보 처리방침｜GUGU 마사지",
        "서울 출장마사지·홈타이 예약 과정의 개인정보 수집·이용·보유 기준을 안내합니다.",
        [("서울 출장마사지", H), ("개인정보 처리방침", "/privacy/")],
        f"""
        <p class="muted">최종 수정일: {esc(SITE['updated_label'])}</p>
        <h2>1. 수집하는 개인정보 항목</h2>
        <p>{esc(SITE['brand'])}는 예약 안내를 위해 필요한 최소한의 정보만 수집합니다. 전화 예약 과정에서 연락처, 방문 희망 지역·시간, 위치 정보가 안내 목적으로 확인될 수 있습니다.</p>
        <h2>2. 개인정보의 이용 목적</h2>
        <ul>
          <li>예약 접수 및 방문 가능 여부 안내</li>
          <li>예약 변경·취소 등 고객 문의 응대</li>
          <li>서비스 제공을 위한 위치·시간 확인</li>
        </ul>
        <h2>3. 보유 및 이용 기간</h2>
        <p>수집된 정보는 예약 안내 목적이 달성되면 지체 없이 파기하며, 관련 법령에서 보관을 요구하는 경우 해당 기간 동안만 보관합니다.</p>
        <h2>4. 제3자 제공</h2>
        <p>이용자의 동의 없이 개인정보를 외부에 제공하지 않습니다. 다만 법령에 따른 요청이 있는 경우 관련 절차에 따릅니다.</p>
        <h2>5. 이용자의 권리</h2>
        <p>이용자는 본인 정보의 열람·정정·삭제를 요청할 수 있으며, 요청 시 지체 없이 처리합니다. 관련 문의는 <a href="/support/">고객센터</a>로 연락하시면 됩니다.</p>
        <h2>6. 안전성 확보 조치</h2>
        <p>수집된 정보가 분실·도난·유출되지 않도록 합리적인 관리적·기술적 보호 조치를 취합니다.</p>
        """,
        extra_kw="개인정보 처리방침",
    )


# --------------------------------------------------------------------- #
# 루트 리다이렉트 + sitemap + robots                                     #
# --------------------------------------------------------------------- #
def render_root_redirect():
    canonical = BASE + "/seoul-chuljangmassage/"
    content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>서울 출장마사지｜25개 자치구 홈타이 지역별 예약 안내</title>
<meta name="description" content="서울 출장마사지·홈타이 예약 전 자치구, 행정동, 역세권 정보를 확인하세요.">
<link rel="canonical" href="{esc(canonical)}">
<meta http-equiv="refresh" content="0; url=/seoul-chuljangmassage/">
</head>
<body>
<p><a href="/seoul-chuljangmassage/">서울 출장마사지 메인으로 이동</a></p>
<script>location.replace("/seoul-chuljangmassage/");</script>
</body>
</html>"""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(content)


def render_sitemap():
    urls = ["/seoul-chuljangmassage/"]
    urls += [district_url(d["slug"]) for d in DISTRICTS]
    urls += [g["url"] for g in GUIDE_PAGES]
    items = "".join(
        f"<url><loc>{esc(BASE + u)}</loc><lastmod>{SITE['updated']}</lastmod>"
        f"<changefreq>weekly</changefreq><priority>{'1.0' if u=='/seoul-chuljangmassage/' else '0.8'}</priority></url>"
        for u in urls
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>\n'
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def render_robots():
    txt = f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n"
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(txt)


def render_cloudflare():
    # 루트는 메인으로 302 (HTML 플래시 없는 깔끔한 리다이렉트)
    redirects = "/    /seoul-chuljangmassage/    302\n"
    with open(os.path.join(ROOT, "_redirects"), "w", encoding="utf-8") as f:
        f.write(redirects)
    # 정적 자산 장기 캐시 + 기본 보안 헤더
    headers = (
        "/assets/*\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
    )
    with open(os.path.join(ROOT, "_headers"), "w", encoding="utf-8") as f:
        f.write(headers)


# --------------------------------------------------------------------- #
def clean():
    for p in ["seoul-chuljangmassage", "seoul", "guide", "support", "privacy"]:
        fp = os.path.join(ROOT, p)
        if os.path.isdir(fp):
            shutil.rmtree(fp)


def main():
    clean()
    render_main()
    for d in DISTRICTS:
        render_district(d)
    render_guides()
    render_root_redirect()
    render_sitemap()
    render_robots()
    render_cloudflare()
    total = 1 + len(DISTRICTS) + len(GUIDE_PAGES)
    print(f"빌드 완료: 메인 1 + 자치구 {len(DISTRICTS)} + 안내 {len(GUIDE_PAGES)} = 총 {total}개 페이지")


if __name__ == "__main__":
    main()
