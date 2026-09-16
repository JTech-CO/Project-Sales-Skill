# Performance review

Use supplied campaign exports or authorized read tools. State the project/campaign scope, cohort definition, observation window, timezone, event deduplication rule, and data coverage. Do not re-run prospect discovery or start experiments without a separate request.

## Definitions

Positive replies are substantive positive_interest or meeting_intent from actual inbound messages, excluding courtesy, OOO, automatic replies, bounces, and opt-outs. Do not double-count a reply with two labels. Report clear interest separately from confirmed bookings.

Track confirmed bookings with evidence and a stable booking identity; one thread may contain multiple revisions to one booking. Keep cancellations and held meetings separate. A booking link and a calendar event created without recipient agreement are not confirmed outcomes. A past appointment is not proof of attendance.

## Recommended calculations

| Metric | Definition | Missing-data handling |
|---|---|---|
| Positive reply rate | Unique positively replying recipients / unique recipients with confirmed send acceptance in the same cohort | State that send acceptance is not delivery. Unknown denominator -> unavailable |
| Confirmed bookings | Unique confirmed booking records or mutually agreed meetings with evidence | Exclude unsupported bookings; show cancellations separately |
| Cost per confirmed booking | Included attributable cost / confirmed bookings under an explicit gross or net-of-cancellations definition | Zero bookings -> undefined; missing costs -> unavailable or clearly labeled partial cost |
| Bounce rate | Confirmed bounce count / documented applicable send denominator | Unknown reporting coverage -> unavailable, not 0% |
| Opt-out / wrong-target rate | Unique applicable recipients / stated comparable cohort denominator | Do not mix message counts with recipient counts |

For period reporting, do not divide this week's replies by this week's sends when they belong to different cohorts without labeling it as an activity ratio rather than cohort conversion. Bookings after the window require explicit follow-up coverage. A 100% rate from one response is not robust evidence.

Account for research/enrichment, verification, messaging, and model costs when available. Do not silently mix currencies or assume free tool use. State conversion rates and dates when the user provides an exchange rate; otherwise keep currencies separate. Do not set expected conversion to the historical vendor claims in the source handoff.

## Improvement

Tie a proposed change to evidence: stale contacts, unclear offer, unsupported personalization, low-quality fit, or response handling. Offer a testable hypothesis, not causal certainty from a small sample. Do not optimize for sent volume, manufactured hot leads, or bypassing opt-outs. The result is an analysis and suggested experiment, not a campaign launch.

## Small arithmetic example (fictional)

One complete cohort: 20 send-accepted unique recipients, 2 substantive positive replies, 1 evidence-backed confirmed booking, USD 8 total known attributable cost. Positive reply rate is 10%; cost per confirmed booking is USD 8. Delivery is unobserved, so there is no justified delivery or bounce rate. With zero bookings, cost per booking would be undefined rather than USD 0.
