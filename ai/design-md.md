# What is DESIGN.md?

Source:

- <https://getdesign.md/what-is-design-md>
- <https://stitch.withgoogle.com/docs/design-md/overview>

The DESIGN.md concept was introduced by Google Stitch. It's a design system document that AI agents read to generate consistent UI across your project.

Every project has a visual identity: colors, fonts, spacing, component styles. Traditionally, this lives in a Figma file, a brand PDF, or a designer’s head. None of these are readable by an AI agent.

DESIGN.md changes that. It’s a plain-text design system document that both humans and agents can read, edit, and enforce. Think of it as the design counterpart of `AGENTS.md`.

| File      | Who reads it  | What it defines                      |
| --------- | ------------- | ------------------------------------ |
| README.md | Humans        | What the project is                  |
| AGENTS.md | Coding agents | How to build the project             |
| DESIGN.md | Design agents | How the project should look and feel |

## 1. The problem: AI builds "nice" but not "yours"

Tell any AI agent to "build me a landing page" and you already know what you'll get. Rounded cards. A purple-blue gradient. A centered hero. A "Get Started" button. It works. It also looks like everything else.

The reason is simple. The agent's idea of "good design" is an average of averages. It has no clue why Vercel uses border instead of shadow, why Linear keeps its letter-spacing so tight, or why Stripe goes easy on gradients. Even if it did know, cramming all of that into a prompt is borderline impossible.

So you end up with two bad options:

1. Write 40 lines of prompt every time ("use #0070f3 for links, -0.02em letter spacing on headings, 8px border radius, no shadows just 1px borders...") and still get half of it wrong.
2. Screenshot a site, paste it, say "make it look like this." The agent copies pixels but misses the system behind them.

Neither scales.

## 2. The fix: DESIGN.md

A DESIGN.md file describes a design system semantically. It is not a token list. Not a Figma export. Not a component library. Picture a document where an experienced designer explains a brand's visual language to a developer who's seeing it for the first time. That's what it reads like.

Here's what goes inside:

- Visual theme and atmosphere tells the agent what the brand looks like and, more importantly, why. The philosophy behind the aesthetic. Sentences like "Minimalism as engineering principle." The agent gets intent, not just instructions.
- Color palette and roles gives every color a hex value and a job. "#ff5b4f, ship red, used for the production deploy flow because shipping should feel urgent." The name tells you what the color does.
- Typography rules cover font, size, weight, line-height, letter-spacing. But the real value is context: which style goes where, and why. "Display sizes get -2.4px tracking because headlines should feel like minified code."
- Spacing, shadows, motion, components fill in the rest of the system. Every rule, wherever possible, with a reason attached.

DESIGN.md keeps token, rule, and rationale in the same file. A token tells you what to use but not where. A rule tells you where but not when to bend it. The rationale is what lets an agent make the right call when it hits a situation the file never covers.

## 3. What DESIGN.md is not

The name can be misleading, so this matters:

You can't drop it in and call the theme done. It is a dictionary. The implementation still needs writing. There is no code inside, just rules. It describes what a button looks like; you or your agent still build the button.

It is not a brand guideline PDF either. Brand guidelines are written for humans and speak too loosely for agents to act on ("our brand feels approachable yet premium"). A DESIGN.md has to be specific enough for the agent to make its next decision.

It is not a Figma export. Figma token exports tell you "what" but skip "why." A DESIGN.md carries the rationale.

And it is not static. When the brand evolves, the file evolves. It gets versioned, PR'd, discussed. It behaves like code.

## 4. The structure of a DESIGN.md file

A DESIGN.md file has 9 standard sections. Each one is a layer the agent reaches for when making a specific design decision.

### 4.1. Visual theme and atmosphere

The top of the file describes the brand's feel. Not tokens or pixels. Attitude and philosophy.

```markdown
## Visual theme and atmosphere

Linear's interface embodies "opinionated calm." Every surface is dark,
every motion is restrained, every element earns its place through
information density, not decoration. The aesthetic borrows from
developer tooling: monospaced accents, tight spacing, muted palettes.
```

### 4.2. Color palette and roles

Every color is defined with its hex value and its semantic role. The file doesn't just say "blue." It says what that blue does.

```markdown
## Color palette

| Role           | Token            | Value   |
| -------------- | ---------------- | ------- |
| Background     | --bg-primary     | #000000 |
| Surface        | --bg-surface     | #141414 |
| Brand accent   | --accent-primary | #5E6AD2 |
| Destructive    | --color-danger   | #E5484D |
| Text primary   | --text-primary   | #EDEDEF |
| Border default | --border-default | #2A2A2A |
```

### 4.3. Typography rules

Font family, size hierarchy, weight, line-height, and letter-spacing, all in a table, with context for which one goes where.

```markdown
## Typography

Font: Inter (UI), JetBrains Mono (code)

| Level     | Size | Weight | Line-height | Letter-spacing |
| --------- | ---- | ------ | ----------- | -------------- |
| Display   | 52px | 500    | 1.1         | -2.4px         |
| Heading 1 | 32px | 500    | 1.2         | -1.2px         |
| Body      | 14px | 400    | 1.6         | -0.1px         |
| Caption   | 12px | 400    | 1.4         | 0              |
```

### 4.4. Component styles

Style definitions for core elements like buttons, cards, inputs, navigation, and badges, including all states. Padding, border-radius, shadow, hover/focus/disabled behavior.

```markdown
## Components

### Button (primary)

- Background: var(--accent-primary)
- Padding: 6px 12px
- Border-radius: 6px
- Font-size: 13px, weight 500
- Hover: brightness(1.15)
- Focus: 2px ring offset 2px
- Disabled: opacity 0.5, pointer-events none

### Card

- Background: var(--bg-surface)
- Border: 1px solid var(--border-default)
- Border-radius: 8px
- Padding: 16px
- Shadow: none (depth comes from borders only)
```

### 4.5. Layout principles

Spacing scale, grid system, container widths, whitespace approach, and border-radius scale.

```markdown
## Layout

- Base unit: 4px
- Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64
- Max content width: 1080px
- Section gap: 64-96px
- Border-radius scale: 4px (badge), 6px (button), 8px (card), 12px (modal)
```

### 4.6. Depth and elevation

The shadow system, surface hierarchy, and elevation levels. Which layer gets which shadow, with specific rgba values.

```markdown
## Depth and elevation

| Level   | Usage         | Shadow                     |
| ------- | ------------- | -------------------------- |
| Level 0 | Page bg       | none                       |
| Level 1 | Card, panel   | 0 1px 2px rgba(0,0,0,0.3)  |
| Level 2 | Dropdown      | 0 4px 12px rgba(0,0,0,0.4) |
| Level 3 | Modal, dialog | 0 8px 24px rgba(0,0,0,0.5) |
```

### 4.7. Do's and don'ts

Design boundaries and anti-patterns. The "don't" list matters at least as much as the "do" list.

```markdown
## Do's and don'ts

Do:

- Use border for separation, not shadow
- Keep letter-spacing tight on headings (-1px or more)
- Use opacity for disabled states, not gray tints

Don't:

- Don't use rounded-full on rectangular buttons
- Don't mix warm and cool grays in the same surface
- Don't use gradients on interactive elements
- Don't exceed 3 font weights on a single page
```

### 4.8. Responsive behavior

Breakpoints, touch target sizes, and how things collapse on smaller screens.

```markdown
## Responsive

| Breakpoint | Width     | Behavior                        |
| ---------- | --------- | ------------------------------- |
| Mobile     | < 640px   | Single column, bottom nav       |
| Tablet     | < 1024px  | Sidebar collapses to overlay    |
| Desktop    | >= 1024px | Full layout with persistent nav |

- Touch target minimum: 44x44px
- Font sizes don't drop below 13px on mobile
```

### 4.9. Agent prompt guide

A quick-reference color summary and ready-to-use component prompts for the agent.

```markdown
## Agent prompt guide

Quick palette: bg=#000, surface=#141414, accent=#5E6AD2, text=#EDEDEF

### Ready-to-use prompts:

- "Create a settings page" -> dark bg, grouped sections with subtle borders,
  toggle switches using accent color, 14px body text
- "Build a data table" -> compact rows (36px height), monospaced numbers,
  sticky header, hover row highlight at 4% white overlay
```
