# Paste into a web or app agent

Copy the **contents** of `LITE.md` or `LITE-KR.md` into the requested conversation or project instruction field. Add the task and source material separately. Do not paste all optional references by default. A text field supplies instructions; it does not install tools or grant permissions.

Example task (Korean):

```text
Project Sales 기준으로 첨부한 제품 소개와 기업 명단을 검토합니다.
고객군 가설, 후보별 적합·제외 근거, 상위 후보의 첫 메일 초안을 만듭니다.
실제 연락처 검증이 안 된 항목은 미확인으로 남기고 발송하지 않습니다.
```

For a single reply:

```text
Classify only the supplied sales reply. Distinguish interest, courtesy,
opt-out, and out-of-office. Propose the next action; do not send or save anything.
```

Where a product has native skill upload, follow that product's current format and availability. The `dist/project-sales-core.zip` archive contains a single self-contained skill directory, but generic file upload is not proof of native installation. For ChatGPT web, LITE is the universal text route; official plugin distribution is a separate host workflow, not implemented by this repository. Consult the dated source notes before using host-specific setup instructions.

No actual browser, mailbox, or calendar can be inferred from the presence of its name in a prompt. Keep missing checks visible and supply useful drafts.
