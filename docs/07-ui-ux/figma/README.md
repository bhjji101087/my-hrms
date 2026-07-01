# UI Designs — Visual Mockups & Figma Handoff

> ⚠️ **Superseded:** these flat SVG wireframes are kept for layout reference only. The
> **canonical visual design is now the interactive prototype** at
> `../prototype/index.html` (approved "Modern & Friendly" theme). Review that, not these.

This folder holds the **viewable visual designs** for the foundational screens.

## What's here

`*.svg` — renderable wireframe/mid-fidelity mockups (open in any browser or VS Code's
SVG preview). These are the **concrete visuals to review and approve** before development.

## The design asset pipeline

```
 Low-fi (text)            Mid-fi (here)              Hi-fi (Figma)
 SCREENS-001.md  ──────►  *.svg mockups  ──────►  Figma file (.fig)
 ASCII wireframes         viewable images          by Figma Designer (Agent 12)
```

## Honest note on "Figma"

Native Figma files (`.fig`) cannot be generated as text — they require the Figma
application and a human designer (Agent 12 in our roster). The SVGs here are a faithful
**visual stand-in** so the layout, hierarchy, and flow can be approved now. Once approved,
a designer reproduces them as a high-fidelity, interactive Figma prototype using the
tokens in `DESIGN-SYSTEM-001`.

## Screens

| File | Screen | Surface |
|---|---|---|
| `01-login.svg` | Login + tenant resolution | Desktop |
| `02-employee-directory.svg` | People directory | Desktop |
| `03-apply-leave.svg` | Apply leave (ESS) | Mobile |
| `04-approvals-inbox.svg` | Approvals inbox | Desktop |
| `05-workflow-studio.svg` | Workflow Studio builder | Desktop |

## Approval

These mockups are **pending your visual sign-off**. See the new
**UI Design Sign-off gate** in `PROJECT_STATE.md` — design must be approved before any
implementation (Golden Rule 1 extended to UI).
