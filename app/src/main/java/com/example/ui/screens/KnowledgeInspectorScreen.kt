package com.example.ui.screens

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.Add
import androidx.compose.material.icons.rounded.CloudDownload
import androidx.compose.material.icons.rounded.DeleteOutline
import androidx.compose.material.icons.rounded.Edit
import androidx.compose.material.icons.rounded.ExpandLess
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material.icons.rounded.Search
import androidx.compose.material.icons.rounded.Storage
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonDefaults
import androidx.compose.material3.SingleChoiceSegmentedButtonRow
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.R
import com.example.model.KnowledgeEntry
import com.example.model.KnowledgeStats
import com.example.model.VaultRecord
import com.example.ui.AiUiState
import com.example.ui.components.FormattedResponseText
import com.example.ui.theme.MonoFontFamily
import java.text.NumberFormat
import java.util.Locale

private val INSPECTOR_CATEGORIES = listOf(
    "All", "English", "Horticulture", "Computer Science", "Math", "General", "Online Cached", "Learned"
)

private val VAULT_DOMAINS = listOf("All", "Math", "Computer Science", "Horticulture", "English")

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun KnowledgeInspectorScreen(
    uiState: AiUiState,
    onBack: () -> Unit,
    onOpenGather: () -> Unit,
    onTabChange: (Int) -> Unit,
    onSearchChange: (String) -> Unit,
    onCategoryChange: (String) -> Unit,
    onVaultSearchChange: (String) -> Unit,
    onVaultDomainChange: (String) -> Unit,
    onAddNew: () -> Unit,
    onEditEntry: (KnowledgeEntry) -> Unit,
    onDeleteEntry: (Int) -> Unit,
) {
    BackHandler(onBack = onBack)

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        contentWindowInsets = WindowInsets.statusBars,
        topBar = {
            TopAppBar(
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                ),
                navigationIcon = {
                    IconButton(
                        onClick = onBack,
                        modifier = Modifier.testTag("inspector_back_button"),
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Rounded.ArrowBack,
                            contentDescription = stringResource(R.string.back_cd),
                        )
                    }
                },
                title = {
                    Column {
                        Text(
                            text = stringResource(R.string.inspector_title),
                            style = MaterialTheme.typography.titleLarge,
                        )
                        Text(
                            text = "${NumberFormat.getIntegerInstance(Locale.US).format(uiState.stats.combinedOfflineRecords)} Total Offline Records",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                },
                actions = {
                    IconButton(
                        onClick = onOpenGather,
                        modifier = Modifier.testTag("inspector_gather_button"),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.CloudDownload,
                            contentDescription = stringResource(R.string.open_gather_cd),
                            tint = MaterialTheme.colorScheme.secondary,
                        )
                    }
                },
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = onAddNew,
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
                modifier = Modifier.testTag("add_knowledge_fab"),
            ) {
                Icon(
                    imageVector = Icons.Rounded.Add,
                    contentDescription = stringResource(R.string.add_knowledge_cd),
                )
            }
        },
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentAlignment = Alignment.TopCenter,
        ) {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .widthIn(max = 720.dp),
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 92.dp),
                verticalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                item {
                    SingleChoiceSegmentedButtonRow(modifier = Modifier.fillMaxWidth()) {
                        SegmentedButton(
                            selected = uiState.inspectorTab == 0,
                            onClick = { onTabChange(0) },
                            shape = SegmentedButtonDefaults.itemShape(index = 0, count = 2),
                            modifier = Modifier.testTag("inspector_tab_semantic"),
                        ) {
                            Text("Semantic Brain (${uiState.stats.totalEntries})")
                        }
                        SegmentedButton(
                            selected = uiState.inspectorTab == 1,
                            onClick = { onTabChange(1) },
                            shape = SegmentedButtonDefaults.itemShape(index = 1, count = 2),
                            modifier = Modifier.testTag("inspector_tab_vault"),
                        ) {
                            Text("1M+ Data Vault")
                        }
                    }
                }

                if (uiState.inspectorTab == 0) {
                    item {
                        DatabaseStatsCard(stats = uiState.stats)
                    }

                    item {
                        OutlinedTextField(
                            value = uiState.inspectorSearch,
                            onValueChange = onSearchChange,
                            placeholder = { Text(stringResource(R.string.inspector_search_hint)) },
                            leadingIcon = { Icon(Icons.Rounded.Search, contentDescription = null) },
                            singleLine = true,
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .testTag("inspector_search_field"),
                        )
                    }

                    item {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            INSPECTOR_CATEGORIES.forEach { cat ->
                                FilterChip(
                                    selected = uiState.inspectorCategory == cat,
                                    onClick = { onCategoryChange(cat) },
                                    label = { Text(cat) },
                                    modifier = Modifier.testTag("inspector_filter_${cat.lowercase().replace(" ", "_")}"),
                                )
                            }
                        }
                    }

                    if (uiState.inspectorEntries.isEmpty()) {
                        item { EmptyInspectorState() }
                    } else {
                        items(uiState.inspectorEntries, key = { it.id }) { entry ->
                            KnowledgeEntryCard(
                                entry = entry,
                                onEdit = { onEditEntry(entry) },
                                onDelete = { onDeleteEntry(entry.id) },
                            )
                        }
                    }
                } else {
                    item {
                        VaultSummaryBanner(stats = uiState.stats)
                    }

                    item {
                        OutlinedTextField(
                            value = uiState.vaultSearch,
                            onValueChange = onVaultSearchChange,
                            placeholder = { Text("Search 1,050,000+ rows (e.g. port_443, num_1729, Arabica)…") },
                            leadingIcon = { Icon(Icons.Rounded.Search, contentDescription = null) },
                            singleLine = true,
                            shape = RoundedCornerShape(16.dp),
                            modifier = Modifier
                                .fillMaxWidth()
                                .testTag("vault_search_field"),
                        )
                    }

                    item {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .horizontalScroll(rememberScrollState()),
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            VAULT_DOMAINS.forEach { dom ->
                                FilterChip(
                                    selected = uiState.vaultDomain == dom,
                                    onClick = { onVaultDomainChange(dom) },
                                    label = { Text(dom) },
                                    modifier = Modifier.testTag("vault_filter_${dom.lowercase().replace(" ", "_")}"),
                                )
                            }
                        }
                    }

                    if (uiState.vaultResults.isEmpty()) {
                        item { EmptyInspectorState() }
                    } else {
                        items(uiState.vaultResults, key = { it.id }) { rec ->
                            VaultRecordCard(record = rec)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun EmptyInspectorState() {
    Card(
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(6.dp),
        ) {
            Icon(
                imageVector = Icons.Rounded.Storage,
                contentDescription = null,
                modifier = Modifier.size(36.dp),
                tint = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            Text(
                text = stringResource(R.string.empty_search_title),
                style = MaterialTheme.typography.titleMedium,
            )
            Text(
                text = stringResource(R.string.empty_search_subtitle),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun VaultSummaryBanner(stats: KnowledgeStats) {
    val v = stats.vault
    Card(
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.tertiaryContainer.copy(alpha = 0.6f)),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text(
                    text = v.stage,
                    style = MaterialTheme.typography.titleMedium,
                )
                Text(
                    text = "${NumberFormat.getIntegerInstance(Locale.US).format(v.totalRecords)} rows",
                    style = MaterialTheme.typography.labelLarge.copy(fontFamily = MonoFontFamily),
                    color = MaterialTheme.colorScheme.primary,
                )
            }
            LinearProgressIndicator(
                progress = { if (v.isComplete) 1f else v.progress.coerceIn(0.02f, 1f) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(6.dp),
            )
            Text(
                text = "Indexed SQLite storage (${v.sizeMb} MB): 400k Math • 300k CS/Ports/Unicode • 200k Horticulture • 150k English.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun VaultRecordCard(record: VaultRecord) {
    Card(
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.35f)),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(5.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
            ) {
                Text(
                    text = record.domain,
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.primary,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    text = "#${record.id} • ${record.topicKey}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Text(
                text = record.title,
                style = MaterialTheme.typography.titleMedium,
            )
            Text(
                text = record.fact,
                style = MaterialTheme.typography.bodyMedium.copy(fontFamily = MonoFontFamily),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun DatabaseStatsCard(stats: KnowledgeStats) {
    Card(
        shape = RoundedCornerShape(20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.55f)),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.primary.copy(alpha = 0.25f)),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = "Maya Semantic Brain Metrics",
                    style = MaterialTheme.typography.titleMedium,
                    color = MaterialTheme.colorScheme.onPrimaryContainer,
                )
                Text(
                    text = "Avg Boost ${stats.avgReinforcement}x",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.primary,
                )
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                StatMetricBox(
                    value = "${stats.totalEntries}",
                    label = "Total Q&A",
                    modifier = Modifier.weight(1f),
                )
                StatMetricBox(
                    value = "${stats.onlineCachedCount}",
                    label = "Web Cached",
                    modifier = Modifier.weight(1f),
                )
                StatMetricBox(
                    value = "${stats.learnedCount}",
                    label = "Learned",
                    modifier = Modifier.weight(1f),
                )
                StatMetricBox(
                    value = "${stats.vocabSize}",
                    label = "Terms",
                    modifier = Modifier.weight(1f),
                )
            }
        }
    }
}

@Composable
private fun StatMetricBox(
    value: String,
    label: String,
    modifier: Modifier = Modifier,
) {
    Surface(
        shape = RoundedCornerShape(14.dp),
        color = MaterialTheme.colorScheme.surface,
        modifier = modifier,
    ) {
        Column(
            modifier = Modifier.padding(vertical = 10.dp, horizontal = 4.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(
                text = value,
                style = MaterialTheme.typography.titleMedium.copy(fontFamily = MonoFontFamily),
                color = MaterialTheme.colorScheme.primary,
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

@Composable
private fun KnowledgeEntryCard(
    entry: KnowledgeEntry,
    onEdit: () -> Unit,
    onDelete: () -> Unit,
) {
    var expanded by remember(entry.id) { mutableStateOf(false) }

    val (badgeBg, badgeFg, badgeLabel) = when (entry.source) {
        "learned" -> Triple(
            MaterialTheme.colorScheme.secondaryContainer,
            MaterialTheme.colorScheme.onSecondaryContainer,
            "Self-Learned",
        )
        "online_cached" -> Triple(
            MaterialTheme.colorScheme.primaryContainer,
            MaterialTheme.colorScheme.onPrimaryContainer,
            "Online Cached",
        )
        else -> Triple(
            MaterialTheme.colorScheme.tertiaryContainer,
            MaterialTheme.colorScheme.onTertiaryContainer,
            "Pre-Seeded",
        )
    }

    Card(
        onClick = { expanded = !expanded },
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.35f)),
        modifier = Modifier
            .fillMaxWidth()
            .testTag("knowledge_card_${entry.id}"),
    ) {
        Column(
            modifier = Modifier.padding(14.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Surface(
                        shape = RoundedCornerShape(50),
                        color = badgeBg,
                    ) {
                        Text(
                            text = badgeLabel,
                            style = MaterialTheme.typography.labelSmall,
                            color = badgeFg,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                        )
                    }
                    Text(
                        text = entry.category,
                        style = MaterialTheme.typography.labelMedium,
                        color = MaterialTheme.colorScheme.primary,
                        fontWeight = FontWeight.SemiBold,
                    )
                }

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        text = "w=${"%.2f".format(entry.reinforcementWeight)} • ${entry.timesUsed}x",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                    Icon(
                        imageVector = if (expanded) Icons.Rounded.ExpandLess else Icons.Rounded.ExpandMore,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }

            Text(
                text = entry.question,
                style = MaterialTheme.typography.titleMedium,
                maxLines = if (expanded) Int.MAX_VALUE else 2,
                overflow = TextOverflow.Ellipsis,
            )

            AnimatedVisibility(visible = expanded) {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    FormattedResponseText(
                        text = entry.answer,
                        style = MaterialTheme.typography.bodyMedium,
                    )
                    if (entry.tags.isNotBlank()) {
                        Text(
                            text = "Tags: ${entry.tags}",
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.End,
                    ) {
                        IconButton(
                            onClick = onEdit,
                            modifier = Modifier.testTag("edit_entry_${entry.id}"),
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.Edit,
                                contentDescription = stringResource(R.string.edit_entry_cd),
                                tint = MaterialTheme.colorScheme.primary,
                            )
                        }
                        IconButton(
                            onClick = onDelete,
                            modifier = Modifier.testTag("delete_entry_${entry.id}"),
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.DeleteOutline,
                                contentDescription = stringResource(R.string.delete_entry_cd),
                                tint = MaterialTheme.colorScheme.error,
                            )
                        }
                    }
                }
            }
        }
    }
}
