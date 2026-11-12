# Korea four-part release audit — 2026-11-12 14:16 Asia/Riyadh

## Verified actual artifacts
- Run 43207413138 completed success and uploaded artifact **13940615608**, `korea-four-full-arabic-parts`, 53,719,776 bytes; expires 2026-11-19 11:16:35 UTC. https://github.com/drcmdd91-cyber/hikaya-audio/actions/runs/43207413138
- Run 43207273520 completed success and uploaded artifact **13939291818**, 53,718,074 bytes; expires 2026-11-19 11:16:12 UTC. https://github.com/drcmdd91-cyber/hikaya-audio/actions/runs/43207273520
- Run 43207548200 was in progress (render step) at this audit. https://github.com/drcmdd91-cyber/hikaya-audio/actions/runs/43207548200
- **None of these artifacts has been visually or aurally reviewed in this audit. They are renders, not approved deliverables.** Do not publish or delete old posts yet.

## Critical reproducible risk in `.github/workflows/korea-full-arabic.yml`
1. Narration is built from only n1.wav, n2.wav, n3.wav plus three radio lines. There is no per-scene cue sheet or verified source event timeline.
2. Video uses four fixed 124-second intervals (`START=(N-1)*124`) and slices one continuous narration by those same boundaries. This does not demonstrate that each spoken sentence matches the visible event; earlier cross-part mismatches were explicitly reported by the owner in issue #1.
3. `amix=inputs=4:duration=first` in narration mix may truncate dialogue to the narration track length; source voice duration is not checked against the full 496 seconds.
4. Source audio is mixed under Arabic at low volume, but no audit confirms English speech was removed without affecting effects.
5. The workflow emits MP4s only: no independent covers, timestamped speaker dialogue ledger, synchronized word captions, or human-review evidence.
6. Success status means ffmpeg and upload completed; **it is not proof of audiovisual synchronization**.

## Required release gates
- Extract and archive the original 496-second timeline with `scene_id, source_in, source_out, part_id, speaker_id, original_dialogue, arabic_text, voice_file, audio_in, audio_out`; compare every sentence to footage.
- Probe and verify each source/narration/dialogue length; no audio may be absent due to short track or cross-part offset.
- Separate all speaking characters' voices, use appropriate radio effects, keep environmental audio, and inspect all four complete rendered videos visually and aurally.
- Produce correct individual covers, captions and metadata; save approval evidence.
- Only after all four replacements are approved and available, publish in order, verify each TikTok URL, then remove obsolete posts only when authorized tool access and verified replacement exist.
- Source/rights: https://youtu.be/izwUcX2UMuY ; owner has confirmed rights for this specific project, not a blanket license for other sources.
- Issue tracking: https://github.com/drcmdd91-cyber/hikaya-audio/issues/1

**Release status: BLOCKED ON ACTUAL AUDIOVISUAL VERIFICATION AND CUE-SHEET CORRECTION. No new TikTok publication verified during this audit.**
