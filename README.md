# Voxy NeoForge 1.21.1

An unofficial NeoForge 1.21.1 port of **Voxy**, the high-performance Level of Detail terrain renderer for Minecraft.

Voxy renders far-away terrain at lower detail so you can see much farther than vanilla render distance without asking your computer to draw every distant block as a full chunk. This port is aimed at NeoForge modpacks that want Voxy-style distant terrain rendering without running the Fabric build through a compatibility layer.

> All original Voxy credit belongs to [MCRcortex](https://github.com/MCRcortex), the creator of Voxy.

## Status

This port is currently **alpha** software. It builds for Minecraft 1.21.1 and NeoForge 21.1.x, but you should test it in a copy of your world or a fresh profile before adding it to a long-term modpack.

### What Works

- Distant Level of Detail terrain rendering
- Smooth handoff between vanilla chunks and LOD terrain
- Sodium-based rendering integration
- NeoForge mod metadata and dependency declarations
- Fog handling at LOD boundaries
- Block model baking for solid, cutout, cutout-mipped, and translucent render layers

### Known Limitations

- Client-side only; do not install this on a dedicated server.
- Requires the NeoForge build of Sodium.
- Shader and optional mod integrations are still being ported and tested.
- Some behavior may differ from upstream Fabric Voxy while this NeoForge port is stabilized.

## Requirements

| Requirement | Version |
| --- | --- |
| Minecraft | 1.21.1 |
| NeoForge | 21.1.x |
| Sodium | mc1.21.1-0.6.13-neoforge or newer compatible NeoForge build |
| Forgified Fabric API | 0.116.7+2.2.0+1.21.1 or compatible |

Recommended:

| Mod | Why |
| --- | --- |
| Reese's Sodium Options | Better access to Sodium-related video settings |
| Lithium | General game performance improvements |

The current development artifact has also been built against Sodium `mc1.21.1-0.8.12-alpha.4-neoforge` for alpha modpack testing.

## Installation

1. Install Minecraft 1.21.1 with NeoForge 21.1.x.
2. Add the required dependencies to your `mods` folder.
3. Download the latest `voxy-*.jar` from this repository's GitHub Releases page.
4. Place the Voxy jar in your `mods` folder.
5. Start the game once and check the mod list for `Voxy`.

For modpacks, include the Voxy jar together with the required dependency versions listed above. Keep Voxy client-side only unless a future release explicitly states otherwise.

## Configuration

Voxy's options are exposed through the client configuration and Sodium-related settings screens where available. If the config screen is not visible in your setup, install Reese's Sodium Options and confirm that Sodium is loading correctly.

Useful first-test settings:

- Start with a conservative render distance and increase it gradually.
- Test in a fresh world before using a heavily modded save.
- If you use shader packs, test with shaders disabled first, then enable them after confirming Voxy renders correctly.

## Troubleshooting

### The Game Crashes on Startup

- Confirm you are using Minecraft 1.21.1, not another 1.21.x version.
- Confirm every dependency is the NeoForge build, especially Sodium.
- Remove shader packs and optional rendering mods for the first test.
- Check `latest.log` for missing dependency or mixin errors.

### Distant Terrain Does Not Render

- Confirm the mod appears in the in-game mod list.
- Confirm Sodium is installed and active.
- Lower other rendering settings temporarily to rule out GPU memory pressure.
- Test without shaders or other rendering overhaul mods.

### Shader Issues

Shader support is sensitive during the port. If a shader pack breaks Voxy rendering, test without the shader pack and report the shader, Sodium, NeoForge, and Voxy versions together with the relevant log.

## Building From Source

Clone the repository and run Gradle:

```bash
git clone https://github.com/yarnobachmann/Voxy-Neoforge.-1.21.1.git
cd Voxy-Neoforge.-1.21.1
./gradlew build
```

On Windows:

```powershell
git clone https://github.com/yarnobachmann/Voxy-Neoforge.-1.21.1.git
cd Voxy-Neoforge.-1.21.1
.\gradlew.bat build
```

The compiled jar will be written to `build/libs/`.

## Development Notes

This repository is a NeoForge 1.21.1 port of the Fabric Voxy codebase. Porting work should be verified against local reference sources before changing mixins, access transformers, or Minecraft/Sodium integration points.

Important files:

- `build.gradle` - Gradle build, dependencies, and NeoForge setup
- `gradle.properties` - Minecraft, NeoForge, dependency, and mod versions
- `src/main/resources/META-INF/neoforge.mods.toml` - NeoForge metadata
- `src/main/resources/client.voxy.mixins.json` - Client mixin configuration
- `src/main/resources/common.voxy.mixins.json` - Common mixin configuration
- `src/main/resources/iris.voxy.mixins.json` - Iris-related mixin configuration

## Credits

- [MCRcortex](https://github.com/MCRcortex) - Original Voxy author
- [Original Voxy repository](https://github.com/MCRcortex/voxy)
- NeoForge, Sodium, and Forgified Fabric API contributors

## License

See [LICENSE.md](LICENSE.md). This is an unofficial port and is not affiliated with Mojang, Microsoft, NeoForge, Sodium, or the original Voxy project.
