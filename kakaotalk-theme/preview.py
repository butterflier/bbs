# -*- coding: utf-8 -*-
"""테마 두 벌의 미리보기 한 장을 그린다.

    python3 kakaotalk-theme/preview.py

카카오톡 화면을 흉내 낸 그림일 뿐, 실제 앱 렌더링은 아니다.
build.py 가 만든 Images/ 의 말풍선·탭아이콘·프로필을 그대로 갖다 쓰므로
색과 모양이 어긋나면 여기서 먼저 보인다.
"""
import os

from PIL import Image, ImageDraw, ImageFont

import build

ROOT = build.ROOT
FONTS = os.path.join(ROOT, 'assets', 'fonts')

W, H = 420, 760          # 화면 한 벌 크기
GAP = 32


def font(size, bold=False):
    name = 'Paperlogy-7Bold.ttf' if bold else 'Paperlogy-4Regular.ttf'
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def img2x(key, name):
    return Image.open(os.path.join(ROOT, 'build-src', key, 'Images', name)).convert('RGBA')


def stretch(bub, w, h):
    """cap inset 대로 9조각 늘리기. 카톡이 말풍선을 늘리는 방식과 같다."""
    # 들어온 그림은 @2x 다. 1x 로 줄여 놓고 pt 단위 cap 을 그대로 쓴다
    bub = bub.resize((build.BUBBLE_SIZE, build.BUBBLE_SIZE), Image.LANCZOS)
    cap = build.CAP
    s = bub.size[0]
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    xs = [(0, cap, 0, cap), (cap, s - cap, cap, w - cap), (s - cap, s, w - cap, w)]
    ys = [(0, cap, 0, cap), (cap, s - cap, cap, h - cap), (s - cap, s, h - cap, h)]
    for sx0, sx1, dx0, dx1 in xs:
        for sy0, sy1, dy0, dy1 in ys:
            if dx1 <= dx0 or dy1 <= dy0:
                continue
            piece = bub.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS)
            out.paste(piece, (dx0, dy0), piece)
    return out


CHAT = [
    ('recv', '마루', '이번 주 수업 일정 올렸습니다'),
    ('recv', '마루', '9/22 숙제 제출 9번이에요'),
    ('send', None, '확인했습니다'),
    ('send', None, '피드백은 9/22~24 이어서 진행할게요'),
    ('recv', '마루', '넵 감사합니다'),
]


def screen(key, t):
    px = lambda c: build.rgba(c)
    im = Image.new('RGBA', (W, H), px(t['bg_deep']))
    d = ImageDraw.Draw(im)

    # 상단 제목줄
    d.rectangle((0, 0, W, 64), fill=px(t['surface']))
    d.line((0, 64, W, 64), fill=px(t['border']), width=1)
    d.text((20, 22), '소논문반 27기', font=font(19, True), fill=px(t['text']))
    d.text((W - 20, 25), '24', font=font(14), fill=px(t['subtext']), anchor='ra')

    # 말풍선
    bub = {s: {v: img2x(key, 'chatroomBubble%s%s@2x.png' % (s, v)) for v in ('01', '02')}
           for s in ('Send', 'Receive')}
    f = font(15)
    y = 84
    for side, who, text in CHAT:
        tw = d.textlength(text, font=f)
        bw, bh = int(tw) + build.INSET_H * 2, 15 + build.INSET_V * 2
        if side == 'recv':
            # 기본 프로필 그림을 실제로 써서 동그랗게 자른 모습을 확인한다
            pf = img2x(key, 'profileImg01@2x.png').resize((36, 36), Image.LANCZOS)
            mask = Image.new('L', (36, 36), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, 35, 35), fill=255)
            im.paste(pf, (16, y), mask)
            d.text((70, y - 2), who, font=font(12), fill=px(t['subtext']))
            x = 70
            body = stretch(bub['Receive']['01'], bw, bh)
            ink, ty = t['recv_text'], y + 16
        else:
            x = W - 16 - bw
            body = stretch(bub['Send']['01'], bw, bh)
            ink, ty = t['send_text'], y
        im.paste(body, (x, ty), body)
        d.text((x + build.INSET_H, ty + build.INSET_V), text, font=f, fill=px(ink))
        y = ty + bh + 14

    # 입력바
    bar = H - 120
    d.rectangle((0, bar, W, H - 56), fill=px(t['surface']))
    d.line((0, bar, W, bar), fill=px(t['border']), width=1)
    d.text((22, bar + 20), '메시지 입력', font=font(14), fill=px(t['subtext']))
    d.rounded_rectangle((W - 62, bar + 12, W - 18, bar + 44), radius=4, fill=px(t['accent']))
    d.line((W - 50, bar + 28, W - 30, bar + 28), fill=px(t['on_accent']), width=2)
    d.line((W - 38, bar + 20, W - 30, bar + 28), fill=px(t['on_accent']), width=2)
    d.line((W - 38, bar + 36, W - 30, bar + 28), fill=px(t['on_accent']), width=2)

    # 탭바
    d.rectangle((0, H - 56, W, H), fill=px(t['surface']))
    d.line((0, H - 56, W, H - 56), fill=px(t['border']), width=1)
    for i, kind in enumerate(build.TAB_KINDS[:5]):
        name = 'maintabIco' + kind.capitalize() + ('Selected' if i == 1 else '') + '@2x.png'
        ico = img2x(key, name).resize((26, 26), Image.LANCZOS)
        im.paste(ico, (int((i + 0.5) * W / 5) - 13, H - 42), ico)
    return im


def main():
    shots = [(k, build.PALETTES[k]) for k in build.PALETTES]
    head = 92
    sheet = Image.new('RGBA', (W * len(shots) + GAP * (len(shots) + 1),
                               H + head + GAP), (250, 250, 250, 255))
    d = ImageDraw.Draw(sheet)
    d.text((GAP, 28), 'jyugyo_pink · iOS 카카오톡 테마', font=font(24, True), fill=(32, 40, 51, 255))
    for i, (key, t) in enumerate(shots):
        x = GAP + i * (W + GAP)
        ico = Image.open(os.path.join(ROOT, 'build-src', key, 'Images',
                                      'commonIcoTheme.png')).convert('RGBA')
        ico = ico.resize((28, 28), Image.LANCZOS)
        sheet.paste(ico, (x, head - 34), ico)
        d.text((x + 38, head - 32), t['name'], font=font(15, True), fill=(32, 40, 51, 255))
        sheet.paste(screen(key, t), (x, head))
        d.rectangle((x, head, x + W - 1, head + H - 1), outline=(222, 226, 231, 255), width=1)
    out = os.path.join(ROOT, 'assets', 'preview.png')
    sheet.convert('RGB').save(out)
    print(out)


if __name__ == '__main__':
    main()
