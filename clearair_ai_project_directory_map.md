# ClearAir AI — Production Project Structure & Codebase

This repository contains the complete source code, modular components, deterministic physics engine, Gemini 2.5 Flash structured JSON integration, and deployment configuration for **ClearAir AI (Top 400 Competition Edition)**.

```
clearair-ai/
├── README.md
├── index.html                   # Unified standalone production application
├── package.json                 # Project manifest & tooling scripts
├── vite.config.js               # Fast bundling & local dev server configuration
├── src/
│   ├── main.js                  # Application bootstrapper & lifecycle
│   ├── styles/
│   │   └── main.css             # Tailwind directives & design system token extensions
│   ├── config/
│   │   ├── presets.js           # Hackathon persona presets (Delhi, Lahore, Beijing)
│   │   └── actions.js           # Science-backed clean air & IAQ action catalog
│   ├── engine/
│   │   ├── physics.js           # Deterministic 0ms IAQ & emissions calculation engine
│   │   ├── contextCompiler.js   # Two-stage prompt & telemetry serializer
│   │   └── cache.js             # State hashing, sessionStorage & memory cache
│   ├── api/
│   │   └── gemini.js            # Gemini 2.5 Flash Structured JSON Schema pipeline
│   └── components/
│       ├── header.js            # Live telemetry header & persona switcher
│       ├── inspector.js         # Layer 1-3 Architecture & Pipeline Inspector HUD
│       ├── impactVisualizer.js  # Micro-to-macro gauge & WHO benchmark comparison
│       ├── playbook.js          # Interactive action playbook with tabbed categories
│       └── navigator.js         # Structured action cards & trade-off solver panel
└── public/
    └── favicon.svg              # Botanical clean-air emblem
```

Below are all the source files organized by path.
