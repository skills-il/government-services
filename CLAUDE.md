# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

This is a Skills IL category repository containing AI agent skills for Israeli government APIs and digital services. Each subdirectory is a self-contained skill following the open Agent Skills standard.

## Repository Structure

```
government-services/
├── .github/                          # CI workflows, issue/PR templates
├── israel-gov-api/                   # Skill: Israel Gov API
│   ├── SKILL.md                     # Required skill definition
│   └── scripts/                     # Optional helper scripts
├── israeli-address-autocomplete/     # Skill: Israeli Address Autocomplete
│   └── SKILL.md
├── CLAUDE.md                         # This file
├── LICENSE                           # MIT
└── README.md                         # Category overview
```

## Skill Format (CRITICAL)

Every skill is a folder containing a `SKILL.md` file. The folder name MUST be kebab-case.

### Validation Rules

These rules are enforced by CI on every PR:

1. File must be exactly `SKILL.md` (case-sensitive)
2. YAML frontmatter must have `---` delimiters on both sides
3. `name` field: kebab-case only, must match folder name
4. `description` field: present, under 1024 chars, no XML angle brackets, must include WHAT + WHEN
5. SKILL.md body must be under 5,000 words
6. No `README.md` inside skill folders
7. No skill names containing "claude" or "anthropic"
8. No hardcoded secrets

See [CONTRIBUTING.md](https://github.com/skills-il/.github/blob/main/CONTRIBUTING.md) for the full guide.

## Commands

```bash
./scripts/validate-skill.sh <skill-folder>/SKILL.md
```

## Conventions

- All skill folders use kebab-case naming
- Bilingual content should use `{ he: "...", en: "..." }` when applicable
- Israeli-specific context should reference official sources
- Org-level files are inherited from skills-il/.github
