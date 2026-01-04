package me.cortex.voxy.client.mixin.minecraft;

import com.mojang.blaze3d.systems.RenderSystem;
import me.cortex.voxy.client.config.VoxyConfig;
import me.cortex.voxy.client.core.IGetVoxyRenderSystem;
import net.minecraft.client.Camera;
import net.minecraft.client.renderer.FogRenderer;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * MC 1.21.1 compatible fog mixin.
 * Disables render distance fog when Voxy is active by pushing fog distance to infinity.
 */
@Mixin(FogRenderer.class)
public class MixinFogRenderer {
    /**
     * Inject at the end of setupFog to override the fog parameters after vanilla sets them.
     * MC 1.21.1 setupFog signature: (Camera, FogMode, float farPlaneDistance, boolean, float partialTick)
     */
    @Inject(method = "setupFog", at = @At("TAIL"))
    private static void voxy$disableFog(Camera camera, FogRenderer.FogMode fogMode, float farPlaneDistance,
                                         boolean shouldCreateFog, float partialTick, CallbackInfo ci) {
        if (!(VoxyConfig.CONFIG.enableRendering && VoxyConfig.CONFIG.enabled)) return;

        var vrs = IGetVoxyRenderSystem.getNullable();
        if (vrs == null) return;

        // Only disable terrain fog, not sky fog (sky fog affects sky rendering)
        if (fogMode == FogRenderer.FogMode.FOG_TERRAIN) {
            // Push fog to effectively infinite distance
            RenderSystem.setShaderFogStart(Float.MAX_VALUE);
            RenderSystem.setShaderFogEnd(Float.MAX_VALUE);
        }
    }
}
