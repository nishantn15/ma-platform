# Folder Restructure Changelog

**Date:** 2026-04-20
**Reason:** Align local folder with Google Drive structure for consistency and collaboration readiness.

## Previous Structure (flat + 2 subdirs)
```
MidMarket_MA_Platform_TK/
├── 00_MEETING_PREP_TK.md
├── 01_email_context.md
├── 02_platform_detailed_summary.md
├── ...all numbered .md files at root...
├── platform_*.html (4 files at root)
├── references/          ← PDFs, PPTXs, JPG
└── references-md/       ← markdown summaries of reference decks
```

## New Structure (organized subfolders)
```
MidMarket_MA_Platform_TK/
├── Research & Analysis/     (12 files)
│   ├── 01_email_context.md
│   ├── 02_platform_detailed_summary.md
│   ├── 03_india_midmarket_ma_landscape.md
│   ├── 04_emerging_sectors_ma.md
│   ├── 05_platform_business_models_research.md
│   ├── 6Pager_Summary.md
│   ├── CXO_Deck_10Apr2026.md
│   ├── Global_MA_ExecEd_Research.md
│   ├── IIM_Ahmedabad_and_Others_ExecEd_Research.md
│   ├── IIM_Bangalore_ExecEd_Research.md
│   ├── MLP_Roadmap_and_Outreach_Pack.md
│   └── OnePager_9Apr2026.md
├── Curriculum/              (3 files)
│   ├── 07_curriculum_draft_v1.md
│   ├── 08_curriculum_v2_refined.md
│   └── 09_rubber_duck_critique.md
├── Meeting Notes/           (2 files)
│   ├── 00_MEETING_PREP_TK.md
│   └── 06_call_notes_TK_Nishant.md
├── Reference Decks/         (5 files)
│   ├── MA_Leadership_Platform_CXO_Deck_10 Apr 2026.pptx
│   ├── MLP_Roadmap_and_Outreach_Pack.pptx
│   ├── MA_Leadership_Platform_OnePager_9 Apr 2026.pdf
│   ├── Mid_Market_MA_Leadership_Platform_6Pager.pdf
│   └── email_from_tk.jpg
├── Platform Prototypes/     (4 files)
│   ├── platform_v3_navy_gold.html
│   ├── platform_v3_minimalist.html
│   ├── platform_v2.html
│   └── platform_landing_page.html
└── folder-change.md         (this file)
```

## What Changed
| Old Location | New Location |
|---|---|
| `references/` (5 files) | `Reference Decks/` |
| `references-md/` (7 files) | `Research & Analysis/` (merged with research docs) |
| Root-level `0x_*.md` research files | `Research & Analysis/` |
| Root-level `07-09_*.md` curriculum files | `Curriculum/` |
| Root-level `00_*, 06_*` meeting files | `Meeting Notes/` |
| Root-level `platform_*.html` files | `Platform Prototypes/` |

## Mirrors
- **Google Drive:** https://drive.google.com/drive/folders/1FjdQ0Ab3iq5b5WtT-zyHpyGKLiBeETmu
- **Local:** /storage/emulated/0/Download/MidMarket_MA_Platform_TK/

Both locations now have identical structure. Total: 26 files across 5 subfolders.
