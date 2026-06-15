---
globs: ["**/*.tsx", "**/*.jsx", "**/*.css", "**/*.vue", "**/*.svelte"]
alwaysApply: false
---
# UI / UX Standards

## Design Principles

1. **Workflows Over Visual Polish** — Decisions prioritize speed and clarity of daily work, not decorative aesthetics.
2. **Consistency Beats Individuality** — Same actions look and behave the same everywhere (Primary button, confirm pattern, error display).
3. **Clarity Over Complexity** — Information layered by relevance: primary content prominent, secondary in tabs/accordions. Clear visual hierarchy (typography, contrast, spacing).
4. **Communicate Errors Early & Clearly** — Inline validation, understandable messages, actionable guidance. Errors close to the interaction.
5. **Feedback on Every User Action** — Every relevant action (create, save, move, send) gets visual feedback (loading indicator, state change, toast).
6. **Safe Defaults & Undo Where Feasible** — Prefer archive/soft delete with restore option over hard deletion. Critical actions guarded and reversible.

## Layout & Navigation

### Base Layout (Desktop-First)
- **Left Sidebar** — Global navigation (main areas, projects, views).
- **Main Area** — Primary content (lists, detail views, dashboards).
- **Optional Right Sidebar** — Contextual info (details, chat, activity).
- Three-column pattern is familiar and scales well.

### Navigation
- **Primary Navigation** — Defined per project (project selector, views, notifications).
- **Secondary Navigation** — Tabs within an area when needed.
- **Breadcrumbs** — Clickable, structure: "Area / Subcategory / Detail". Serve as fast back-navigation.

## Component Standards

### Buttons
- **Primary** — Most important action on screen (Create, Save). Right-aligned in forms.
- **Secondary** — Less critical actions (Cancel, Reset Filters). Left of Primary.
- **Destructive** — Red, only for data-loss actions (Delete). Right-aligned in dialogs, Cancel left.

### Forms
- **Labels** — Always visible, never placeholder-only. Required fields marked `*` and explained in error text.
- **Field Order** — Matches user's mental model.
- **Validation** — Inline on blur or after submit. Error under field with clear explanation. Not color-only (icons/text for accessibility).

### Modals, Drawers, Pages
- **Modal** — Small focused actions (Create, Quick Edit).
- **Drawer (Right Sidebar)** — Detail views that keep background context.
- **Full Page** — Complex or critical processes (Settings, Admin).

### Tables & Lists
- **Tables** — Sortable by relevant fields. Sticky header for many rows. Define columns per project.
- **Responsive** — Less critical columns hidden or stacked on small viewports.

## States & Feedback

### Loading
- **Page-Level** — Skeletons for key areas, no global spinner.
- **Inline** — Buttons show spinner + disabled during action (e.g., "Saving...").

### Empty States
- **Empty Lists/Areas** — Brief explanation ("No entries yet") + prominent CTA ("Create").
- **Empty Filter Results** — Indicate active filter + easy reset.

### Error States
- **Form Errors** — Directly on field, brief cause + actionable instruction.
- **API/Network Errors** — Toast or inline alert: "Action could not be saved. Please retry." Persistent errors: "Show Details" with technical info (internal users).

### Realtime Feedback (if applicable)
- New data appears without reload (chat, live updates).
- Subtle hints when open data changes externally ("Updated — Show changes").

## Text & Microcopy
- **Tone** — Clear, concise, professional. No playful error messages.
- **Terminology** — Consistent within app and across JF suite.
- **Buttons** — No generic labels: "Save" not "OK", "Submit" → concrete action name.
- **Confirm Dialogs** — Describe action + consequence: "This item will be archived and hidden from overview. You can restore it later."

## UX Principles for Internal Tools
1. **Optimize for Speed** — Keyboard shortcuts for frequent actions. Focus management: after Create focus sensible field, after Save focus next element.
2. **Medium Information Density** — Higher density than public products acceptable if readability/structure preserved. Long tables and complex views allowed with good filtering/sorting.
3. **Error Prevention Over Correction** — Critical actions always with confirm dialog + clear warning. Defaults biased toward safe choices.

## Accessibility Baseline
- **Contrast & Colors** — Target WCAG AA for text/icons, especially status badges and buttons.
- **Focus States** — All interactive elements have visible focus states (never removed).
- **Semantics** — Headings, lists, buttons semantically correct for screen readers and stable keyboard navigation.
- Even internal tools must meet these baselines for usability and future extensibility.

## Design Tokens (JF Corporate)
- **Primary**: `#5676ad`
- **Background**: `#f4f2ee`
- **Text**: `#333333`
- All colors as CSS Custom Properties.
- Icons: `lucide-react` (TS/React) or equivalent consistent set.
- Language: Code/Comments English, UI texts German. Error messages user-friendly, no technical details.
