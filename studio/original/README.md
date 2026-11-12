# Original scene production / صناعة الأفلام من الصفر
This pipeline complements the existing licensed-footage translation pipeline.

Stages: script -> shot list -> characters and environment consistency bible -> image/keyframes -> motion/video generation -> dialogue/TTS -> Foley/music -> scene edit -> quality checks -> cover -> publish.

## Backend design
- `scene_spec.schema.json`: shot contract, continuity, reference assets and quality criteria.
- `prepare_shots.py`: fail-closed validation and per-shot manifest generation.
- `backends.json`: candidate render backends and capability/availability statuses.
- The first supported mode is `storyboard` (shot manifests and prompts). It **does not generate video**. Actual render adapters need GPU/runtime and testing.
- Keep image, motion, speech and music engines independent, so an unavailable or expensive engine can be replaced.
- Do not claim model installation, generation, quality or GPU readiness until demonstrated.
- No unlicensed footage/music or imitation of real voices without permission.

For each shot record visual action, subject identity, camera, setting, duration, aspect, Arabic dialogue, reference asset IDs and consistency constraints. Validate every scene before rendering.
