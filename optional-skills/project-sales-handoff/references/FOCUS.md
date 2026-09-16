# Meeting and sales handoff

Use when an existing conversation needs a human owner, a reply about booking, or an update proposal for a connected system. The output is a handoff, not an external write.

## Minimum useful context

Identify the product/project, relevant contact and company, source thread, expressed need, requested next step, commitments already made, unresolved questions, and proposed owner. Unknown budget, purchasing authority, timeline, or company facts stay unknown. Do not force a sales qualification framework when the conversation does not support it.

Use only a real, supplied or verified booking link. A supplied link is still not evidence that anyone booked. Never invent an owner's availability. If availability tools are available and authorized, use their returned timezone and scope; otherwise propose asking about availability.

## Booking states

- `not_discussed`: no scheduling discussion.
- `meeting_intent`: interest in meeting, not a reservation.
- `link_shared`: the actual thread shows a link was sent; a link merely drafted is not shared.
- `time_proposed`: an actual date/time was proposed, not mutually confirmed.
- `confirmed`: a reliable booking record or explicit mutual agreement identifies date, time, timezone, and parties.
- `cancelled`: a previously confirmed meeting was cancelled.
- `held`: there is evidence the meeting occurred; a past date alone is insufficient.
- `unknown`: insufficient or conflicting records.

A calendar entry created only by the operator is not evidence of recipient agreement. A provider record with "pending" attendees may be tentative. For ambiguous dates such as "Tuesday", resolve the date/timezone from context or leave it pending rather than choosing silently.

## Output

A compact human-readable brief is enough unless an app requests structured data. Distinguish the current observed booking state from any proposed next state. Include evidence references, the next owner/action, and exact unresolved items.

For a CRM update or invitation request, prepare an action proposal with the intended destination, exact fields or message, and required approval scope. Do not claim a remote draft, deal, contact, or event was saved. Minimize exported personal data; never include the full mailbox or credentials for a one-contact handoff.
