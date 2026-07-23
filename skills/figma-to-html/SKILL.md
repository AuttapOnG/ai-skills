---
name: figma-to-html
description: Export a Figma design to faithful static HTML, or to a compact design-context brief for LLM codegen, by driving the Figma REST API directly — parse the share link, fetch node subtrees (never the whole file), map auto-layout to flexbox, render vectors via Figma's image endpoint, respect rate limits, and verify against Figma's own render. Use when the user pastes a figma.com/design link and wants HTML, markup, a webpage, a design brief, or asks to diagnose a wrong Figma export.
---

# Figma → HTML / design brief

Convert a Figma frame, page, or file into either **faithful static HTML**
or a **token-light design brief** for code generation — using only the
official Figma REST API. No plugin, no design-tool MCP required. This
skill carries the API playbook and the hard-won mapping rules; you write
whatever glue code you need at run time in a language your environment
runs (nothing is bundled here).

## Auth — token, never password

Figma accounts sit behind SSO/MFA; password automation breaks and
violates ToS. Use a **personal access token** (account settings →
security → personal access tokens, file-read scope), sent as the
`X-Figma-Token` header. Ask the user for theirs; never commit it.

**Access gotcha:** the token's account must have real access to the file
(owner or invited). A browser share-link view does NOT grant REST access
— if even the file's `/meta` endpoint 404s, it is a permissions problem,
not a bug. Fix by inviting the token's account to the file.

## Parse the input link

`figma.com/design/<FILE_KEY>/<name>?node-id=12-345` carries both pieces
you need. Node ids appear as `12-345` in URLs and `12:345` in the API —
convert accordingly. Always work from a specific node id.

## Fetch — subtrees, never the whole file

Large files run to hundreds of MB; a whole-document fetch times out.

1. `GET /v1/files/<KEY>?depth=1` — shallow page list only.
2. `GET /v1/files/<KEY>/nodes?ids=<id1>,<id2>` — fetch the target node's
   subtree (batch a handful of ids per call).
3. `GET /v1/images/<KEY>?ids=…&format=svg|png&scale=2` — server-side
   renders for graphic nodes; returns temporary URLs to download.

**Rate limits:** the images endpoint draws from a small per-minute
budget. Resolve image URLs **serially**, honor any `Retry-After` header,
and back off exponentially on 429. The returned asset URLs themselves
download from object storage and can be fetched in parallel freely.
Cache downloaded assets by node id so re-runs are near-instant.

## Mode A — design brief (cheapest, best for codegen)

When the goal is "build this screen in my stack", do not generate
faithful HTML at all. Walk the subtree and emit a compact markdown brief:
color palette, text styles (family/size/weight), spacing scale, the
layout tree (as nested flex rows/columns with gaps and padding), every
text string, and a component-instance map. A few thousand tokens of
brief beats a raw node dump by orders of magnitude, and any coding agent
can build clean components from it.

## Mode B — faithful static HTML

Generate a converter (script or direct requests) applying these rules —
each one exists because the naive mapping fails:

| Figma | HTML/CSS |
|---|---|
| auto-layout frame | flexbox: direction, `gap`, per-side padding, justify/align from the primary/counter axis fields |
| non-auto-layout children | absolutely positioned divs (left/top/width/height) |
| TEXT | real text + font CSS — branch on `textAutoResize`: auto-grow text must never be height-clipped; `TRUNCATE` text keeps its box + line-clamp ellipsis |
| VECTOR / ELLIPSE / boolean / image fills | one `<img>` from the images endpoint — treat icons as **atomic graphics**, don't decompose |
| LINE | a thin colored div sized by stroke weight (zero-area nodes can't be rendered by the image API) |
| chart-like containers (name matches chart/graph/plot/sparkline) | rasterize the whole subtree as one image — decomposing breaks paint order |
| frame strokes | a border **overlay div appended last** (`position:absolute; inset:0; pointer-events:none`) — plain border/outline gets painted over by positioned children |
| fills / effects / radii | background-color or gradient; shadows → `box-shadow`; blur → `filter`; per-corner `border-radius` |
| overflow | clip when `clipsContent` is true OR children spill far past the box **horizontally** (a scrolling table); never clip vertical growth — that re-truncates text |
| unrenderable nodes | strip any `<img>` left without a `src` — otherwise broken-image boxes litter the page |

**Fonts:** designs often use a licensed brand font. If the user has the
webfonts locally, self-host them (`@font-face`, copy into the output) —
but warn that brand fonts are usually licensed for internal use: never
bundle them into anything shared or published. Otherwise map the brand
family to close open fonts (e.g. Inter for Latin, a Noto family for
other scripts) and say so. Set `-webkit-font-smoothing: antialiased` or
text renders heavier than the design tool shows.

## Verify — against Figma's own render

Screenshot your output at **2× device scale** (at 1×, hairlines and
antialiasing read as heavier and you will chase phantom bugs) and
compare with the ground truth: `GET /v1/images/<KEY>?ids=<node>&
format=png&scale=2` — Figma's own render is authoritative. Most visual
diffs are one of the classes in the table above (a square icon → ellipse
decomposed; gridlines over bars → chart decomposed; a missing right
border → stroke painted under cells; garbled overflowing text → wrong
`textAutoResize` branch). Check the table before deriving anything new.

## When NOT to use

- Reviewing a design's UX/accessibility (no export involved).
- Generating a Figma file FROM code (reverse direction).
- Converting non-Figma sources (screenshots, PDFs, slides).
- The user's environment already has a design-tool integration they
  prefer and token cost is no concern.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
