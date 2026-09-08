# Day 3 - Text To Image generation

## Goal

Given a reference image and a fixed SEED (70216), reconstruct a text prompt that reproduces the image as closely as possible using prompt conditioning on Z-Image Turbo.

## Approach

Since the SEED was fixed across all iterations, every change in the output image is attributable only to the prompt wording — not to random noise. This let me isolate individual visual features (setting, framing, camera angle, clothing color, mirroring) and refine them one at a time, comparing each output against the reference image before moving to the next detail.

## Iterative Process

### Iteration 1 — Establish the baseline scene
**Prompt:**
> "a smart girl using laptop in a cafe facing glass window, the sun light approaches to girl from window on his sweat shirt, girl wearing a black glasses, and facially girl looks Chinese had a black hairs with brown shadow where the sunlight appears, a cup of coffee is placed beside laptop, laptop is a MacBook. the image is in portrait camera mode, background is blurred, and hands of girl are placed on the laptop as she is using her laptop for some work, when i zoomed the image i came to know that she is writing code. the laptop screen is visible to the viewer and viewer can only see her side profile."

**SEED:** 70216

**Goal of this step:** Lock in the core subject, setting, lighting, and camera framing — girl, cafe, glass window, sunlight, MacBook, coffee cup, portrait mode, blurred background, side profile, visible screen with code.

---

### Iteration 2 — Fix the table and cup placement
**Prompt:**
> "the girl is sitting on a separate table which is a normal sized round table, the cup is placed on left side."

**SEED:** 70216

**Goal of this step:** The baseline output didn't match the reference's table type and coffee cup position closely enough, so this iteration corrected the table to a standalone, normal-sized round table and moved the coffee cup to the left side to match the reference image layout.

---

### Iteration 3 — Refine camera angle, framing, and outfit color
**Prompt:**
> "legs are not visible. the image is taken from left side of that girl. and she looks very smart and elegant. she is wearing beige sweat shirt."

**SEED:** 70216

**Goal of this step:** Cropped the frame so legs are excluded, explicitly fixed the camera position to the subject's left side, and adjusted the sweatshirt color to beige to better match the reference.

---

### Iteration 4 — Final post-processing adjustment
**Prompt:**
> "Flip this image horizontally and change the color of sweat shirt to beige."

**SEED:** 70216

**Goal of this step:** A final corrective pass — mirroring the composition horizontally to match the reference's orientation, and reinforcing the beige sweatshirt color since it hadn't fully carried over from the previous step.

## Final Result

The final consolidated prompt (combining all confirmed details from Iterations 1–4) is saved in [`system_prompt.txt`](./system_prompt.txt), and the resulting image is saved as `final_image.png`, both using **SEED: 70216** throughout for full reproducibility.

## Key Takeaway

Keeping the SEED constant across all four iterations meant every visual difference between outputs was a direct, measurable effect of the prompt change — table shape/cup position (Iteration 2), camera angle/framing/color (Iteration 3), and orientation (Iteration 4) — rather than random variation. This made it possible to converge on the reference image through targeted, incremental prompt edits instead of trial and error.
