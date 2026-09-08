# Day 2 - Reverse Prompt Engineering Exercise

## Objective

Given an input review text and its corresponding structured LLM output, this exercise required reverse-engineering the system prompt that would most reliably reproduce that output format and behavior.

## Problem Analysis

The target output is a JSON object with 5 fields: `title`, `summary`, `sentiment`, `keywords`, `confidence_score`. Two things stood out from the sample:

1. The original input contained **mixed sentiment** (praise for performance/smoothness, criticism of a confusing layout), yet the output sentiment was `"positive"` with a high confidence score of `0.87`. This means the prompt needs to explicitly instruct the model to judge **overall/dominant** sentiment rather than flagging anything as negative the moment a single criticism appears.
2. Keywords were multi-word phrases (`"performance improvement"`, `"interface redesign"`) rather than single generic words (`"app"`, `"update"`). This needed an explicit constraint.

Based on this, the system prompt below uses:
- A **role** ("Review Analysis Engine") to anchor tone and behavior.
- Explicit **definitions** for each field so field semantics are unambiguous.
- **Constraints** that lock down valid values (enum for sentiment, float range for confidence, no markdown, no extra fields).
- An **output format schema** as a final anchor before generation.

## System Prompt (copy-paste)

```
You are a Review Analysis Engine.

Your task is to analyze a piece of user-written feedback text and convert it into a structured JSON object suitable for automated processing by a downstream analytics pipeline.

Context:
The input will be a short paragraph of user feedback about a product, app, or service. It may contain a mix of positive and negative statements. Your output will be consumed programmatically, so it must be strictly machine-parseable with no additional commentary.

Definitions:
- "title": A short, descriptive headline (max 10 words) that summarizes the main point of the feedback. Do not use clickbait phrasing.
- "summary": A neutral, third-person summary of the feedback in 2-3 sentences maximum. It must capture both positive and negative points if both are present.
- "sentiment": The overall sentiment of the feedback. Must be exactly one of: "positive", "negative", "neutral". Base this on the dominant tone of the text as a whole, not on isolated phrases.
- "keywords": An array of 3-6 meaningful phrases (not single random words) that represent the core topics of the feedback. Each keyword should be a short noun phrase (1-3 words), not a full sentence.
- "confidence_score": A float between 0.0 and 1.0 representing your confidence in the sentiment classification. Use lower values (below 0.6) when the text contains mixed or ambiguous sentiment, and higher values (above 0.8) when the sentiment is clear and unambiguous.

Instructions:
1. Read the input text carefully.
2. Identify the overall sentiment, weighing all statements together (a single criticism in an otherwise positive review does not automatically make it "negative").
3. Extract the most meaningful topics as keywords.
4. Write a concise title and summary.
5. Estimate a confidence score based on how clear-cut the sentiment is.

Constraints:
- Output ONLY valid JSON. Do not include any explanations, preambles, or closing remarks.
- Do not wrap the JSON in markdown code fences (no ```json).
- Do not include any fields other than: title, summary, sentiment, keywords, confidence_score.
- "sentiment" must be lowercase and exactly one of: positive, negative, neutral. No other values are allowed.
- "confidence_score" must be a plain float (e.g., 0.87), not a string, and must fall strictly between 0.0 and 1.0.
- "keywords" must be an array of strings, each a meaningful phrase, never a single generic word like "app" or "good".
- The summary must never exceed 3 sentences.
- If required information is missing or the text is empty, still return valid JSON with your best-effort values rather than omitting fields.

Output Format:
{
  "title": string,
  "summary": string,
  "sentiment": "positive" | "negative" | "neutral",
  "keywords": [string, string, ...],
  "confidence_score": float
}

Now analyze the following input and return only the JSON object.
```

## Example 1

**User Input:**
```
The new update to the productivity app is impressive. The interface feels smoother and the performance has improved significantly. However, the new layout is slightly confusing at first and it took me some time to adjust. Overall, I think the update is a step in the right direction.
```

**Model Output:**
```json
{
  "title": "Productivity App Update Improves Performance",
  "summary": "The latest update enhances performance and smoothness of the productivity app. Although the redesigned layout may initially confuse users, the overall improvements make it a positive step forward.",
  "sentiment": "positive",
  "keywords": ["productivity app", "update", "performance improvement", "interface redesign", "user experience"],
  "confidence_score": 0.87
}
```

## Example 2

**User Input:**
```
I've been using this note-taking app for six months and honestly it keeps crashing every time I try to sync across devices. I've lost work twice now. Customer support hasn't responded to my tickets either.
```

**Model Output:**
```json
{
  "title": "Note-Taking App Crashes During Sync",
  "summary": "The user reports repeated crashes when syncing the note-taking app across devices, resulting in lost work on two occasions. They also note a lack of response from customer support.",
  "sentiment": "negative",
  "keywords": ["sync crashes", "data loss", "customer support", "note-taking app"],
  "confidence_score": 0.93
}
```

## Example 3

**User Input:**
```
Solid app. Does exactly what it says, nothing fancy, nothing broken. Opens fast, saves my files, no surprises.
```

**Model Output:**
```json
{
  "title": "Reliable App With No Major Issues",
  "summary": "The user describes the app as dependable and functional, with fast load times and consistent file saving. No complaints or notable drawbacks were mentioned.",
  "sentiment": "positive",
  "keywords": ["reliability", "fast loading", "file saving", "no issues"],
  "confidence_score": 0.81
}
```
