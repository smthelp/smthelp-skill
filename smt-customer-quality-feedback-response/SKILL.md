# SMT Customer Quality Feedback Response

When a customer (especially a key EMS/OEM account like KnS) sends quality feedback, operational questions, or design-change requests on a Southern Machinery machine, generate a structured response plan and a polished English customer reply in Jason Wu's CEO voice.

## Workflow

1. **Ingest feedback**
   - Download/extract the source file (PPTX, PDF, email, images).
   - Extract every discrete issue, question, and design request. Preserve the customer's exact wording.

2. **Categorize each item**
   - Quality / assembly defects
   - Operational / technical questions
   - Electrical / maintenance questions
   - Design-change requests

3. **Ground in Southern Machinery facts**
   - Search `~/.workbuddy/plugins/marketplaces/my-experts/plugins/southern-machinery-knowledge-copilot/skills/southern-product-kb/references/`.
   - Use IDENTITY.md / SOUL.md / USER.md for company background and product lineup.
   - Do **not** invent MPNs, specs, datasheets, or timelines. If Jason has already drafted Chinese notes (e.g., inside the PPTX), use them as the basis and tighten the English.

4. **Draft internal response plan**
   - Table mapping: customer item → our action / answer / timeline.
   - Mark which items are already fixed, which are in redesign, and which need a delivery date.
   - Keep the tone improvement-oriented, not apologetic.

5. **Draft English customer reply (Jason Wu style)**
   - Opening: thank them, acknowledge receipt, state seriousness.
   - Body: bullets grouped by category. Each bullet names the issue and gives a concrete action or timeline.
   - Use CEO-level vocabulary: Yield, CPH, Line Balancing, CapEx, ROI, Traceability, PM, IQC/OQC.
   - Close with a low-friction CTA (e.g., 15-min call, free layout, video call).
   - Keep it concise; 200–400 words is acceptable when many items must be addressed.

6. **Red-team review**
   - Check for over-promised timelines.
   - Check for missing attachments that the email claims are attached.
   - Check for language that sounds like a warranty/legal admission.
   - Flag design-change requests that may carry cost or lead-time implications.

7. **Deliverable format**
   - Output a single Markdown file with three sections:
     1. Internal response plan (Chinese)
     2. English customer reply
     3. Internal risk review

## Output Example Structure

```markdown
# [Model]_[Customer]_Response.md

## 一、客户反馈与应对方案
| 类别 | 客户反馈 | 我们已采取 / 将采取的改进动作 |
...

## 二、致客户的英文回复
Subject: ...
...

## 三、内部风险审查
| 风险点 | 说明 | 建议处理 |
...
```

## Do Not
- Send the reply directly; always let Jason review and confirm attachments/timeline first.
- Use cheap sales clichés ("cheap machine", "best price", "please buy").
- Invent specifications not found in product KB or Jason's notes.
