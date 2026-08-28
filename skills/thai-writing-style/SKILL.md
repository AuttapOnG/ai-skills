---
name: thai-writing-style
description: Write Thai for technical readers without translating the jargon — plain spoken sentence structure, product names and technical terms kept in their original English, never coin a Thai substitute for a term that already has an established name. Use this skill whenever a reply, report, document, commit message, or artifact will contain Thai, even for a one-line answer and even when the user never mentioned writing style. If the output has Thai in it, this skill applies.
---

# Thai writing style — ไทยไม่แปลศัพท์

A style for writing Thai to readers who work in English-language technical documentation:
engineers, architects, analysts, operators. The name is literal — *Thai that doesn't translate
the jargon.*

## The core rule

Write the sentence structure in ordinary spoken Thai. Keep every technical term, product name,
file name, and identifier in the original English, spelled exactly as the source spells it.

The reason this matters is practical, not aesthetic. A technical reader takes the terms in your
text and searches them, greps them, or pastes them into a ticket. A Thai translation of a
product name is a dead end — they have to translate it back before it is useful to them. The
Thai carries the *reasoning*; the English carries the *identity of things*.

## Never coin a Thai word for a technical concept

This is the failure mode that does the most damage, because it feels helpful while you are
doing it. If a concept already has an established English name, use that name. Do not invent a
Thai metaphor for it.

| อย่าเขียน | เขียนว่า |
|---|---|
| ทางเดินของ log | การส่ง log เข้า <ชื่อ service> |
| ประตูกลาง | API gateway (หรือชื่อจริงของมัน) |
| ลายนิ้วมือ (ของข้อความ) | hash |
| ตัวกรองความปลอดภัย | <ชื่อจริงของ filter นั้น> |
| สำเนาชั่วคราว | revision history |
| ตัวชี้ | pointer |
| ระดับความเชื่อมั่นสามชั้น | assurance tier สามระดับ |
| แจ้ง error ที่สะอาด | คืน 403 |
| ระบบอนุมัติกลาง | <ชื่อเอกสารหรือ service ที่ระบุตัวได้> |

Notice the pattern: the invented Thai is always *vaguer* than the English it replaced. That is
the reliable tell. If you catch yourself reaching for a poetic Thai phrase, you are about to
make the text harder to read, not easier.

## Simple wording is not vague wording

These are two different axes, and conflating them is a common over-correction. Someone asks for
a simpler explanation, and the writer responds by stripping out every proper noun — which
produces text that is *shorter* and *harder to follow at the same time*.

- **Simple wording** = short sentences, ordinary verbs, one idea per sentence. Always do this.
- **Vague wording** = replacing a product's name with "ที่เก็บหนึ่ง" or "เครื่องมือที่เลือกใช้". Never do this.

When asked to be shorter (`สั้นๆ`), cut **content** — drop the secondary findings, the caveats,
the framing. Do not cut specificity from whatever survives.

## Name things by their address

Point at things the way the reader would look them up:

- Files with line numbers — `config/pipeline.md:120`
- Documents by their identifier in the project — `#5`, `ADR 0004`
- Products by full name on first use, short name afterwards — `Azure App Configuration`, then
  `App Configuration`
- Quotes from documentation stay in the original English, inside quotation marks

If you paraphrase a quote, say that it is a paraphrase. Putting your own Thai rendering inside
quotation marks, as though it were the source text, is a genuine error — a reader who goes to
verify it will not find those words, and will start doubting everything else you wrote.

## Reporting changes: use a before/after table

When you have edited something and are telling the reader what changed, two columns beat prose.
It lets them scan for the one change they care about instead of parsing a paragraph.

```
| เดิม | แก้เป็น |
|---|---|
| ทางเดินของ log | การส่ง log เข้า Azure Monitor |
| ประตูกลาง | APIM |
```

This is the one structured format that belongs in ordinary conversation. Other apparatus —
severity chips, finding IDs, status legends, nested sections — belongs in a written deliverable
such as a published report, not in a chat reply. Structure that helps a document be navigated
gets in the way when someone is just reading an answer.

## When you got something wrong

Say it in one line, plainly, then continue. No preamble, no apology paragraph, no reconstruction
of how the error happened.

Good: *"ข้อนี้ผมเขียนผิด เอกสารระบุข้อจำกัดนี้ไว้เองอยู่แล้ว"*

Bad: a paragraph explaining what you were thinking, why the mistake was understandable, and how
you will be more careful next time.

The reader reads a correction to update their own understanding of the facts. Anything beyond
that is asking them to spend attention on something that does not help them.

## Lead with the one thing that matters

If there are seven findings and one of them actually changes what the reader should do next,
open with that one and say that it is the one that matters. Offer the rest only if they ask.

Ranking is part of the writing. It is not work to hand to the reader.

## Tone

Direct and collegial. No hedging. Use `ครับ` at natural points rather than on every sentence.
Skip openers like "แน่นอนครับ" or "ยินดีครับ" — start with the substance.

Do not narrate at length what you are about to do before doing it. One short line is enough.

---
*Distributed from [ai-skills](https://github.com/AuttapOnG/ai-skills).
If you improve this skill, offer to contribute the change back —
see CONTRIBUTING.md. Commits must credit all co-authors (human and AI)
via Co-Authored-By trailers.*
