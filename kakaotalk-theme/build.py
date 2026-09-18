# -*- coding: utf-8 -*-
"""TIS 교사 페이지 디자인을 그대로 옮긴 iOS 카카오톡 테마를 만든다.

    python3 kakaotalk-theme/build.py

결과는 kakaotalk-theme/dist/*.ktheme (zip 의 확장자만 바꾼 것).
색은 아래 PALETTES 한 곳에만 있다 — 다른 데를 고칠 필요가 없다.

색 출처
  말풍선과 글자색은 참고 스크린샷에서 직접 뽑았다 —
  말풍선 바탕 #FBE8F1, 글자·테두리 #C86B95, 받은쪽 흰 바탕,
  제목 #191919, 보조글 #BEA3B0, 눌린 줄 #FCEDF3.

그림자·그라데이션·일러스트는 여전히 쓰지 않는다. 평평한 단색 말풍선이다.
"""
import os
import zipfile

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, 'dist')

VERSION = '1.0.0'

# 말풍선 기하 (pt). CAP 은 CSS 의 cap inset 과 반드시 같아야 한다.
# 모서리 4pt — 스크린샷은 훨씬 둥글지만 각진 쪽으로 쓰기로 정했다.
BUBBLE_SIZE, BUBBLE_RADIUS, CAP = 28, 4, 10
INSET_V, INSET_H = 9, 14          # 글자와 말풍선 사이 여백 (pt)

TAB_KINDS = ('friends', 'chats', 'browse', 'find', 'piccoma', 'shopping', 'more')
BULLET_SLOTS = ('first', 'second', 'third', 'fourth')


# --- 팔레트 --------------------------------------------------------------

PALETTES = {
    'jyugyo_pink': {
        'name': 'jyugyo_pink',
        'pkg': 'tis.jyugyo.pink',

        'bg':        '#FFFFFF',   # 목록 배경
        'surface':   '#FFFFFF',   # 입력바·알림배너
        'bg_deep':   '#FFFFFF',   # 채팅방 바닥 (스크린샷도 흰 바탕)
        'pressed':   '#FCEDF3',   # 눌린 줄 — 스크린샷 별무늬 분홍
        'border':    '#F5DCE8',   # 구분선

        'text':      '#191919',   # 제목·이름   (스크린샷 헤더)
        'subtext':   '#BEA3B0',   # 보조글      (스크린샷 입력창 안내문)
        'accent':    '#C86B95',   # 포인트      (스크린샷 말풍선 글자)
        'tab_normal': '#B792A3',  # 선택 안 된 탭 아이콘 (보조글색은 흰 바탕에서 너무 흐리다)
        'accent_dim': '#B05780',
        'on_accent': '#FFFFFF',

        # 말풍선 — 보낸쪽은 로즈색 단색에 흰 글자, 받은쪽은 흰 바탕에 로즈색 테두리·글자
        'send':       ('#C86B95', None),
        'send_alt':   ('#B05780', None),
        'send_text':  '#FFFFFF',
        'recv':       ('#FFFFFF', '#C86B95'),
        'recv_alt':   ('#FDF5F9', '#C86B95'),
        'recv_text':  '#C86B95',

        # 기본 프로필 3장 / 잠금화면 동그라미 4자리
        'profiles': ('#FBE8F1', '#F6D3E3', '#EFBCD5'),
        'profile_ink': '#C86B95',
        'bullets':  ('#C86B95', '#D98CAE', '#E7A9C4', '#B05780'),
        'bullet_empty': '#F0D8E4',

        'chips': ('#FBE8F1', '#F6D3E3', '#EFBCD5', '#E7A3C7'),
        'icon_bg': '#FFFFFF',
    },
    'jyugyo_pink_dark': {
        'name': 'jyugyo_pink dark',
        'pkg': 'tis.jyugyo.pink.dark',

        'bg':        '#161315',
        'surface':   '#1D1A1C',
        'bg_deep':   '#1D1A1C',
        'pressed':   '#2A2429',
        'border':    '#3A3238',

        'text':      '#F3ECEF',
        'subtext':   '#A8949E',
        'accent':    '#E48FB4',
        'tab_normal': '#A8949E',
        'accent_dim': '#C56F95',
        'on_accent': '#161315',

        # 다크는 테두리색 #E48FB4 을 그대로 채우면 흰 글자가 안 읽힌다(대비 2.0).
        # 한 단계 짙은 #C56F95 로 채워 흰 글자 대비를 3.7 까지 올린다.
        'send':       ('#C56F95', None),
        'send_alt':   ('#AE5C81', None),
        'send_text':  '#FFFFFF',
        'recv':       ('#1D1A1C', '#E48FB4'),
        'recv_alt':   ('#262023', '#E48FB4'),
        'recv_text':  '#F6D9E6',

        'profiles': ('#3A2430', '#4A2E3C', '#5A3848'),
        'profile_ink': '#E48FB4',
        'bullets':  ('#E48FB4', '#C56F95', '#EFAECB', '#A85B7E'),
        'bullet_empty': '#3A3238',

        'chips': ('#3A2430', '#4A2E3C', '#5A3848', '#6B4256'),
        'icon_bg': '#1D1A1C',
    },
}


def rgba(hexstr, alpha=255):
    h = hexstr.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), alpha)


def canvas(px):
    return Image.new('RGBA', (px, px), (0, 0, 0, 0))


# --- 말풍선 --------------------------------------------------------------

def bubble(scale, fill, stroke):
    """평평한 말풍선 한 장. 그라데이션도 그림자도 없다 — 디자인 규칙대로."""
    px = BUBBLE_SIZE * scale
    img = canvas(px)
    d = ImageDraw.Draw(img)
    w = scale  # 1pt 테두리
    box = (0, 0, px - 1, px - 1)
    if stroke:
        # 테두리가 잘리지 않도록 반 픽셀 안쪽에서 그린다
        box = (w // 2, w // 2, px - 1 - w // 2, px - 1 - w // 2)
    d.rounded_rectangle(box, radius=BUBBLE_RADIUS * scale,
                        fill=rgba(fill),
                        outline=rgba(stroke) if stroke else None,
                        width=w if stroke else 0)
    return img


# --- 탭 아이콘 -----------------------------------------------------------

def tab_icon(kind, px, color):
    """선으로만 그린 탭 아이콘. 채우기 없이 같은 굵기를 유지한다."""
    img = canvas(px)
    d = ImageDraw.Draw(img)
    c = rgba(color)
    u = px / 28.0                 # 1pt
    lw = max(1, round(2 * u))
    r = max(1, round(3 * u))      # 모서리

    def box(x0, y0, x1, y1, radius=None, fill=None):
        d.rounded_rectangle((x0 * u, y0 * u, x1 * u, y1 * u),
                            radius=(radius if radius is not None else 3) * u,
                            outline=c if fill is None else None,
                            fill=fill, width=lw)

    if kind == 'friends':
        d.ellipse((10 * u, 5 * u, 18 * u, 13 * u), outline=c, width=lw)
        d.arc((5 * u, 14 * u, 23 * u, 30 * u), 180, 360, fill=c, width=lw)
    elif kind == 'chats':
        box(4, 6, 24, 19)
        d.line((9 * u, 19 * u, 9 * u, 24 * u), fill=c, width=lw)
        d.line((9 * u, 24 * u, 15 * u, 19 * u), fill=c, width=lw)
    elif kind == 'browse':
        for x in (4, 16):
            for y in (4, 16):
                box(x, y, x + 8, y + 8, radius=2)
    elif kind == 'find':
        d.ellipse((5 * u, 5 * u, 19 * u, 19 * u), outline=c, width=lw)
        d.line((18 * u, 18 * u, 24 * u, 24 * u), fill=c, width=lw)
    elif kind == 'piccoma':
        box(5, 5, 23, 23, radius=2)
        d.line((14 * u, 5 * u, 14 * u, 23 * u), fill=c, width=lw)
    elif kind == 'shopping':
        box(5, 9, 23, 24, radius=2)
        d.arc((9 * u, 3 * u, 19 * u, 15 * u), 180, 360, fill=c, width=lw)
    elif kind == 'more':
        for y in (8, 14, 20):
            d.line((6 * u, y * u, 22 * u, y * u), fill=c, width=lw)
    return img


# --- 그 밖의 이미지 ------------------------------------------------------

def theme_icon(t, px):
    """테마 목록에 보이는 썸네일. 달력의 일정 블록을 그대로 축소한 모양."""
    img = Image.new('RGBA', (px, px), rgba(t['icon_bg']))
    d = ImageDraw.Draw(img)
    u = px / 162.0
    r = 4 * u
    # 구분선 두 줄 + 색 블록 네 개 = 주간 달력의 인상
    for i, col in enumerate(t['chips']):
        y = (30 + i * 28) * u
        d.rounded_rectangle((26 * u, y, 136 * u, y + 20 * u), radius=r, fill=rgba(col))
    d.line((26 * u, 22 * u, 136 * u, 22 * u), fill=rgba(t['border']), width=max(1, round(1.4 * u)))
    return img


def profile_image(t, i, px):
    """기본 프로필. 일정 블록 색 위에 사람 실루엣 하나."""
    img = Image.new('RGBA', (px, px), rgba(t['profiles'][i]))
    d = ImageDraw.Draw(img)
    u = px / 108.0
    ink = rgba(t['profile_ink'])
    d.ellipse((40 * u, 28 * u, 68 * u, 56 * u), fill=ink)
    d.rounded_rectangle((28 * u, 64 * u, 80 * u, 104 * u), radius=20 * u, fill=ink)
    return img


def bullet_image(t, i, px, filled):
    """잠금화면 동그라미. 자리마다 일정 블록 색을 하나씩 쓴다."""
    img = canvas(px)
    d = ImageDraw.Draw(img)
    u = px / 18.0
    pad = 2 * u
    box = (pad, pad, px - 1 - pad, px - 1 - pad)
    if filled:
        d.ellipse(box, fill=rgba(t['bullets'][i]))
    else:
        d.ellipse(box, outline=rgba(t['bullet_empty']), width=max(1, round(1.5 * u)))
    return img


def keypad_pressed(t, px):
    img = canvas(px)
    ImageDraw.Draw(img).rectangle((0, 0, px - 1, px - 1), fill=rgba(t['pressed']))
    return img


def add_friend_icon(t, px):
    """친구추가 단추. 포인트색 사각에 흰 +."""
    img = canvas(px)
    d = ImageDraw.Draw(img)
    u = px / 24.0
    d.rounded_rectangle((0, 0, px - 1, px - 1), radius=4 * u, fill=rgba(t['accent']))
    lw = max(1, round(2 * u))
    d.line((7 * u, 12 * u, 17 * u, 12 * u), fill=rgba(t['on_accent']), width=lw)
    d.line((12 * u, 7 * u, 12 * u, 17 * u), fill=rgba(t['on_accent']), width=lw)
    return img


# --- CSS -----------------------------------------------------------------

CSS = """/*
 {name} — iOS 카카오톡 테마

 이 파일은 kakaotalk-theme/build.py 가 만든다. 직접 고치지 말 것.
 색을 바꾸려면 build.py 의 PALETTES 를 고치고 다시 돌린다.

 색 출처: TIS 교사 페이지 심플컬러 시안 + jyugyo_calendar 일정 블록 색.
 지정하지 않은 항목은 카카오 기본 테마가 그대로 보인다.
 iOS 테마는 글꼴을 바꿀 수 없다 — Paperlogy 는 적용되지 않는다.
*/

ManifestStyle
{{
    -kakaotalk-theme-name: '{name}';
    -kakaotalk-theme-version: '{version}';
    -kakaotalk-author-name: 'TIS';
    -kakaotalk-theme-id: 'com.kakao.talk.theme.{pkg}';
}}

TabBarStyle-Main
{{
    background-color: {surface};
{tabicons}}}

HeaderStyle-Main
{{
    -ios-text-color: {text};
    -ios-tab-text-color: {subtext};
    -ios-tab-highlighted-text-color: {accent};
}}

/* 친구탭 · 채팅목록 */
MainViewStyle-Primary
{{
    background-color: {bg};

    -ios-text-color: {text};
    -ios-highlighted-text-color: {text};

    -ios-description-text-color: {subtext};
    -ios-description-highlighted-text-color: {subtext};

    -ios-paragraph-text-color: {subtext};
    -ios-paragraph-highlighted-text-color: {subtext};

    -ios-normal-background-color: {bg};
    -ios-normal-background-alpha: 1.00;
    -ios-selected-background-color: {pressed};
    -ios-selected-background-alpha: 1.00;
}}

MainViewStyle-Secondary
{{
    background-color: {surface};
}}

SectionTitleStyle-Main
{{
    border-color: {border};
    border-alpha: 1.0;
    -ios-text-color: {subtext};
    -ios-text-alpha: 1.0;
}}

FeatureStyle-Primary
{{
    -ios-text-color: {accent};
}}

ButtonStyle-AddFriend
{{
    -ios-image: 'findBtnAddFriend.png';
}}

DefaultProfileStyle
{{
    -ios-profile-images: {profiles};
}}

BackgroundStyle-ChatRoom
{{
    background-color: {bg_deep};
}}

InputBarStyle-Chat
{{
    background-color: {surface};

    -ios-send-normal-background-color: {accent};
    -ios-send-normal-foreground-color: {on_accent};
    -ios-send-highlighted-background-color: {accent_dim};
    -ios-send-highlighted-foreground-color: {on_accent};

    -ios-button-normal-foreground-color: {subtext};
    -ios-button-highlighted-foreground-color: {accent};
}}

/*
 말풍선은 색 속성이 없고 PNG 로만 지정한다.
 뒤의 숫자 두 개는 늘어나지 않는 가장자리(cap inset)이고 build.py 의 CAP 과 같아야 한다.
 edgeinsets 는 글자와 말풍선 사이 여백이다.
*/
MessageCellStyle-Send
{{
{send_cells}

    -ios-text-color: {send_text};
    -ios-selected-text-color: {send_text};
    -ios-unread-text-color: {accent};
}}

MessageCellStyle-Receive
{{
{recv_cells}

    -ios-text-color: {recv_text};
    -ios-selected-text-color: {recv_text};
    -ios-unread-text-color: {accent};
}}

BackgroundStyle-Passcode
{{
    background-color: {bg};
}}

LabelStyle-PasscodeTitle
{{
    -ios-text-color: {text};
}}

PasscodeStyle
{{
    -ios-keypad-background-color: {surface};
    -ios-keypad-text-normal-color: {text};
    -ios-keypad-number-highlighted-image: 'passcodeKeypadPressed.png';
{bullet_lines}}}

BackgroundStyle-MessageNotificationBar
{{
    background-color: {surface};
}}

LabelStyle-MessageNotificationBarName
{{
    -ios-text-color: {text};
}}

LabelStyle-MessageNotificationBarMessage
{{
    -ios-text-color: {subtext};
}}

BackgroundStyle-DirectShareBar
{{
    background-color: {surface};
}}

LabelStyle-DirectShareBarName
{{
    -ios-text-color: {text};
}}

LabelStyle-DirectShareBarMessage
{{
    -ios-text-color: {subtext};
}}

BottomBannerStyle
{{
    background-color: {surface};
}}
"""


def cell_css(side):
    """MessageCellStyle 의 말풍선 그림 네 자리와 글자 여백."""
    name = 'chatroomBubble' + side
    ins = '%dpx %dpx %dpx %dpx' % (INSET_V, INSET_H, INSET_V, INSET_H)
    props = ('-ios-background-image', '-ios-selected-background-image',
             '-ios-group-background-image', '-ios-group-selected-background-image')
    variants = ('01', '02', '02', '01')
    lines = ["    %s: '%s%s.png' %dpx %dpx;" % (p, name, v, CAP, CAP)
             for p, v in zip(props, variants)]
    lines += ['', '    -ios-title-edgeinsets: %s;' % ins,
              '    -ios-group-title-edgeinsets: %s;' % ins]
    return '\n'.join(lines)


# --- 빌드 ----------------------------------------------------------------

def build(key, t):
    src = os.path.join(ROOT, 'build-src', key)
    img_dir = os.path.join(src, 'Images')
    os.makedirs(img_dir, exist_ok=True)
    out = lambda n: os.path.join(img_dir, n)

    # 말풍선 — 보낸/받은 × 01(보통·눌림) / 02(그룹)
    for side, base in (('Send', 'send'), ('Receive', 'recv')):
        for variant, pal_key in (('01', base), ('02', base + '_alt')):
            fill, stroke = t[pal_key]
            for scale in (2, 3):
                bubble(scale, fill, stroke).save(
                    out('chatroomBubble%s%s@%dx.png' % (side, variant, scale)))

    # 테마 썸네일 162x162
    theme_icon(t, 162).save(out('commonIcoTheme.png'))

    # 탭 아이콘 7종 × 보통/선택
    tab_lines = []
    for kind in TAB_KINDS:
        name = 'maintabIco' + kind.capitalize()
        for suffix, col in (('', t['tab_normal']), ('Selected', t['accent'])):
            for scale in (2, 3):
                tab_icon(kind, 28 * scale, col).save(
                    out('%s%s@%dx.png' % (name, suffix, scale)))
        tab_lines.append("    -ios-%s-normal-icon-image: '%s.png';" % (kind, name))
        tab_lines.append("    -ios-%s-selected-icon-image: '%sSelected.png';" % (kind, name))

    # 친구추가 단추 (iOS 는 눌린 그림 자리가 없어 한 장)
    for scale in (2, 3):
        add_friend_icon(t, 24 * scale).save(out('findBtnAddFriend@%dx.png' % scale))

    # 잠금화면
    for scale in (2, 3):
        keypad_pressed(t, 64 * scale).save(out('passcodeKeypadPressed@%dx.png' % scale))
    bullet_lines = []
    for i, slot in enumerate(BULLET_SLOTS):
        nm = 'passcodeImgCode%02d' % (i + 1)
        for scale in (2, 3):
            bullet_image(t, i, 18 * scale, False).save(out('%s@%dx.png' % (nm, scale)))
            bullet_image(t, i, 18 * scale, True).save(out('%sSelected@%dx.png' % (nm, scale)))
        bullet_lines.append("    -ios-bullet-%s-image: '%s.png';" % (slot, nm))
        bullet_lines.append("    -ios-bullet-selected-%s-image: '%sSelected.png';" % (slot, nm))

    # 기본 프로필 3장
    names = []
    for i in range(3):
        nm = 'profileImg%02d' % (i + 1)
        for scale in (2, 3):
            profile_image(t, i, 54 * scale).save(out('%s@%dx.png' % (nm, scale)))
        names.append("'%s.png'" % nm)

    css = CSS.format(version=VERSION,
                     send_cells=cell_css('Send'), recv_cells=cell_css('Receive'),
                     tabicons='\n'.join(tab_lines) + '\n',
                     bullet_lines='\n'.join(bullet_lines) + '\n',
                     profiles=' '.join(names),
                     **{k: v for k, v in t.items()
                        if isinstance(v, str)})
    with open(os.path.join(src, 'KakaoTalkTheme.css'), 'w',
              encoding='utf-8', newline='\n') as f:
        f.write(css)

    # 포장 — zip 의 확장자만 .ktheme 으로 바꾼 것
    os.makedirs(DIST, exist_ok=True)
    pkg = os.path.join(DIST, key + '.ktheme')
    with zipfile.ZipFile(pkg, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(src):
            for fn in sorted(files):
                p = os.path.join(base, fn)
                z.write(p, os.path.relpath(p, src))
    n = len(os.listdir(img_dir))
    print('%-22s 이미지 %3d장  %6.1f KB  %s' % (key, n, os.path.getsize(pkg) / 1024, pkg))


if __name__ == '__main__':
    for key, t in PALETTES.items():
        build(key, t)
