# دفتر الحكايات — Studio Pipeline v1
This is a reusable production scaffold, **not** a verified automatic publishing system.

## Flow
1. Fill `project.json` and complete the script before rendering.
2. Create a verified shot-by-shot `timeline.json` with source time ranges, Arabic dialogue, speaker IDs, narration audio paths and evidence.
3. Run `python studio/check_project.py studio/templates/project.json studio/templates/timeline.json` (templates deliberately fail until filled).
4. Render previews and final outputs only after reviewing scene/audio matching manually.
5. Produce unique cover for each part, verify MP4 with ffprobe, and publish via authorized channel connector; verify post URL.
6. Log every error, workaround, actual elapsed time and a prevention test in GitHub Issues.

**Non-negotiable:** An automated schema check cannot certify that an Arabic sentence describes the visible action. Visual/audio human review is required. No fixed 90-second scene splitting or fixed 1.2-second voice offset. No deleting published posts before corrected replacements are verified.

Targets: Korea full correction <=2 hours (aspirational); future full projects 15 minutes from start to verified publication (aspirational, not guaranteed).
