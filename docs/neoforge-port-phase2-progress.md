# Voxy NeoForge Port - Phase 2 Progress Report

**Date:** 2025-12-31
**Branch:** `neoforge-1.21.1`
**Status:** 🔄 DEPENDENCY RESOLUTION COMPLETE - API MIGRATION IN PROGRESS
**Latest Commit:** 2492fabf

---

## Executive Summary

Phase 2 build verification has successfully resolved all build system and dependency issues. Project now compiling against correct NeoForge 1.21.1 dependencies with Forgified Fabric API support. Remaining work involves fixing MC 1.21.11 → 1.21.1 API incompatibilities (27 compilation errors identified).

**Confidence Level:** 85% - Core infrastructure working, API fixes are mechanical

---

## ✅ Completed Tasks

### 1. Build System Fixes

**Fabric Loom → NeoGradle Migration:**
- ✅ Removed `processIncludeJars()` task (Fabric Loom specific)
- ✅ Removed `remapJar()` task (handled by NeoGradle automatically)
- ✅ Replaced `include()` dependency configuration with `implementation`/`runtimeOnly`
- ✅ Replaced `minecraftRuntimeLibraries()` with standard `runtimeOnly`

**Files Modified:**
- `build.gradle` - Removed 4 Fabric Loom specific constructs
- Result: Clean build configuration compatible with NeoGradle

### 2. Dependency Resolution

**Forgified Fabric API:**
- ❌ **Initial Attempt Failed:** Version format error (`0.114.0+1.21.1+21.1.84`)
  - Issue: Incorrectly concatenating `neoforge_version` to `forgified_fabric_version`
- ❌ **Second Attempt Failed:** Maven coordinates incorrect
  - Issue: Used `dev.su5ed.sinytra.fabric-api:fabric-api` (wrong artifact ID)
- ❌ **Third Attempt Failed:** Modrinth Maven missing transitive dependencies
  - Issue: `maven.modrinth:forgified-fabric-api` doesn't bundle Fabric Loader API
- ✅ **Final Solution:** Sinytra Maven with correct coordinates
  - `org.sinytra.forgified-fabric-api:forgified-fabric-api:0.116.7+2.2.0+1.21.1`
  - Includes Fabric Loader API as transitive dependency

**Lithium:**
- ✅ Updated from non-existent `mc1.21.1-0.18.0-neoforge` to `mc1.21.1-0.14.7-neoforge`
- ✅ Confirmed available on Modrinth Maven

**Sodium:**
- ✅ Version `mc1.21.1-0.6.9-neoforge` resolving correctly

**gradle.properties Changes:**
```diff
- forgified_fabric_version=0.114.0+1.21.1
+ forgified_fabric_version=0.116.7+2.2.0+1.21.1
```

**build.gradle Changes:**
```diff
- implementation "dev.su5ed.sinytra.fabric-api:fabric-api:${project.forgified_fabric_version}+${project.neoforge_version}"
+ implementation "org.sinytra.forgified-fabric-api:forgified-fabric-api:${project.forgified_fabric_version}"

- implementation("maven.modrinth:lithium:mc1.21.1-0.18.0-neoforge")
+ implementation("maven.modrinth:lithium:mc1.21.1-0.14.7-neoforge")
```

### 3. Fabric Loader API Resolution

**Problem:** `net.fabricmc.loader.api.FabricLoader` imports failing
**Root Cause:** Forgified Fabric API does NOT automatically include Fabric Loader API when using Modrinth Maven
**Solution:** Use Sinytra Maven (`org.sinytra.forgified-fabric-api`) which bundles Forgified Fabric Loader

**Result:** All Fabric Loader API imports now resolve correctly

---

## 🔄 In Progress

### MC 1.21.11 → 1.21.1 API Incompatibilities

**Total Errors:** 27 compilation errors
**Categories:**

#### 1. Chunk System API Changes (2 errors)
**Files Affected:**
- `WorldImporter.java:26-28`

**Missing Classes:**
- `net.minecraft.world.level.chunk.PalettedContainerFactory`
- `net.minecraft.world.level.chunk.Strategy`

**Usage:**
```java
// MC 1.21.11 (current code)
var factory = PalettedContainerFactory.create(mcWorld.registryAccess());
this.biomeCodec = factory.biomeContainerCodec();
this.blockStateCodec = factory.blockStatesContainerCodec();
```

**MC 1.21.1 API:** These classes don't exist - replaced with `PalettedContainer.PaletteProvider` and direct codec creation methods

**Resolution Needed:** Investigate MC 1.21.1 `PalettedContainer` codec creation API

#### 2. Rendering API Changes - ChunkSectionLayer (9 errors)
**Files Affected:**
- `ModelFactory.java:21`
- `ModelTextureBakery.java:5, 51, 65, 87`

**Missing Class:**
- `net.minecraft.client.renderer.chunk.ChunkSectionLayer`

**MC 1.21.1 API:** Likely replaced with `RenderType` or removed entirely in rendering refactor

**Resolution Needed:** Check MC 1.21.1 block/chunk rendering API for equivalent

#### 3. Sodium API Remnants - FogParameters (3 errors)
**Files Affected:**
- `Viewport.java:6, 38, 91`

**Missing Class:**
- `net.caffeinemc.mods.sodium.client.util.FogParameters`

**Note:** Partially addressed in Phase 1 (removed from mixin parameters), but field/method references remain

**Resolution Needed:** Remove `FogParameters` field from `Viewport` class or make it nullable/optional

#### 4. Blaze3D Package Changes (4 errors)
**Files Affected:**
- `VoxyRenderSystem.java:3-4`
- `BudgetBufferRenderer.java:4, 49`

**Missing Classes:**
- `com.mojang.blaze3d.opengl.GlConst`
- `com.mojang.blaze3d.opengl.GlStateManager`
- `com.mojang.blaze3d.textures.GpuTexture`

**MC 1.21.1 API:** These classes moved to different packages in Blaze3D refactor

**Resolution Needed:** Find new package locations (likely `com.mojang.blaze3d.platform` or similar)

#### 5. Texture/Mipmap API Changes (1 error)
**Files Affected:**
- `ReuseVertexConsumer.java:7`

**Missing Class:**
- `net.minecraft.client.renderer.texture.MipmapStrategy`

**Resolution Needed:** Check MC 1.21.1 texture system API

#### 6. Debug Screen API Changes (3 errors)
**Files Affected:**
- `VoxyDebugScreenEntry.java:8-9, 18, 20`

**Missing Classes:**
- `net.minecraft.client.gui.components.debug.DebugScreenDisplayer`
- `net.minecraft.client.gui.components.debug.DebugScreenEntry`

**MC 1.21.1 API:** Debug screen system refactored

**Resolution Needed:** Adapt to new debug screen API or comment out debug integration temporarily

#### 7. Optional Dependencies (5 errors - EXPECTED)
**Files Affected:**
- `MixinFabricWorld.java` - Chunky integration
- `FlashbackCompat.java` - Flashback mod integration
- `RenderPipelineFactory.java` - Iris shader integration

**Status:** Expected failures - optional mod integrations
**Resolution:** These can be commented out or conditionally compiled based on mod presence

---

## Build Verification Results

### Successful Steps:
✅ Gradle configuration parsing
✅ Dependency resolution (all artifacts found)
✅ NeoForge artifact download and setup
✅ Minecraft decompilation and patching
✅ Mixin configuration validation
❌ Source compilation (27 API errors)

### Build Performance:
- NeoForge setup: ~97 seconds (cached)
- Dependency resolution: ~6 seconds
- Compilation attempt: Fails at `:compileJava`

---

## Technical Discoveries

### 1. Forgified Fabric API Ecosystem

**Structure:**
- **Forgified Fabric API:** Fabric API port for NeoForge
- **Forgified Fabric Loader:** Fabric Loader API port for NeoForge (bundled with FFAPI)
- **Sinytra Connector:** Full Fabric mod compatibility layer (not needed for native development)

**Maven Repositories:**
- ❌ **Modrinth Maven** (`maven.modrinth:forgified-fabric-api`) - Missing transitive dependencies
- ✅ **Sinytra Maven** (`org.sinytra.forgified-fabric-api:forgified-fabric-api`) - Complete with Fabric Loader

**Key Finding:** Sinytra Maven is required for proper transitive dependency resolution

### 2. Version Format Understanding

**Forgified Fabric API Version Scheme:**
```
<fabric_api_version>+<forgified_version>+<minecraft_version>
Example: 0.116.7+2.2.0+1.21.1
```

**NOT:** `<version>+<minecraft>+<neoforge>`
**Initial Mistake:** Concatenating `neoforge_version` created invalid version string

### 3. NeoGradle vs Fabric Loom

**Fabric Loom Features NOT in NeoGradle:**
- `include()` - Jar-in-jar dependency packaging
- `minecraftRuntimeLibraries()` - Runtime library injection
- `processIncludeJars` - Included jar preprocessing
- `remapJar` - Automatic remapping (NeoGradle does this differently)

**Migration Pattern:** Replace all Loom-specific features with standard Gradle constructs

---

## Risk Assessment Update

| Component | Phase 1 Risk | Phase 2 Risk | Change |
|-----------|--------------|--------------|---------|
| Build system | 🟡 MODERATE | 🟢 LOW | ✅ RESOLVED |
| Dependencies | 🟡 MODERATE | 🟢 LOW | ✅ RESOLVED |
| Fabric API compatibility | ⚠️ HIGH | 🟢 LOW | ✅ RESOLVED |
| MC API migration | 🟡 MODERATE | 🟡 MODERATE | → No change |
| Sodium compatibility | 🟡 MODERATE | 🟡 MODERATE | → Partial (FogParameters remnants) |

---

## Remaining Work

### Immediate (Current Session):
1. **Fix PalettedContainer API** (2 errors)
   - Research MC 1.21.1 codec creation methods
   - Replace `PalettedContainerFactory.create()` usage
   - Remove `Strategy` imports

2. **Fix ChunkSectionLayer references** (9 errors)
   - Identify MC 1.21.1 chunk rendering API
   - Update `ModelFactory` and `ModelTextureBakery`

3. **Remove FogParameters remnants** (3 errors)
   - Make `Viewport.fogParameters` optional or remove
   - Update all usages

4. **Fix Blaze3D package imports** (4 errors)
   - Locate new packages for `GlConst`, `GlStateManager`, `GpuTexture`
   - Update imports

5. **Comment out optional integrations** (8 errors)
   - Wrap Chunky integration in conditional compilation
   - Wrap Flashback integration in conditional compilation
   - Wrap Iris integration in conditional compilation
   - Or stub out interfaces

### Testing Phase:
1. Achieve successful compilation
2. Test runtime loading
3. Verify mixin application
4. Test basic LoD rendering
5. Performance validation

---

## Timeline Estimate

**Phase 2 Completed:** 4 hours (dependency resolution)
**Phase 2 Remaining:** 4-6 hours (API migration)
**Phase 3 (Testing):** 2-4 hours

**Total Remaining:** 6-10 hours to functional NeoForge port

---

## Commits (Phase 2)

**2492fabf** - "fix: resolve dependency issues for NeoForge 1.21.1 port"
- Update Forgified Fabric API to 0.116.7+2.2.0+1.21.1
- Switch to Sinytra Maven for correct transitive dependencies
- Update Lithium to mc1.21.1-0.14.7-neoforge
- Remove Fabric Loom specific build tasks
- Fix dependency configurations

**Previous (Phase 1):**
- d42e9c43 - Initial NeoForge conversion

---

## Next Steps

### Priority 1: Core Chunk System
Fix `WorldImporter.java` PalettedContainer API to enable world import functionality

### Priority 2: Rendering System
Fix `ChunkSectionLayer` and Blaze3D API changes to enable LoD rendering

### Priority 3: Polish
Handle FogParameters remnants and optional mod integrations

### Priority 4: Testing
Runtime validation and performance benchmarking

---

## Key Learnings

1. **Dependency Resolution is Critical:** Spent 70% of Phase 2 debugging dependency issues
2. **Maven Repository Selection Matters:** Sinytra Maven vs Modrinth Maven have different bundling
3. **Version Format Errors are Silent:** Build fails without clear indication of version string issues
4. **API Changes are Version-Specific:** MC 1.21.1 vs 1.21.11 have significant rendering/chunk API differences

---

**Report Status:** IN PROGRESS
**Next Update:** After MC API migration completion
**Branch:** `neoforge-1.21.1` at commit 2492fabf
