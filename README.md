# Voxy NeoForge 1.21.1

> **Unofficial NeoForge port** of the Voxy mod

## Special Thanks

**All credit for Voxy goes to [MCRcortex](https://github.com/MCRcortex)**, the original author and creator of this incredible LOD rendering mod.

- **Original Repository:** [MCRcortex/voxy](https://github.com/MCRcortex/voxy)
- **Original Author:** [MCRcortex](https://github.com/MCRcortex)

This repository is a community port to NeoForge 1.21.1, created because the original author has indicated they will not be backporting to this version. We are deeply grateful for MCRcortex's work on Voxy.

## License Notice

The original Voxy mod is licensed under **All Rights Reserved** by MCRcortex. This port is provided for personal use. Please respect the original author's licensing terms.

---

## About

**Voxy** is a Level-of-Detail (LOD) rendering mod for Minecraft that extends your view distance far beyond vanilla limits by rendering distant terrain at lower detail levels.

## Status

**Alpha** - Functional with known limitations.

### Working Features
- LOD terrain rendering beyond vanilla render distance
- Smooth transitions between LOD and vanilla chunks
- Fog integration (disabled at LOD boundaries)
- Block model baking for all render types (solid, cutout, cutout_mipped, translucent)
- Delayed chunk unloading to prevent pop-out effects

### Current Limitations
- Requires Sodium 0.6.13+ (NeoForge version)
- Some optional integrations not yet ported (Iris, Nvidium, Vivecraft)
- Debug screen integration disabled (MC 1.21.1 API changes)

## Requirements

| Dependency | Version | Link |
|------------|---------|------|
| Minecraft | 1.21.1 | - |
| NeoForge | 21.1.x | [NeoForge](https://neoforged.net/) |
| Sodium | mc1.21.1-0.6.13-neoforge | [Modrinth](https://modrinth.com/mod/sodium/version/mc1.21.1-0.6.13-neoforge) |
| Forgified Fabric API | 0.116.7+2.2.0+1.21.1 | [Modrinth](https://modrinth.com/mod/forgified-fabric-api/version/0.116.7+2.2.0+1.21.1) |

## Installation

1. Install NeoForge for Minecraft 1.21.1
2. Install Sodium (NeoForge version)
3. Install Forgified Fabric API
4. Download Voxy from the [Releases](https://github.com/j-shelfwood/voxy-neoforge/releases) page
5. Place the JAR in your `mods` folder

## Building from Source

```bash
./gradlew build
```

The built JAR will be in `build/libs/`.

## Contributing

For development guidelines, see [CLAUDE.md](CLAUDE.md).

### Validation Scripts

The `scripts/` directory contains build validation tools used in CI.

## Links

- **Original Voxy:** [github.com/MCRcortex/voxy](https://github.com/MCRcortex/voxy)
- **This Port:** [github.com/j-shelfwood/voxy-neoforge](https://github.com/j-shelfwood/voxy-neoforge)
- **Releases:** [Releases Page](https://github.com/j-shelfwood/voxy-neoforge/releases)
