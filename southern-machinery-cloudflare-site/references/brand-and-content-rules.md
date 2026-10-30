# Brand and Content Rules

## Positioning

Present Southern Machinery as an automation partner for global EMS factories, not merely an equipment vendor. Lead with complete SMT/THT line capability, engineering support, practical ROI, customization, and Shenzhen-based manufacturing and R&D.

Default public language is English unless the user requests another language. Internal planning may be Chinese.

## Information Architecture

The standard site has eight independent pages: Home, Products, Turnkey Solutions, Industries, About, Support, Contact/RFQ, and Ad Studio. Keep page purpose distinct; do not turn every page into a repeated landing-page hero.

Operational B2B design should be restrained, technical, and easy to scan. Favor specification tables, process flows, comparison views, application filters, strong navigation, clear RFQ actions, and real machine imagery. Avoid decorative card grids, oversized type inside tools, excessive rounded containers, one-color palettes, and visual effects that obscure equipment details.

## Product Claims

- Use uploaded catalogs and repository data as authoritative sources.
- Attach the source file or code location to each material specification during drafting.
- Treat CPH, board dimensions, component support, accuracy, labor replacement, and ROI as unverified until sourced.
- State assumptions for every ROI calculation: labor count, loaded labor cost, shifts, operating days, utilization, maintenance, and purchase cost.
- Never promise price or delivery time unless the user supplies current approved data.
- For unsupported customization questions, state that engineering confirmation is required and direct the inquiry to the approved contact.
- Anonymize customer examples by default.

## Conversion and Contact

Every public page needs an appropriate next action such as request a sample test, submit PCB/component information, ask for a line proposal, or contact sales. RFQ forms should ask only useful qualification questions and include consent/context appropriate to the deployment market.

Take current contact details from project `AGENTS.md` or user-provided content. Do not bake personal contact information into reusable code.

## Ad Studio

Provide a complete workflow: product selection, market/channel, language, campaign goal, key proof points, image selection, generate action, output preview, copy/export actions, and clear loading/error/empty states. Integrate through a configurable same-origin API or n8n webhook environment variable. Never expose webhook authentication in browser code.
