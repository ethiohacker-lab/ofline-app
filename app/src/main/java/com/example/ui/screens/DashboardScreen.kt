package com.example.ui.screens

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.animateIntAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.AutoAwesome
import androidx.compose.material.icons.rounded.Bolt
import androidx.compose.material.icons.rounded.ChatBubble
import androidx.compose.material.icons.rounded.CloudDone
import androidx.compose.material.icons.rounded.CloudDownload
import androidx.compose.material.icons.rounded.Dataset
import androidx.compose.material.icons.rounded.Eco
import androidx.compose.material.icons.rounded.Functions
import androidx.compose.material.icons.rounded.Memory
import androidx.compose.material.icons.rounded.OfflineBolt
import androidx.compose.material.icons.rounded.Psychology
import androidx.compose.material.icons.rounded.Quiz
import androidx.compose.material.icons.rounded.Storage
import androidx.compose.material.icons.rounded.Summarize
import androidx.compose.material.icons.rounded.Terminal
import androidx.compose.material.icons.rounded.Translate
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.R
import com.example.ui.AiUiState
import com.example.ui.theme.AmberLeaf
import com.example.ui.theme.CobaltCircuit
import com.example.ui.theme.ForestEmerald
import com.example.ui.theme.ForestEmeraldLight
import com.example.ui.theme.MonoFontFamily
import com.example.ui.theme.TerracottaGold
import java.text.NumberFormat
import java.util.Locale

private data class DonutSlice(
    val label: String,
    val count: Int,
    val color: Color,
)

private data class DemoQueryChip(
    val label: String,
    val domain: String,
    val query: String,
    val icon: ImageVector,
)

@Composable
fun DashboardScreen(
    uiState: AiUiState,
    onOpenChat: () -> Unit,
    onRunQueryInChat: (String) -> Unit,
    onPrefillSummarizer: () -> Unit,
    onOpenTeach: () -> Unit,
    onOpenGather: () -> Unit,
    onOpenVault: () -> Unit,
) {
    val stats = uiState.stats
    val vault = stats.vault
    val animatedTotal by animateIntAsState(
        targetValue = stats.combinedOfflineRecords,
        animationSpec = tween(durationMillis = 850),
        label = "totalRecordsAnim",
    )
    val formattedTotal = NumberFormat.getIntegerInstance(Locale.US).format(animatedTotal)

    val demoChips = listOf(
        DemoQueryChip("Ethiopic 'ሀ' (U+1200)", "1M+ Vault", "unicode 4608", Icons.Rounded.Translate),
        DemoQueryChip("HTTPS Port 443", "1M+ Vault", "port 443", Icons.Rounded.Terminal),
        DemoQueryChip("Hardy-Ramanujan 1729", "1M+ Vault", "number 1729", Icons.Rounded.Functions),
        DemoQueryChip("Urea for 2 Timad", "Horticulture", "fertilizer urea 100 kg/ha 2 timad", Icons.Rounded.Eco),
        DemoQueryChip("2×2 Matrix Inverse", "Math NumPy", "matrix [[2,1],[5,3]]", Icons.Rounded.Memory),
        DemoQueryChip("Define Resilience", "English", "define resilience", Icons.Rounded.AutoAwesome),
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background),
        contentAlignment = Alignment.TopCenter,
    ) {
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .widthIn(max = 760.dp),
            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 14.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            // 1. Hero Command Center Banner
            item {
                HeroCommandCard(
                    formattedTotal = formattedTotal,
                    isOnline = uiState.isOnline,
                    isInitializing = uiState.isInitializing,
                    vaultProgress = vault.progress,
                    vaultIsComplete = vault.isComplete,
                    vaultStage = vault.stage,
                    vaultSizeMb = vault.sizeMb,
                    onOpenChat = onOpenChat,
                )
            }

            // 2. Superpowers 2x3 Bento Grid
            item {
                Text(
                    text = "Maya Superpowers",
                    style = MaterialTheme.typography.titleLarge,
                    modifier = Modifier.padding(top = 2.dp),
                )
            }

            item {
                Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        SuperpowerTile(
                            title = "Ask Maya AI",
                            subtitle = "Chat, English & Math",
                            icon = Icons.Rounded.ChatBubble,
                            accent = ForestEmeraldLight,
                            onClick = onOpenChat,
                            modifier = Modifier
                                .weight(1f)
                                .testTag("dash_ask_maya"),
                        )
                        SuperpowerTile(
                            title = "1M+ Data Vault",
                            subtitle = "Browse 1,050,000+ rows",
                            icon = Icons.Rounded.Dataset,
                            accent = CobaltCircuit,
                            onClick = onOpenVault,
                            modifier = Modifier
                                .weight(1f)
                                .testTag("dash_open_vault"),
                        )
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        SuperpowerTile(
                            title = "Summarizer",
                            subtitle = "NumPy TextRank bullets",
                            icon = Icons.Rounded.Summarize,
                            accent = TerracottaGold,
                            onClick = onPrefillSummarizer,
                            modifier = Modifier
                                .weight(1f)
                                .testTag("dash_summarizer"),
                        )
                        SuperpowerTile(
                            title = "Study Quiz",
                            subtitle = "Offline active recall",
                            icon = Icons.Rounded.Quiz,
                            accent = Color(0xFF6B4C9A),
                            onClick = { onRunQueryInChat("quiz me") },
                            modifier = Modifier
                                .weight(1f)
                                .testTag("dash_quiz"),
                        )
                    }

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                    ) {
                        SuperpowerTile(
                            title = "Sync Web → Offline",
                            subtitle = if (uiState.isOnline) "Wikipedia & Dictionary" else "Offline (view cached)",
                            icon = Icons.Rounded.CloudDownload,
                            accent = Color(0xFF1E6091),
                            onClick = onOpenGather,
                            modifier = Modifier
                                .weight(1f)
                                .testTag("dash_sync_web"),
                        )
                        SuperpowerTile(
                            title = "Teach Maya",
                            subtitle = "Save custom Q&A forever",
                            icon = Icons.Rounded.Psychology,
                            accent = Color(0xFF9E2A2B),
                            onClick = onOpenTeach,
                            modifier = Modifier
                                .weight(1f)
                                .testTag("dash_teach"),
                        )
                    }
                }
            }

            // 3. Knowledge Distribution Donut Chart + Telemetry
            item {
                KnowledgeDistributionCard(uiState = uiState)
            }

            // 4. Telemetry Bento Row
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    TelemetryTile(
                        value = "${vault.sizeMb} MB",
                        label = "SQLite Vault",
                        icon = Icons.Rounded.Storage,
                        modifier = Modifier.weight(1f),
                    )
                    TelemetryTile(
                        value = "${stats.learnedCount + stats.onlineCachedCount}",
                        label = "Learned + Web",
                        icon = Icons.Rounded.Bolt,
                        modifier = Modifier.weight(1f),
                    )
                    TelemetryTile(
                        value = "${stats.vocabSize}",
                        label = "TF-IDF Terms",
                        icon = Icons.Rounded.Memory,
                        modifier = Modifier.weight(1f),
                    )
                    TelemetryTile(
                        value = "${stats.avgReinforcement}×",
                        label = "Avg Boost",
                        icon = Icons.Rounded.AutoAwesome,
                        modifier = Modifier.weight(1f),
                    )
                }
            }

            // 5. Instant Vault & Calculator Triggers
            item {
                Text(
                    text = "Instant 1M+ Vault & Engine Demos",
                    style = MaterialTheme.typography.titleMedium,
                )
                Spacer(Modifier.height(8.dp))
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState()),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    demoChips.forEach { chip ->
                        Card(
                            onClick = { onRunQueryInChat(chip.query) },
                            shape = RoundedCornerShape(18.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
                            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.35f)),
                            modifier = Modifier
                                .width(190.dp)
                                .testTag("dash_demo_${chip.label.lowercase().replace(" ", "_")}"),
                        ) {
                            Column(
                                modifier = Modifier.padding(14.dp),
                                verticalArrangement = Arrangement.spacedBy(6.dp),
                            ) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                                ) {
                                    Icon(
                                        imageVector = chip.icon,
                                        contentDescription = null,
                                        modifier = Modifier.size(16.dp),
                                        tint = MaterialTheme.colorScheme.primary,
                                    )
                                    Text(
                                        text = chip.domain,
                                        style = MaterialTheme.typography.labelSmall,
                                        color = MaterialTheme.colorScheme.primary,
                                    )
                                }
                                Text(
                                    text = chip.label,
                                    style = MaterialTheme.typography.titleMedium,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis,
                                )
                                Text(
                                    text = chip.query,
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                    maxLines = 1,
                                    overflow = TextOverflow.Ellipsis,
                                )
                            }
                        }
                    }
                }
            }

            item { Spacer(Modifier.height(8.dp)) }
        }
    }
}

@Composable
private fun HeroCommandCard(
    formattedTotal: String,
    isOnline: Boolean,
    isInitializing: Boolean,
    vaultProgress: Float,
    vaultIsComplete: Boolean,
    vaultStage: String,
    vaultSizeMb: Double,
    onOpenChat: () -> Unit,
) {
    Card(
        onClick = onOpenChat,
        shape = RoundedCornerShape(26.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
        modifier = Modifier
            .fillMaxWidth()
            .testTag("dash_hero_card"),
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(
                    Brush.linearGradient(
                        colors = listOf(
                            ForestEmerald,
                            Color(0xFF153833),
                            CobaltCircuit,
                        )
                    )
                ),
        ) {
            Image(
                painter = painterResource(id = R.drawable.img_hero_scholar),
                contentDescription = null,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .matchParentSize()
                    .alpha(0.16f),
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(20.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        Text(
                            text = "Maya AI",
                            style = MaterialTheme.typography.titleLarge,
                            color = Color.White,
                        )
                        Surface(
                            shape = RoundedCornerShape(50),
                            color = AmberLeaf.copy(alpha = 0.22f),
                        ) {
                            Text(
                                text = "NUMPY + SQLITE",
                                style = MaterialTheme.typography.labelSmall,
                                color = AmberLeaf,
                                modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                            )
                        }
                    }

                    Surface(
                        shape = RoundedCornerShape(50),
                        color = if (isOnline) Color(0xFF2D6A4F) else Color.White.copy(alpha = 0.16f),
                    ) {
                        Row(
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(5.dp),
                        ) {
                            Icon(
                                imageVector = if (isOnline) Icons.Rounded.CloudDone else Icons.Rounded.OfflineBolt,
                                contentDescription = null,
                                modifier = Modifier.size(13.dp),
                                tint = Color.White,
                            )
                            Text(
                                text = if (isOnline) "ONLINE SYNC" else "OFFLINE",
                                style = MaterialTheme.typography.labelSmall,
                                color = Color.White,
                            )
                        }
                    }
                }

                Column(verticalArrangement = Arrangement.spacedBy(2.dp)) {
                    Text(
                        text = if (isInitializing) "Booting…" else formattedTotal,
                        style = MaterialTheme.typography.headlineMedium.copy(
                            fontFamily = MonoFontFamily,
                            fontWeight = FontWeight.Bold,
                        ),
                        color = AmberLeaf,
                    )
                    Text(
                        text = "Indexed Offline Knowledge Records Ready On-Device",
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color.White.copy(alpha = 0.88f),
                    )
                }

                // Live Vault Hydration Bar
                Column(verticalArrangement = Arrangement.spacedBy(5.dp)) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                    ) {
                        Text(
                            text = vaultStage,
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.White.copy(alpha = 0.85f),
                        )
                        Text(
                            text = if (vaultIsComplete) "$vaultSizeMb MB" else "${(vaultProgress * 100).toInt()}%",
                            style = MaterialTheme.typography.labelSmall,
                            color = AmberLeaf,
                        )
                    }
                    LinearProgressIndicator(
                        progress = { if (vaultIsComplete) 1f else vaultProgress.coerceIn(0.02f, 1f) },
                        color = AmberLeaf,
                        trackColor = Color.White.copy(alpha = 0.2f),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(6.dp)
                            .clip(RoundedCornerShape(50)),
                    )
                }
            }
        }
    }
}

@Composable
private fun SuperpowerTile(
    title: String,
    subtitle: String,
    icon: ImageVector,
    accent: Color,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        onClick = onClick,
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.35f)),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp),
        modifier = modifier.height(106.dp),
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(14.dp),
            verticalArrangement = Arrangement.SpaceBetween,
        ) {
            Box(
                modifier = Modifier
                    .size(38.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(accent.copy(alpha = 0.14f)),
                contentAlignment = Alignment.Center,
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = accent,
                    modifier = Modifier.size(21.dp),
                )
            }
            Column {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
    }
}

@Composable
private fun KnowledgeDistributionCard(uiState: AiUiState) {
    val stats = uiState.stats
    val vaultDom = stats.vault.domainCounts

    val mathCount = (vaultDom["Math"] ?: 0) + (stats.categories["Math"] ?: 0)
    val csCount = (vaultDom["Computer Science"] ?: 0) + (stats.categories["Computer Science"] ?: 0)
    val hortCount = (vaultDom["Horticulture"] ?: 0) + (stats.categories["Horticulture"] ?: 0)
    val engCount = (vaultDom["English"] ?: 0) + (stats.categories["English"] ?: 0)
    val otherCount = (stats.categories["General"] ?: 0) + (stats.categories["Learned"] ?: 0)

    val slices = listOf(
        DonutSlice("Math", mathCount.coerceAtLeast(1), ForestEmeraldLight),
        DonutSlice("Comp Sci", csCount.coerceAtLeast(1), CobaltCircuit),
        DonutSlice("Horticulture", hortCount.coerceAtLeast(1), TerracottaGold),
        DonutSlice("English", engCount.coerceAtLeast(1), AmberLeaf),
        DonutSlice("General", otherCount.coerceAtLeast(1), Color(0xFF7B6D8D)),
    )
    val total = slices.sumOf { it.count }.coerceAtLeast(1).toFloat()
    val animatedSweep by animateFloatAsState(
        targetValue = 360f,
        animationSpec = tween(durationMillis = 900),
        label = "donutSweep",
    )

    Card(
        shape = RoundedCornerShape(22.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.35f)),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(18.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = "Knowledge Distribution",
                    style = MaterialTheme.typography.titleMedium,
                )
                Text(
                    text = "4 Core Domains",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary,
                )
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(18.dp),
            ) {
                Box(
                    modifier = Modifier.size(126.dp),
                    contentAlignment = Alignment.Center,
                ) {
                    Canvas(modifier = Modifier.fillMaxSize().padding(8.dp)) {
                        val strokeW = 18.dp.toPx()
                        val diameter = size.minDimension - strokeW
                        val topLeft = Offset(
                            (size.width - diameter) / 2f,
                            (size.height - diameter) / 2f,
                        )
                        val arcSize = Size(diameter, diameter)
                        var startAngle = -90f
                        slices.forEach { slice ->
                            val sweep = (slice.count / total) * animatedSweep
                            if (sweep > 1.5f) {
                                drawArc(
                                    color = slice.color,
                                    startAngle = startAngle,
                                    sweepAngle = (sweep - 2f).coerceAtLeast(1f),
                                    useCenter = false,
                                    topLeft = topLeft,
                                    size = arcSize,
                                    style = Stroke(width = strokeW, cap = StrokeCap.Round),
                                )
                            }
                            startAngle += sweep
                        }
                    }
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = if (stats.vault.isComplete) "1.05M+" else "${stats.totalEntries}",
                            style = MaterialTheme.typography.titleMedium.copy(fontFamily = MonoFontFamily),
                            color = MaterialTheme.colorScheme.primary,
                        )
                        Text(
                            text = "Records",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }

                Column(
                    modifier = Modifier.weight(1f),
                    verticalArrangement = Arrangement.spacedBy(7.dp),
                ) {
                    slices.forEach { slice ->
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                            ) {
                                Box(
                                    modifier = Modifier
                                        .size(10.dp)
                                        .clip(CircleShape)
                                        .background(slice.color),
                                )
                                Text(
                                    text = slice.label,
                                    style = MaterialTheme.typography.labelLarge,
                                )
                            }
                            Text(
                                text = NumberFormat.getIntegerInstance(Locale.US).format(slice.count),
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun TelemetryTile(
    value: String,
    label: String,
    icon: ImageVector,
    modifier: Modifier = Modifier,
) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.3f)),
        modifier = modifier,
    ) {
        Column(
            modifier = Modifier.padding(vertical = 12.dp, horizontal = 6.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(4.dp),
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                modifier = Modifier.size(18.dp),
                tint = MaterialTheme.colorScheme.primary,
            )
            Text(
                text = value,
                style = MaterialTheme.typography.labelLarge.copy(fontFamily = MonoFontFamily),
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
            Text(
                text = label,
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}
