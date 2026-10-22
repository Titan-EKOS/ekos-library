---
id: TANGERINE-010
title: Civil 3D alignment extraction and InfraWorks corridor views - check license
  and loader first
type: skill
function: data-gathering
trigger: An automated run needs alignments, profiles or corridor geometry from Civil
  3D drawings or perspective renders from InfraWorks
steps:
- Before scheduling, confirm a Civil 3D seat is free on this machine (no Device limit
  reached)
- Build any NETLOAD plugin as a proper project targeting the installed AutoCAD .NET
  runtime and test it in accoreconsole on one drawing
- 'Fallback: export LandXML alignments and profiles from Civil 3D by hand and read
  them with a script'
- Build the InfraWorks base model (terrain, aerial) only after CRS and vertical units
  are verified; do not present source-only aerial views as proposed-corridor renders
gotchas:
- A csc-compiled Extract.dll mixing .NET 8 and .NET 10 references failed in accoreconsole
  with Unable to load assembly, then Unknown command
- Civil 3D showed Device limit reached because another device held the seat; proposed
  corridor and six perspectives stayed pending
jurisdiction: Town of Marana
tools_versions: AutoCAD / Civil 3D 2026, InfraWorks 2026, accoreconsole, csc
evidence:
- C:\Ekos\projects\tangerine\qa\cad_extract.log
- C:\Ekos\projects\tangerine\cad\compile.ps1
- C:\Ekos\projects\tangerine\README.md
hours_lost: 2.0
recurrence: 1
confidence: medium
project: TANGERINE
source_ai: claude
timestamp: '2026-10-22T23:35:09+00:00'
schema_version: 1
---
