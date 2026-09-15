# Channel logo prompts — transparent-alpha wordmark + icon (gpt-image-2.5)

Ported 2026-09-15 from `~/pet-projects/suno-music-gen/.claude/rules/channel-logo-prompts.md`
(originally distilled from OpenAI's gpt-image-2.5 image-prompting guide). Grammar for
generating a channel's **logo asset** — a clean wordmark and/or icon on a fully
transparent background — distinct from the round social avatar (filled circle) and the
in-video watermark bug (`pipeline/plates.py`'s `bug()`, already locked).

## Why gpt-image-2.5 for logos specifically

- **True transparent background with clean alpha edges** — a real cutout, not a
  white/black square to key out. Request PNG/WebP with alpha.
- **Higher text accuracy**, including small lettering, when the wording is quoted
  verbatim and `quality` is pushed to `high`/`xhigh`.

In the API it's `gpt-image-2.5`, two tiers: **Flare** (fast) and **Sunburst** (best
quality). Use the quality tier for anything with legible text. Through Higgsfield it
appears as its GPT Image family — request the transparent-background option explicitly
and verify the alpha actually came back (see gate below).

## Hard rules

- **This is the one place a "no text" ban inverts.** The wordmark IS the image: spell
  it out verbatim in quotes, and close with `no extra text, no watermarks, no extra
  glyphs` — that forbids *stray* text, not the wordmark itself.
- **Wordmark verbatim, in quotes.** For this channel: `"WEIRD NEWS"` / `"USA"` exactly
  as locked in `channel/branding.md`.
- **`rendered exactly once, no doubled or ghosted text`** — a logo with a ghosted
  second copy is dead.
- **Transparent background, stated explicitly**: `fully transparent background, clean
  alpha edges, the mark centred with generous even padding`. No scene, no ground, no
  panel, no drop-shadow baked onto transparency (shadows on alpha read as grey haze).
- **Scalable/flat discipline**: clean shapes, negative space, `flat design, minimal
  strokes, no gradients unless essential`. Must survive 24px (favicon/avatar-adjacent)
  and read at banner size.
- **Match the locked palette**: near-black #0B0B0D, accent red #D6202A, white #F5F5F5
  (from `channel/branding.md`).
- **No real politician's face on the logo/icon/avatar** — those are for real-clip
  thumbnails only (see `docs/seo-playbook.md` §4). The brand mark itself stays
  generic (magnifying glass, starburst, mic — never a likeness).

## Prompt structure

1. **Result + use** — "A channel logo / wordmark for Weird News USA, for use as a
   transparent overlay and watermark."
2. **The wordmark** — exact text in quotes, `rendered exactly once`, locked typography
   (bold white all-caps, two lines: WEIRD NEWS / USA).
3. **The icon** (optional) — the locked mark (magnifying glass over a melting US
   outline) as a small clean silhouette, same flat language as the avatar prompt.
4. **Palette + finish** — near-black/red/white; flat, high-contrast, scalable.
5. **Background + framing** — `fully transparent background, clean alpha edges,
   centred, generous even padding, square 1:1` (or `wide` for a horizontal lockmark).
6. **Constraints/close** — `Flat vector-clean logo, no gradients unless essential, no
   background, no photographic scene. Only the wordmark <and icon>; no extra text, no
   watermarks, no extra glyphs.`

Keep to `quality: high` (or `xhigh` only if small text comes back soft). Ask for PNG
(or WebP) with alpha.

## Variants to generate (a real logo kit, not one file)

- **Stacked mark** — icon above the two-line wordmark, square 1:1 (video intro,
  playlist cover).
- **Horizontal lockmark** — icon left, wordmark right, wide (end-card, lower-third).
- **Wordmark only** — no icon, for tight overlays.
- **Icon only, mono white** — the pure mark for a watermark (already exists as the
  avatar silhouette spec in `channel/branding.md` — reuse it).

## Ship gate

1. **Alpha is real.** Check on both a white and a black backing — genuinely
   transparent, clean edges, no grey halo, no baked square. If it came back on a
   solid ground, regenerate — don't hand-key it.
2. **Text is verbatim and single.** Every letter matches exactly, wordmark appears
   once. A dropped word or a ghosted second copy = reject and restate.
3. **24px survival** for the icon/stacked mark — shrink and look, same gate as the
   avatar in `channel/branding.md`.

Store the approved kit under `channel/logo/` in this repo, and note in
`channel/branding.md` which variant is canonical.
