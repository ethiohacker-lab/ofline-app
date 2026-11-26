package com.example.ui.screens

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.WindowInsets
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.statusBars
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.imePadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.Send
import androidx.compose.material.icons.rounded.AutoAwesome
import androidx.compose.material.icons.rounded.Calculate
import androidx.compose.material.icons.rounded.CheckCircle
import androidx.compose.material.icons.rounded.CloudDone
import androidx.compose.material.icons.rounded.CloudDownload
import androidx.compose.material.icons.rounded.Computer
import androidx.compose.material.icons.rounded.DeleteSweep
import androidx.compose.material.icons.rounded.Eco
import androidx.compose.material.icons.rounded.EditNote
import androidx.compose.material.icons.rounded.MenuBook
import androidx.compose.material.icons.rounded.OfflineBolt
import androidx.compose.material.icons.rounded.Psychology
import androidx.compose.material.icons.rounded.ThumbUp
import androidx.compose.material.icons.rounded.TipsAndUpdates
import androidx.compose.material.icons.rounded.Translate
import androidx.compose.material3.AssistChip
import androidx.compose.material3.AssistChipDefaults
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilledIconButton
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.IconButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import com.example.R
import com.example.model.AiResponse
import com.example.model.ChatMessage
import com.example.model.KnowledgeStats
import com.example.model.QuickDomain
import com.example.model.QuickPrompt
import com.example.ui.AiUiState
import com.example.ui.components.FormattedResponseText
import com.example.ui.theme.ConfidenceHigh
import com.example.ui.theme.ConfidenceHighBg
import com.example.ui.theme.ConfidenceLow
import com.example.ui.theme.ConfidenceLowBg
import com.example.ui.theme.ConfidenceMed
import com.example.ui.theme.ConfidenceMedBg
import com.example.ui.theme.MonoFontFamily
import kotlin.math.roundToInt

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ChatScreen(
    uiState: AiUiState,
    quickPrompts: List<QuickPrompt>,
    onInputChanged: (String) -> Unit,
    onSend: () -> Unit,
    onSelectDomain: (QuickDomain) -> Unit,
    onQuickPromptClick: (QuickPrompt) -> Unit,
    onHelpfulClick: (messageId: String, entryId: Int) -> Unit,
    onTeachClick: (question: String, answer: String, category: String, replaceId: Int?, messageId: String?) -> Unit,
    onGatherOnlineTopic: (String) -> Unit,
    onOpenGatherSheet: () -> Unit,
    onOpenInspector: () -> Unit,
    onClearChat: () -> Unit,
    onDismissBanner: () -> Unit,
) {
    val listState = rememberLazyListState()

    LaunchedEffect(uiState.messages.size) {
        if (uiState.messages.isNotEmpty()) {
            listState.animateScrollToItem(uiState.messages.lastIndex)
        }
    }

    val filteredPrompts = remember(uiState.selectedQuickDomain, quickPrompts) {
        if (uiState.selectedQuickDomain == QuickDomain.ALL) {
            listOf(
                quickPrompts.first { it.domain == QuickDomain.ENGLISH },
                quickPrompts.first { it.domain == QuickDomain.HORTICULTURE },
                quickPrompts.first { it.domain == QuickDomain.CS },
                quickPrompts.first { it.domain == QuickDomain.MATH },
                quickPrompts.first { it.title == "Offline Summarizer" },
                quickPrompts.first { it.title == "Study Quiz" },
            )
        } else {
            quickPrompts.filter { it.domain == uiState.selectedQuickDomain }
        }
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        contentWindowInsets = WindowInsets.statusBars,
        topBar = {
            TopAppBar(
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.background,
                ),
                title = {
                    Column {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                        ) {
                            Text(
                                text = stringResource(R.string.app_name),
                                style = MaterialTheme.typography.titleLarge,
                            )
                            Surface(
                                shape = RoundedCornerShape(50),
                                color = if (uiState.isOnline) {
                                    MaterialTheme.colorScheme.secondaryContainer
                                } else {
                                    MaterialTheme.colorScheme.primaryContainer
                                },
                            ) {
                                Row(
                                    modifier = Modifier.padding(horizontal = 8.dp, vertical = 3.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.spacedBy(4.dp),
                                ) {
                                    Icon(
                                        imageVector = if (uiState.isOnline) Icons.Rounded.CloudDone else Icons.Rounded.OfflineBolt,
                                        contentDescription = null,
                                        modifier = Modifier.size(12.dp),
                                        tint = if (uiState.isOnline) {
                                            MaterialTheme.colorScheme.onSecondaryContainer
                                        } else {
                                            MaterialTheme.colorScheme.onPrimaryContainer
                                        },
                                    )
                                    Text(
                                        text = if (uiState.isOnline) "ONLINE SYNC" else "OFFLINE",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = if (uiState.isOnline) {
                                            MaterialTheme.colorScheme.onSecondaryContainer
                                        } else {
                                            MaterialTheme.colorScheme.onPrimaryContainer
                                        },
                                    )
                                }
                            }
                        }
                        Text(
                            text = "${uiState.stats.totalEntries} Q&A • ${uiState.stats.vocabSize} terms",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                },
                actions = {
                    if (uiState.messages.isNotEmpty()) {
                        IconButton(
                            onClick = onClearChat,
                            modifier = Modifier.testTag("clear_chat_button"),
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.DeleteSweep,
                                contentDescription = stringResource(R.string.clear_chat_cd),
                            )
                        }
                    }
                    IconButton(
                        onClick = onOpenGatherSheet,
                        modifier = Modifier.testTag("gather_online_nav_button"),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.CloudDownload,
                            contentDescription = stringResource(R.string.open_gather_cd),
                            tint = MaterialTheme.colorScheme.secondary,
                        )
                    }
                    IconButton(
                        onClick = onOpenInspector,
                        modifier = Modifier.testTag("inspector_nav_button"),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.MenuBook,
                            contentDescription = stringResource(R.string.open_inspector_cd),
                            tint = MaterialTheme.colorScheme.primary,
                        )
                    }
                },
            )
        },
        bottomBar = {
            ChatComposerBar(
                query = uiState.inputQuery,
                selectedDomain = uiState.selectedQuickDomain,
                filteredPrompts = filteredPrompts,
                enabled = !uiState.isInitializing && !uiState.isThinking && uiState.initError == null,
                onInputChanged = onInputChanged,
                onSend = onSend,
                onSelectDomain = onSelectDomain,
                onQuickPromptClick = onQuickPromptClick,
            )
        },
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentAlignment = Alignment.TopCenter,
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .widthIn(max = 720.dp),
            ) {
                AnimatedVisibility(visible = uiState.statusBanner != null) {
                    uiState.statusBanner?.let { banner ->
                        Surface(
                            color = MaterialTheme.colorScheme.secondaryContainer,
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = 16.dp, vertical = 4.dp),
                            shape = RoundedCornerShape(12.dp),
                        ) {
                            Row(
                                modifier = Modifier.padding(horizontal = 12.dp, vertical = 8.dp),
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.SpaceBetween,
                            ) {
                                Text(
                                    text = banner,
                                    style = MaterialTheme.typography.labelLarge,
                                    color = MaterialTheme.colorScheme.onSecondaryContainer,
                                    modifier = Modifier.weight(1f),
                                )
                                TextButton(onClick = onDismissBanner) {
                                    Text("OK")
                                }
                            }
                        }
                    }
                }

                when {
                    uiState.isInitializing -> {
                        Box(
                            modifier = Modifier.fillMaxSize(),
                            contentAlignment = Alignment.Center,
                        ) {
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally,
                                verticalArrangement = Arrangement.spacedBy(12.dp),
                                modifier = Modifier.padding(24.dp),
                            ) {
                                CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                                Text(
                                    text = stringResource(R.string.initializing_python),
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                                )
                            }
                        }
                    }

                    uiState.initError != null -> {
                        Box(
                            modifier = Modifier.fillMaxSize(),
                            contentAlignment = Alignment.Center,
                        ) {
                            Card(
                                colors = CardDefaults.cardColors(containerColor = ConfidenceLowBg),
                                modifier = Modifier.padding(24.dp),
                            ) {
                                Text(
                                    text = "Python Engine Error: ${uiState.initError}",
                                    color = ConfidenceLow,
                                    style = MaterialTheme.typography.bodyLarge,
                                    modifier = Modifier.padding(16.dp),
                                )
                            }
                        }
                    }

                    uiState.messages.isEmpty() -> {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(16.dp),
                            verticalArrangement = Arrangement.spacedBy(14.dp),
                        ) {
                            item {
                                HeroWelcomeCard(
                                    stats = uiState.stats,
                                    isOnline = uiState.isOnline,
                                    onOpenGather = onOpenGatherSheet,
                                    onOpenInspector = onOpenInspector,
                                    onTeachNew = {
                                        onTeachClick("", "", "Learned", null, null)
                                    },
                                )
                            }
                            item {
                                Text(
                                    text = "Try Maya's Offline & Sync Capabilities",
                                    style = MaterialTheme.typography.titleMedium,
                                    modifier = Modifier.padding(top = 4.dp),
                                )
                            }
                            items(filteredPrompts) { prompt ->
                                StarterPromptCard(
                                    prompt = prompt,
                                    onClick = { onQuickPromptClick(prompt) },
                                )
                            }
                        }
                    }

                    else -> {
                        LazyColumn(
                            state = listState,
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 12.dp),
                            verticalArrangement = Arrangement.spacedBy(12.dp),
                        ) {
                            items(uiState.messages, key = { it.id }) { msg ->
                                if (msg.isUser) {
                                    UserBubble(text = msg.text)
                                } else {
                                    AiResponseCard(
                                        message = msg,
                                        isOnline = uiState.isOnline,
                                        onHelpfulClick = onHelpfulClick,
                                        onTeachClick = onTeachClick,
                                        onGatherOnlineClick = onGatherOnlineTopic,
                                    )
                                }
                            }
                            if (uiState.isThinking) {
                                item {
                                    Row(
                                        modifier = Modifier.padding(vertical = 8.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.spacedBy(10.dp),
                                    ) {
                                        CircularProgressIndicator(
                                            modifier = Modifier.size(18.dp),
                                            strokeWidth = 2.dp,
                                        )
                                        Text(
                                            text = "Maya is thinking…",
                                            style = MaterialTheme.typography.labelMedium,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun HeroWelcomeCard(
    stats: KnowledgeStats,
    isOnline: Boolean,
    onOpenGather: () -> Unit,
    onOpenInspector: () -> Unit,
    onTeachNew: () -> Unit,
) {
    Card(
        shape = RoundedCornerShape(24.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.45f)),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
    ) {
        Column {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(168.dp),
            ) {
                Image(
                    painter = painterResource(id = R.drawable.img_hero_scholar),
                    contentDescription = stringResource(R.string.hero_image_cd),
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize(),
                )
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .background(
                            Brush.verticalGradient(
                                listOf(
                                    Color.Transparent,
                                    MaterialTheme.colorScheme.surface.copy(alpha = 0.92f),
                                )
                            )
                        )
                )
                Surface(
                    color = MaterialTheme.colorScheme.primary,
                    shape = RoundedCornerShape(50),
                    modifier = Modifier
                        .align(Alignment.TopStart)
                        .padding(12.dp),
                ) {
                    Text(
                        text = stringResource(
                            if (isOnline) R.string.online_badge else R.string.offline_badge
                        ),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onPrimary,
                        modifier = Modifier.padding(horizontal = 10.dp, vertical = 5.dp),
                    )
                }
            }

            Column(
                modifier = Modifier.padding(horizontal = 18.dp, vertical = 14.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Text(
                    text = stringResource(R.string.hero_title),
                    style = MaterialTheme.typography.headlineMedium,
                )
                Text(
                    text = stringResource(R.string.hero_subtitle),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .horizontalScroll(rememberScrollState())
                        .padding(top = 4.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    MiniStatChip(label = "Seeded", value = "${stats.seededCount}")
                    MiniStatChip(label = "Web Cached", value = "${stats.onlineCachedCount}")
                    MiniStatChip(label = "Learned", value = "${stats.learnedCount}")
                    MiniStatChip(label = "Terms", value = "${stats.vocabSize}")
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 4.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    OutlinedButton(
                        onClick = onOpenGather,
                        modifier = Modifier
                            .weight(1f)
                            .height(48.dp)
                            .testTag("hero_gather_btn"),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.CloudDownload,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp),
                        )
                        Spacer(Modifier.width(5.dp))
                        Text("Sync Web", maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                    OutlinedButton(
                        onClick = onOpenInspector,
                        modifier = Modifier
                            .weight(1f)
                            .height(48.dp)
                            .testTag("hero_inspector_btn"),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.MenuBook,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp),
                        )
                        Spacer(Modifier.width(5.dp))
                        Text("Brain", maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                    Button(
                        onClick = onTeachNew,
                        modifier = Modifier
                            .weight(1f)
                            .height(48.dp)
                            .testTag("hero_teach_btn"),
                    ) {
                        Icon(
                            imageVector = Icons.Rounded.Psychology,
                            contentDescription = null,
                            modifier = Modifier.size(18.dp),
                        )
                        Spacer(Modifier.width(5.dp))
                        Text("Teach", maxLines = 1, overflow = TextOverflow.Ellipsis)
                    }
                }
            }
        }
    }
}

@Composable
private fun MiniStatChip(label: String, value: String) {
    Surface(
        shape = RoundedCornerShape(12.dp),
        color = MaterialTheme.colorScheme.surfaceVariant,
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
            horizontalArrangement = Arrangement.spacedBy(5.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = value,
                style = MaterialTheme.typography.labelLarge.copy(fontFamily = MonoFontFamily),
                color = MaterialTheme.colorScheme.primary,
            )
            Text(
                text = label,
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}

@Composable
private fun StarterPromptCard(
    prompt: QuickPrompt,
    onClick: () -> Unit,
) {
    val icon = when (prompt.domain) {
        QuickDomain.ENGLISH -> Icons.Rounded.Translate
        QuickDomain.MATH -> Icons.Rounded.Calculate
        QuickDomain.HORTICULTURE -> Icons.Rounded.Eco
        QuickDomain.CS -> Icons.Rounded.Computer
        QuickDomain.ALL -> Icons.Rounded.AutoAwesome
    }

    Card(
        onClick = onClick,
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.35f)),
        modifier = Modifier
            .fillMaxWidth()
            .testTag("starter_prompt_${prompt.title.lowercase().replace(" ", "_")}"),
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(MaterialTheme.colorScheme.primaryContainer),
                contentAlignment = Alignment.Center,
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = MaterialTheme.colorScheme.onPrimaryContainer,
                )
            }
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "${prompt.domain.label} • ${prompt.title}",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.primary,
                )
                Text(
                    text = prompt.query,
                    style = MaterialTheme.typography.bodyMedium.copy(fontFamily = MonoFontFamily),
                    color = MaterialTheme.colorScheme.onSurface,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
    }
}

@Composable
private fun UserBubble(text: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.End,
    ) {
        Surface(
            color = MaterialTheme.colorScheme.primary,
            shape = RoundedCornerShape(topStart = 20.dp, topEnd = 6.dp, bottomStart = 20.dp, bottomEnd = 20.dp),
            modifier = Modifier.widthIn(max = 310.dp),
        ) {
            Text(
                text = text,
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onPrimary,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 12.dp),
            )
        }
    }
}

@Composable
private fun AiResponseCard(
    message: ChatMessage,
    isOnline: Boolean,
    onHelpfulClick: (messageId: String, entryId: Int) -> Unit,
    onTeachClick: (question: String, answer: String, category: String, replaceId: Int?, messageId: String?) -> Unit,
    onGatherOnlineClick: (String) -> Unit,
) {
    val resp: AiResponse? = message.aiResponse

    Card(
        shape = RoundedCornerShape(topStart = 6.dp, topEnd = 20.dp, bottomStart = 20.dp, bottomEnd = 20.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline.copy(alpha = 0.4f)),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            if (resp != null) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    DomainPill(category = resp.category, tag = resp.tag)
                    ConfidenceBadge(confidence = resp.confidence, route = resp.route)
                }
            }

            FormattedResponseText(text = message.text)

            if (resp != null && resp.formulaSteps.isNotBlank()) {
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant,
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Text(
                        text = resp.formulaSteps,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(10.dp),
                    )
                }
            }

            if (resp?.closestGuess != null) {
                val guess = resp.closestGuess
                Surface(
                    shape = RoundedCornerShape(14.dp),
                    color = MaterialTheme.colorScheme.secondaryContainer.copy(alpha = 0.55f),
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.secondary.copy(alpha = 0.35f)),
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Column(
                        modifier = Modifier.padding(12.dp),
                        verticalArrangement = Arrangement.spacedBy(4.dp),
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            horizontalArrangement = Arrangement.spacedBy(6.dp),
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.TipsAndUpdates,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                                tint = MaterialTheme.colorScheme.secondary,
                            )
                            Text(
                                text = "Closest Guess (${(guess.confidence * 100).roundToInt()}% • ${guess.category})",
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.onSecondaryContainer,
                            )
                        }
                        Text(
                            text = guess.question,
                            style = MaterialTheme.typography.labelMedium,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.onSurface,
                        )
                        FormattedResponseText(
                            text = guess.answer,
                            style = MaterialTheme.typography.bodyMedium,
                        )
                    }
                }
            }

            if (resp != null && resp.route !in setOf("math_engine", "datetime", "conversational", "summarizer", "dictionary")) {
                if (resp.needsTeaching) {
                    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        if (isOnline) {
                            OutlinedButton(
                                onClick = { onGatherOnlineClick(message.userQueryForMessage) },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(48.dp)
                                    .testTag("gather_online_inline_button"),
                            ) {
                                Icon(
                                    imageVector = Icons.Rounded.CloudDownload,
                                    contentDescription = null,
                                    modifier = Modifier.size(18.dp),
                                )
                                Spacer(Modifier.width(8.dp))
                                Text(stringResource(R.string.btn_gather_online))
                            }
                        }

                        Button(
                            onClick = {
                                onTeachClick(
                                    message.userQueryForMessage,
                                    "",
                                    resp.category,
                                    null,
                                    message.id,
                                )
                            },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = MaterialTheme.colorScheme.secondary,
                            ),
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(48.dp)
                                .testTag("teach_ai_button"),
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.Psychology,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp),
                            )
                            Spacer(Modifier.width(8.dp))
                            Text(stringResource(R.string.btn_teach_ai))
                        }
                    }
                } else if (resp.matchedId != null) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        OutlinedButton(
                            onClick = {
                                if (!message.isReinforced) {
                                    onHelpfulClick(message.id, resp.matchedId)
                                }
                            },
                            enabled = !message.isReinforced,
                            modifier = Modifier
                                .height(48.dp)
                                .testTag("helpful_button"),
                        ) {
                            Icon(
                                imageVector = if (message.isReinforced) Icons.Rounded.CheckCircle else Icons.Rounded.ThumbUp,
                                contentDescription = null,
                                modifier = Modifier.size(16.dp),
                            )
                            Spacer(Modifier.width(6.dp))
                            Text(
                                text = stringResource(
                                    if (message.isReinforced) R.string.btn_helpful_done else R.string.btn_helpful
                                ),
                                style = MaterialTheme.typography.labelMedium,
                            )
                        }

                        TextButton(
                            onClick = {
                                onTeachClick(
                                    resp.matchedQuestion ?: message.userQueryForMessage,
                                    resp.answer,
                                    resp.category,
                                    resp.matchedId,
                                    message.id,
                                )
                            },
                            modifier = Modifier
                                .height(48.dp)
                                .testTag("teach_better_button"),
                        ) {
                            Icon(
                                imageVector = Icons.Rounded.EditNote,
                                contentDescription = null,
                                modifier = Modifier.size(18.dp),
                            )
                            Spacer(Modifier.width(4.dp))
                            Text(
                                text = stringResource(R.string.btn_teach_better),
                                style = MaterialTheme.typography.labelMedium,
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun DomainPill(category: String, tag: String) {
    val label = if (tag.isNotBlank()) "$category • $tag" else category
    Surface(
        shape = RoundedCornerShape(50),
        color = MaterialTheme.colorScheme.tertiaryContainer,
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onTertiaryContainer,
            modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp),
        )
    }
}

@Composable
private fun ConfidenceBadge(confidence: Double, route: String) {
    val pct = (confidence * 100.0).roundToInt()
    val (bg, fg, label) = when {
        route in setOf("math_engine", "datetime", "conversational", "summarizer", "quiz") ->
            Triple(ConfidenceHighBg, ConfidenceHigh, "100% Exact")
        route == "online_cached" -> Triple(ConfidenceHighBg, ConfidenceHigh, "Cached Online")
        confidence >= 0.65 -> Triple(ConfidenceHighBg, ConfidenceHigh, "$pct% Match")
        confidence >= 0.30 -> Triple(ConfidenceMedBg, ConfidenceMed, "$pct% Low")
        else -> Triple(ConfidenceLowBg, ConfidenceLow, "$pct% Unknown")
    }
    Surface(
        shape = RoundedCornerShape(50),
        color = bg,
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = fg,
            modifier = Modifier.padding(horizontal = 9.dp, vertical = 4.dp),
        )
    }
}

@Composable
private fun ChatComposerBar(
    query: String,
    selectedDomain: QuickDomain,
    filteredPrompts: List<QuickPrompt>,
    enabled: Boolean,
    onInputChanged: (String) -> Unit,
    onSend: () -> Unit,
    onSelectDomain: (QuickDomain) -> Unit,
    onQuickPromptClick: (QuickPrompt) -> Unit,
) {
    Surface(
        color = MaterialTheme.colorScheme.surface,
        tonalElevation = 4.dp,
        shadowElevation = 6.dp,
        modifier = Modifier
            .fillMaxWidth()
            .imePadding(),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(top = 8.dp, bottom = 10.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(horizontal = 14.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                QuickDomain.entries.forEach { domain ->
                    FilterChip(
                        selected = selectedDomain == domain,
                        onClick = { onSelectDomain(domain) },
                        label = { Text(domain.label) },
                        modifier = Modifier.testTag("quick_domain_${domain.name.lowercase()}"),
                    )
                }
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(horizontal = 14.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                filteredPrompts.forEach { prompt ->
                    AssistChip(
                        onClick = { onQuickPromptClick(prompt) },
                        label = { Text(prompt.title) },
                        colors = AssistChipDefaults.assistChipColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant,
                        ),
                        modifier = Modifier.testTag("quick_prompt_${prompt.title.lowercase().replace(" ", "_")}"),
                    )
                }
            }

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 14.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                OutlinedTextField(
                    value = query,
                    onValueChange = onInputChanged,
                    placeholder = {
                        Text(
                            text = stringResource(R.string.chat_input_placeholder),
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                        )
                    },
                    enabled = enabled,
                    shape = RoundedCornerShape(24.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedContainerColor = MaterialTheme.colorScheme.background,
                        unfocusedContainerColor = MaterialTheme.colorScheme.background,
                    ),
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Send),
                    keyboardActions = KeyboardActions(onSend = { onSend() }),
                    maxLines = 4,
                    modifier = Modifier
                        .weight(1f)
                        .testTag("chat_input_field"),
                )

                FilledIconButton(
                    onClick = onSend,
                    enabled = enabled && query.isNotBlank(),
                    shape = CircleShape,
                    colors = IconButtonDefaults.filledIconButtonColors(
                        containerColor = MaterialTheme.colorScheme.primary,
                    ),
                    modifier = Modifier
                        .size(52.dp)
                        .testTag("send_button"),
                ) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Rounded.Send,
                        contentDescription = stringResource(R.string.send_message_cd),
                    )
                }
            }
        }
    }
}
