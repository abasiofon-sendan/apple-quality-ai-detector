# AppleGuard AI — Flat UI Redesign (Neutral Slate)

Date: 2026-08-19
Status: Approved

## Summary

Redesign the Streamlit app (`app/`) from the current multi-page, heavily-styled
UI into a single-page flat design in a neutral slate palette. Strip out all
pages, theme switching, and secondary features while keeping the core
prediction functionality working and keeping the model dropdown.

## Scope

### Removed

- **Multi-page navigation** — the radio nav (Home, Apple Quality Detection,
  Safety & Quality Guide, Model Performance, About) is removed. Only the
  detection flow remains.
- **Theme system** — `app/theme.py` theme switching (4 themes) and the
  sidebar theme selector are removed. One fixed neutral slate theme.
- **Sidebar panels** — System Status chips, About panel, and prediction
  history are removed.
- **Model comparison** — the "Compare all registered models" checkbox and
  `render_model_comparison` workflow are removed.
- **Grad-CAM** — heatmap generation and comparison display are removed from
  the UI (backend function stays in `src/`, just unused by the UI).
- **Report downloads** — JSON/CSV/PDF report download section is removed.
- **Hero banner image** — `hero.png` full-width banner is removed; replaced
  with a slim flat header.

### Kept

- **Upload + predict** core flow: upload apple image → show prediction
  (Fresh / Formalin-mixed) with confidence and class probabilities.
- **Model dropdown** — sidebar dropdown to pick among Custom CNN, Transfer
  Learning, and Fine-Tuned MobileNetV3 (FastAPI-first with local fallback,
  same as current behavior).
- **Inference time** shown under results.
- **Footer** strip.

## Visual Design

- **Palette (Neutral Slate):**
  - Primary accent: near-black `#111827`
  - Red `#DC2626` reserved for the "Formalin-mixed" result class
  - Background: light gray `#F9FAFB`
  - Surfaces: white `#FFFFFF`
  - Borders: `#E5E7EB`
  - Text: `#111827` / muted `#6B7280` / `#9CA3AF`
- **Flat styling rules:** solid fills only (no gradients), thin 1px borders,
  small 6–10px border radii, minimal shadows, clean typography.
- **Layout:** slim sidebar (model dropdown only) + two-column main area:
  upload panel left, prediction result panel right. Footer strip across the
  bottom.

## Architecture

- `app/streamlit_app.py` — entry point: page config, sidebar (model
  dropdown), two-column layout, routes to the single detection flow.
- `app/components.py` — keep `render_upload_section`, `render_image_preview`,
  `render_prediction_workflow` (adapted), `render_app_footer`,
  `render_sidebar_panel` (trimmed to model dropdown). Remove unused render
  functions and their imports.
- `app/styles.py` — replace the 900-line CSS system with a single flat
  stylesheet (~100–150 lines) covering: page background, cards, upload
  dashed box, result card, probability bars, sidebar, footer.
- `app/theme.py` — removed (no longer imported).
- `src/config.py` — unchanged except: `DEFAULT_THEME` / `AVAILABLE_THEMES` /
  `ENABLE_THEME_SWITCHING` removed; `ENABLE_GRADCAM`, `ENABLE_MODEL_COMPARISON`,
  `ENABLE_PREDICTION_HISTORY`, `ENABLE_BATCH_PREDICTION` set to `False`.
  `ENABLE_MODEL_CACHE` stays `True`.

## Data Flow

1. User selects a model in the sidebar dropdown.
2. User uploads an image (JPG/JPEG/PNG).
3. `render_prediction_workflow` runs prediction via FastAPI backend if
   available, else local prediction (`src/predict.predict_image`).
4. Result dict is rendered: prediction card (class + confidence), probability
   bars for both classes, inference time.
5. Errors surface as `st.error`; no reports, Grad-CAM, or history.

## Error Handling

- If no model is available: show `st.error` and `st.stop` (existing behavior).
- Prediction failure: `st.error("Prediction failed: ...")` inside the
  workflow try/except (existing behavior).
- FastAPI unavailable: fall back to local prediction silently (remove the
  current sidebar warning banner, keep behavior).

## Testing

- Run `streamlit run app/streamlit_app.py` locally and verify:
  1. App renders as a single page with the two-column flat layout.
  2. Model dropdown lists the 3 models and switching changes the active model.
  3. Uploading an image produces a prediction with confidence and both
     probability bars.
  4. No import errors — `app/theme.py` and removed component functions are
     not referenced anywhere.
  5. Grad-CAM / reports / comparison / history features are gone from the UI.
- Run `python -c "from app import streamlit_app"` (or import checks) to catch
  import-time breakage without launching the server.

## Files Changed

- `app/streamlit_app.py` — rewrite (single page)
- `app/components.py` — trim to used components
- `app/styles.py` — replace with flat stylesheet
- `app/theme.py` — delete
- `src/config.py` — remove theme flags, disable unused features
