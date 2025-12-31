# NeoForge 1.21.1 Port - Phase 3 Progress Report

**Date**: 2025-12-31
**Phase**: API Compatibility & Optional Integration Exclusions
**Status**: IN PROGRESS - Core MC API migrations remaining

## Overview

Phase 3 focused on Sodium 0.6.x API compatibility and systematically excluding optional mod integrations that are not available for NeoForge 1.21.1. Significant progress made in reducing compilation errors from optional dependencies.

## Completed Work

### 1. Sodium 0.6.x API Compatibility ✅

**FogParameters Removal** (Removed in Sodium 0.6.x):
- `Viewport.java`: Commented out FogParameters import and field
- `Viewport.java`: Disabled `setFogParameters()` method (lines 94-100)
- `NormalRenderPipeline.java`: Disabled environmental fog rendering (lines 107-125)
- `VoxyRenderSystem.java`: Removed FogParameters parameter from `setupViewport()` method
- `VoxyRenderSystem.java`: Removed `.setFogParameters(fogParameters)` call (line 207-208)

**Impact**: Fog rendering disabled until Sodium 0.6.x fog API documented and implemented

### 2. Optional Integration Exclusions ✅

Added comprehensive `sourceSets` exclusions in `build.gradle` to prevent compilation of unavailable integrations:

#### Iris Shader Integration
- `me/cortex/voxy/client/iris/**` (entire package)
- `IrisVoxyRenderPipeline.java`
- `IrisUtil.java`
- `me/cortex/voxy/client/mixin/iris/**`

**Files Excluded**: 7 source files + 2 mixin files
**Errors Resolved**: ~25+ Iris-related compilation errors

#### Flashback Recording Integration
- `me/cortex/voxy/client/mixin/flashback/**`

**Reason**: Flashback mod not available for NeoForge 1.21.1

#### Nvidium Renderer Integration
- `me/cortex/voxy/client/mixin/nvidium/**`

**Reason**: Nvidium integration compatibility unclear

#### ModMenu Integration (Fabric-only)
- `ModMenuIntegration.java`

**Reason**: ModMenu is Fabric-only, no NeoForge equivalent

#### Vivecraft VR Integration
- `ViewportSelector.java`

**Reason**: Vivecraft API not available for NeoForge 1.21.1

#### Sodium Config API (Changed in 0.6.x)
- `SodiumConfigBuilder.java`
- `VoxyConfigMenu.java`
- `IConfigPageSetter.java`
- `MixinVideoSettingsScreen.java`

**Reason**: Sodium config API significantly changed between 0.8.x and 0.6.x

#### Debug Screen API (Changed in MC 1.21.1)
- `VoxyDebugScreenEntry.java`
- `MixinDebugScreenEntryList.java`

**Reason**: `net.minecraft.client.gui.components.debug` package API changes

### 3. Code Cleanup ✅

**RenderPipelineFactory.java**:
- Commented out IrisUtil import
- Disabled Iris pipeline creation check
- Preserved createIrisPipeline() method structure for future re-enabling

## Current Compilation Status

```
Total Errors: 200
Unique Files with Errors: 38
```

### Error Distribution by File (Top 10)

| File | Error Count | Category |
|------|-------------|----------|
| ModelFactory.java | 19 | ChunkSectionLayer API |
| WorldImporter.java | 18 | PalettedContainer API |
| ModelTextureBakery.java | 16 | ChunkSectionLayer API |
| DHImporter.java | 7 | Registry API |
| Mapper.java | 7 | BlockState API |
| MixinFogRenderer.java | 6 | Fog Renderer API |
| WorldConversionFactory.java | 4 | PalettedContainer.Data access |
| VoxyClient.java | 4 | Debug Screen + jspecify |
| VoxyRenderSystem.java | 3 | Excluded class references |
| WorldIdentifier.java | 3 | Identifier → ResourceLocation |

## Remaining Work

### Category 1: ChunkSectionLayer API Migration (High Priority)
**Impact**: 35+ errors across 2 files

**Affected Files**:
- `ModelFactory.java` (19 errors)
- `ModelTextureBakery.java` (16 errors)

**Issue**: `net.minecraft.client.renderer.chunk.ChunkSectionLayer` import failing

**Investigation Needed**:
- Determine if ChunkSectionLayer exists in MC 1.21.1
- Check if it was renamed, moved, or removed
- Identify replacement API if removed
- Update all usages throughout codebase

**Code Locations**:
- ModelFactory.java:21 (import)
- ModelFactory.java:76, 268, 413, 418, 425, 487, 523, 543 (usage)
- ModelTextureBakery.java:5 (import)
- ModelTextureBakery.java:51, 65, 87 (usage)

### Category 2: PalettedContainer API Migration (High Priority)
**Impact**: 22+ errors across 2 files

**Affected Files**:
- `WorldImporter.java` (18 errors)
- `WorldConversionFactory.java` (4 errors)

**Issues**:
1. `PalettedContainer.Data` class inaccessible (access transformer not working)
2. `Data.palette` field access denied
3. `Data.storage` field access denied

**Root Cause**: MC 1.21.1 likely made PalettedContainer.Data package-private or changed internal structure

**Investigation Needed**:
- Check MC 1.21.1 PalettedContainer source for Data class visibility
- Verify access transformer configuration in `accesstransformer.cfg`
- Identify alternative API for palette/storage access if Data class removed
- Consider reflection-based access as temporary workaround

**Access Transformer Current Config**:
```
public net.minecraft.world.level.chunk.PalettedContainer data
public net.minecraft.world.level.chunk.PalettedContainer$Data palette
public net.minecraft.world.level.chunk.PalettedContainer$Data storage
```

### Category 3: Minecraft API Migrations (Medium Priority)
**Impact**: 20+ errors across multiple files

#### 3a. Fog Renderer API (MixinFogRenderer.java - 6 errors)
- `net.minecraft.client.renderer.fog.FogData` package not found
- `net.minecraft.client.renderer.fog.FogRenderer` package not found

**Likely Cause**: Fog rendering refactored in MC 1.21.1

#### 3b. BlockState API Changes (Mapper.java - 7 errors)
- `BlockStateBase.getLightBlock()` method signature changed
- Unknown symbol errors at multiple lines (261, 360, 380, 383, 387, 431, 434)

#### 3c. Registry API Changes (DHImporter.java - 7 errors)
- `RegistryLookup<T>` vs `Registry<Biome>` type mismatch (line 102)
- Incompatible types in registry access

#### 3d. Identifier → ResourceLocation Migration (WorldIdentifier.java - 3 errors)
- Lines 56, 120: Symbol not found
- Likely using Fabric's `Identifier` instead of Mojang's `ResourceLocation`

#### 3e. Blaze3D Package Changes
- `BudgetBufferRenderer.java`: `com.mojang.blaze3d.textures` package not found (GpuTexture)
- `MixinGlDebug.java`: `com.mojang.blaze3d.opengl.GlDebug` not found

#### 3f. Other API Changes
- `VoxyClient.java`: `org.jspecify.annotations` package not found (line 21)
- `TextureUtils.java`: Unknown symbol (line 5)
- `ReuseVertexConsumer.java`: MipmapStrategy symbol not found (line 7)
- `MixinRenderSystem.java`: Unknown symbols (lines 4, 5, 21)
- `MixinLevelRenderer.java`: Unknown symbol (line 7)
- `MixinDefaultChunkRenderer.java`: Unknown symbol (line 6)
- `VoxelIngestService.java`: Unknown symbols (lines 103, 118, 141)

### Category 4: Cleanup and References (Low Priority)
**Impact**: 5+ errors

**VoxyRenderSystem.java** (3 errors):
- Lines 17, 31, 70: References to excluded classes (IrisUtil, ViewportSelector)
- Need to stub out or remove these references

**VoxyClient.java** (4 errors):
- Debug screen API imports (lines 15, 16, 17)
- jspecify annotations (line 21)

## Risk Assessment

### High Risk Items
1. **ChunkSectionLayer Removal**: If this class was removed entirely in MC 1.21.1, significant refactoring required
2. **PalettedContainer.Data Access**: Core voxel ingestion depends on palette/storage access - critical functionality
3. **Fog Renderer Refactor**: May require understanding new fog system architecture

### Medium Risk Items
1. **BlockState API Changes**: Lighting calculations may need updates
2. **Registry API Evolution**: Biome registry access patterns changed

### Low Risk Items
1. **Package Moves**: Most Blaze3D and other package moves are mechanical renames
2. **Reference Cleanup**: Straightforward to stub out excluded class references

## Next Steps

### Immediate Actions (Phase 3 Continuation)
1. ✅ Document Phase 3 progress
2. ⏺ **Investigate ChunkSectionLayer API**:
   - Search MC 1.21.1 source for ChunkSectionLayer existence
   - Check Sodium 0.6.x documentation for rendering layer changes
   - Determine replacement API path

3. ⏺ **Investigate PalettedContainer.Data access**:
   - Verify Data class visibility in MC 1.21.1
   - Test access transformer effectiveness
   - Research alternative palette access methods

4. ⏺ **Fix mechanical package moves**:
   - Blaze3D package reorganizations
   - Fog renderer package moves
   - Other simple imports

5. ⏺ **Stub out remaining excluded class references**:
   - VoxyRenderSystem IrisUtil/ViewportSelector usage
   - VoxyClient debug screen imports

### Long-term Actions (Phase 4)
1. Re-enable optional integrations as NeoForge versions become available
2. Implement Sodium 0.6.x fog API when documented
3. Runtime testing and debugging
4. Performance validation

## Lessons Learned

1. **Systematic Exclusion Effective**: Excluding unavailable integrations significantly reduced noise in error logs
2. **Optional vs Core Separation**: Clean separation between optional integrations and core functionality critical for porting
3. **API Documentation Gaps**: Sodium 0.6.x API changes not well-documented; requires source inspection
4. **Access Transformers Fragile**: MC internal class visibility changes break previously working access patterns

## Files Modified This Phase

- `build.gradle` - Added sourceSets exclusions for optional integrations
- `Viewport.java` - FogParameters removal
- `NormalRenderPipeline.java` - Fog rendering disabled
- `VoxyRenderSystem.java` - FogParameters parameter removed
- `RenderPipelineFactory.java` - IrisUtil references removed

## Commits

- `2e976e1e` - Phase 3: Sodium 0.6.x API compatibility + optional integration exclusions

---

**Status Summary**: Phase 3 successfully reduced optional integration noise. Core MC API migrations (ChunkSectionLayer, PalettedContainer, Fog Renderer) remain as primary blockers. Estimated ~200 errors remain, primarily concentrated in rendering and world import subsystems.
