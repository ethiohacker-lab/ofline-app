package com.example.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = DarkEmeraldPrimary,
    onPrimary = Color(0xFF072116),
    primaryContainer = DarkSageContainer,
    onPrimaryContainer = Color(0xFFB7E4C7),
    secondary = DarkAmberSecondary,
    onSecondary = Color(0xFF2D1C04),
    secondaryContainer = DarkWarmContainer,
    onSecondaryContainer = Color(0xFFFCE7C3),
    tertiary = DarkCobaltTertiary,
    onTertiary = Color(0xFF08222D),
    tertiaryContainer = DarkCobaltContainer,
    onTertiaryContainer = Color(0xFFCDEAF7),
    background = DarkForestBg,
    onBackground = DarkInk,
    surface = DarkForestSurface,
    onSurface = DarkInk,
    surfaceVariant = DarkForestVariant,
    onSurfaceVariant = DarkInkMuted,
    outline = DarkOutline,
)

private val LightColorScheme = lightColorScheme(
    primary = ForestEmerald,
    onPrimary = Color.White,
    primaryContainer = SageContainer,
    onPrimaryContainer = OnSageContainer,
    secondary = TerracottaGold,
    onSecondary = Color.White,
    secondaryContainer = WarmSandContainer,
    onSecondaryContainer = OnWarmSand,
    tertiary = CobaltCircuit,
    onTertiary = Color.White,
    tertiaryContainer = CobaltContainer,
    onTertiaryContainer = OnCobaltContainer,
    background = ParchmentBg,
    onBackground = InkSlate,
    surface = ParchmentSurface,
    onSurface = InkSlate,
    surfaceVariant = ParchmentVariant,
    onSurfaceVariant = InkMuted,
    outline = OutlineSubtle,
)

@Composable
fun MeklitAiTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = MeklitTypography,
        content = content,
    )
}
