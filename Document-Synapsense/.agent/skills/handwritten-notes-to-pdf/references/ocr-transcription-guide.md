# Transcribing Handwriting Accurately

The goal is not "produce text that looks plausible." It's "produce text
that is either correct or clearly flagged as uncertain."

## Core technique

1. **Read once for structure, then again for content.** First pass:
   identify headings, numbered items, paragraphs, diagrams, and formulas
   on the page and their layout. Second pass: transcribe content into
   that structure. Trying to do both at once is where line-skipping and
   merged-paragraph errors come from.

2. **Use subject context aggressively.** If the user told you this page
   is, say, thermodynamics or organic chemistry, use that domain's
   vocabulary to resolve ambiguous letters/words (e.g., a scrawled word
   that could be "entropy" or "enthalpy" — subject context plus
   surrounding symbols usually settles it). Don't transcribe in a
   vacuum if you have subject info available — ask for it if you don't
   and the page is ambiguous.

3. **Never silently resolve genuine ambiguity.** If a word could
   plausibly be two different things and context doesn't settle it,
   write `[unclear: option-you-lean-toward]` inline rather than picking
   silently. This is the single highest-value habit for exam material —
   a silent wrong guess is worse than no answer, because the student
   will trust it.

4. **Treat these as their own categories, not prose:**
   - **Math/formulas** — transcribe as LaTeX (`$...$` / `$$...$$`) so
     symbols, subscripts, and exponents survive. If a symbol is
     genuinely ambiguous (e.g., could be a variable "v" or a check
     mark), flag it rather than picking.
   - **Diagrams/sketches** — don't try to force them into text. Either
     describe them briefly in brackets (`[diagram: labeled free-body
     diagram, forces F1 up, F2 right]`) and note that the original
     image should be embedded, or embed the (cropped) image itself in
     the PDF — see `references/pdf-assembly-qa.md`.
   - **Tables** — reconstruct as an actual table (markdown or PDF
     table), not as run-on prose. Preserve row/column alignment as the
     student drew it.
   - **Strikethroughs / corrections** — transcribe the *final* intended
     version by default (what the student corrected *to*), not the
     crossed-out version, unless the crossed-out part is clearly still
     relevant (e.g., "wrong approach, don't repeat").

5. **Cross-check numbers and signs specifically.** Digits and +/−/×/÷
   signs are the most consequential errors and the easiest to
   misread (a 7 vs 1, a minus sign vs a dash, a decimal point vs a
   stray mark). Give these a dedicated second look in the self-check
   pass from SKILL.md step 4 — don't rely on the first read.

6. **Don't "improve" the student's wording.** Transcribe what's there,
   including their own shorthand and abbreviations, unless it's
   genuinely illegible — the point is faithful capture, not editing.

## Confidence flagging convention

Use one consistent marker so the final list in SKILL.md step 6 can be
generated automatically by scanning for it:

```
[unclear: your best guess]
```

Don't invent multiple different flagging styles across pages — this
makes the final "please confirm these" list harder to compile and
easier for the student to miss items in.
